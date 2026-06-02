import json
import os
import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion():
    logger.info("🚀 Starting data ingestion pipeline...")
    
    # Define paths dynamically
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "mall_data.json")
    persist_directory = os.path.join(current_dir, "../chroma_db_storage")
    
    # 1. Load raw JSON data
    if not os.path.exists(json_path):
        logger.error(f"❌ Source data file not found at {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # 2. Parse and convert to LangChain Document structures
    documents = []
    
    for store in data.get("stores", []):
        name = store.get("name")
        hours = store.get("hours", "Not specified")
        if name:
            text = f"Store: {name}. Hours: {hours}"
            documents.append(Document(page_content=text, metadata={"type": "store", "name": name}))
            
    for promo in data.get("promotions", []):
        promo_text = promo.get("promotion")
        store_name = promo.get("store")
        if promo_text and store_name:
            text = f"Promotion: {promo_text} at {store_name}"
            documents.append(Document(page_content=text, metadata={"type": "promo", "store": store_name}))

    if not documents:
        logger.error("❌ No valid records found to index.")
        return

    # 3. Initialize localized open-source embedding model
    logger.info("🧠 Generating embeddings via HuggingFace (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    
    # 4. Build and persist vector store on disk
    logger.info(f"📦 Indexing {len(documents)} documents into persistent Chroma DB...")
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    logger.info(f"🎉 Success! Vector database securely persisted at: {persist_directory}")

if __name__ == "__main__":
    run_ingestion()