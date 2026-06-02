import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
    GCP_REGION = "us-central1"
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "mall-rag")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # API Settings
    API_TITLE = "Enterprise RAG Chatbot"
    API_VERSION = "1.0.0"
    DEBUG = ENVIRONMENT == "development"

settings = Settings()