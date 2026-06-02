import os
import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        """
        Clean initialization of service tracking attributes.
        """
        self.retriever = None
        self.llm = None

    def initialize(self):
        """
        Connects to the pre-computed persistent vector database and initializes Gemini LLM.
        """
        try:
            # 1. Define paths dynamically relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            persist_directory = os.path.join(current_dir, "chroma_db_storage")
            
            # Fallback path logic in case the project structure root shifts
            if not os.path.exists(persist_directory):
                persist_directory = os.path.abspath(os.path.join(current_dir, "../chroma_db_storage"))

            # Safety fallback validation for Fiverr clients
            if not os.path.exists(persist_directory):
                logger.error(f"❌ Vector storage directory missing at {persist_directory}. Please run 'python data/ingest.py' first.")
                raise FileNotFoundError("Chroma DB persistent directory not found. Ingestion required.")

            # 2. Load localized embedding schema
            logger.info("🔄 Loading local HuggingFace embedding model...")
            embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
            
            # 3. Connect directly to the persisted Chroma DB storage (Instant load)
            logger.info("🔌 Connecting to persistent Chroma DB storage...")
            vectordb = Chroma(
                persist_directory=persist_directory, 
                embedding_function=embeddings
            )
            
            # 4. Initialize enterprise Gemini LLM interface
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is missing.")

            logger.info("⚡ Authenticating Google Gemini LLM API...")
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                google_api_key=api_key,
                temperature=0.7
            )
            
            # 5. Set up context retriever configuration (Fetch top 2 most relevant chunks)
            retriever = vectordb.as_retriever(search_kwargs={"k": 2})
            
            # 6. Save for query
            self.retriever = retriever
            self.llm = llm
            
            logger.info("🚀 RAG Pipeline successfully initialized and ready for production.")
            
        except Exception as e:
            logger.error(f"💥 Failed to initialize RAG Service: {e}")
            raise
    
    def query(self, query_text: str) -> dict:
        """
        Executes semantic search over corporate context and builds response using Gemini LLM.
        """
        try:
            if not self.retriever or not self.llm:
                return {"answer": "RAG service runtime not correctly initialized.", "sources": []}

            # 1. Retrieve highly relevant document nodes
            docs = self.retriever.invoke(query_text)
            
            # 2. Consolidate context strings
            context = "\n".join([doc.page_content for doc in docs])
            
            # 3. Construct professional enterprise prompt constraints
            prompt = (
                f"You are a friendly and helpful shopping mall assistant. "
                f"Answer the customer's question in a conversational way based on the provided context. "
                f"Be concise, mention relevant promotions if applicable, and be welcoming.\n\n"
                f"Context:\n{context}\n\n"
                f"Customer Question: {query_text}\n"
                f"Response:"
            )
            
            # 4. Request context-bounded LLM inference
            response = self.llm.invoke(prompt)
            
            return {
                "answer": response.content,
                "sources": [{"text": doc.page_content} for doc in docs]
            }
        except Exception as e:
            logger.error(f"❌ Error occurred during query orchestration: {e}")
            return {"answer": "An enterprise backend error occurred while processing your request.", "sources": []}