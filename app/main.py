from models.vectore_store import VectoreStore
from config import Config
from services.storage_service import S3StorageService
from services.llm_service import LLMService
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import logging
import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

vector_store = VectoreStore(Config.VECTOR_DB_PATH)
storage_service = S3StorageService()
llm_service = LLMService(vector_store)

@app.route("/")
def index():
    return render_template("index.html")


# configure logging
logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Application initialized successfully")


def process_file(file):
    """Process the document and return text chunks """
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    try:
        file.save(temp_path)

        if file.filename.endwith(".pdf"):
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
        elif file.filename.endswith(".txt"):
            loader = TextLoader(temp_path)
            documents = loader.load()
        else:
            logger.error(f"Unsupported file type: {file.filename}")
            raise ValueError("Unsupported file type. Only PDF and TXT are allowed.")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents);
        
        return text_chunks
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")

    finally:
        if(os.path.exists(temp_path)):
            os.remove(temp_path)
        os.rmdir(temp_dir)
            

@app.route("/upload", methods=["POST"])
def upload_document():
    try:
        logger.debug("Upload route is called");

        if "file" not in request.files:
            logger.warning("No file part in the request")
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files["file"]
        if(file.filename == ""):
            logger.warning("Empty file name")
            return jsonify({'error': 'No file selected for uploading'}), 400
        
        if not file.filename.endswith((".pdf", ".txt")):
            logger.warning(f"Unsupported file type: {file.filename}")
            return jsonify({'error': f'Unsupported file type. Only PDF and TXT are allowed. {file.filename}'}), 400
    
        logger.debug(f"Processing file Started ... : {file.filename}")

        try:
            text_chunks = process_file(file)
            logger.debug(f"Chunck created successfully, number of chunks: {len(text_chunks)}")
        except Exception as e:
            logger.error(f"Error processing file chunks: {e}")
            return jsonify({'error': f'An error occurred while processing the file: {e}'}), 500

        try:
            file.seek(0)
            storage_result = storage_service.upload_file(file, file.filename)
            if storage_result is False:
                logger.error("Failed to upload file to S3")
                return jsonify({'error': 'Failed to upload file to storage'}), 500
        except Exception as e:
            logger.error(f"Error uploading file to storage: {e}")
            return jsonify({'error': f'An error occurred while uploading the file: {e}'}), 500
    


        try:
            vector_store.add_documents(text_chunks)
            logger.debug("Documents added to vector store successfully")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return jsonify({'error': f'An error occurred while adding documents to the vector store: {e}'}), 500
        
        
        return jsonify(
            {
                'message': 'File uploaded and processed successfully.',
                'file_name': file.filename,
                'num_chunks': len(text_chunks)
            }), 200

    except Exception as e: 
        logger.error(f"Error in upload route: {e}")
        return jsonify({'error': f'An error occurred while uploading the file: {e}'}), 500 
    
@app.route("/query", methods=["POST"])
def query():
        data = request.json
        if 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
        
        try:
            response = llm_service.get_response(data['question'])
            return jsonify({{'response': response}}), 200
        except Exception as e: 
            logger.error(f"Error getting response from LLM: {e}")
            return jsonify({'error': f'An error occurred while getting response from LLM: {e}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1982, debug=True)

