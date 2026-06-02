from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import logging
import os
from services.rag_service import RAGService
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enterprise RAG Chatbot",
    description="RAG chatbot for shopping malls using ChromaDB and Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
rag_service = RAGService()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list
    latency_ms: float

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing RAG service...")
    rag_service.initialize()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    start_time = time.time()
    
    try:
        result = rag_service.query(request.query)
        latency_ms = (time.time() - start_time) * 1000
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency_ms=latency_ms
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)