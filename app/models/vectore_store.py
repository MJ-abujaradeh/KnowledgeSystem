import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from config import Config
class VectoreStore:
    def __init__(self, path):
        self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key= Config.OPENAI_API_KEY
        );
        self.vector_store = Chroma(
            persist_directory = path,
            embedding_function = self.embeddings,
            collection_name = "knowledge_system_collection"
        )
        
    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def similarity_search(self, query, k=4):
        return self.vector_store.similarity_search(query, k=k)
