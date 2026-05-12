from models.vectore_store import VectoreStore
from app.config import Config
from services.storage_service import S3StorageService
from services.llm_service import LLMService
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import logging
import os

vector_store = VectoreStore(Config.VECTOR_DB_PATH)
storage_service = S3StorageService()
llm_service = LLMService(vector_store)

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
            


