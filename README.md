# Enterprise RAG Chatbot - Shopping Mall Assistant

A production-ready, high-performance RAG (Retrieval-Augmented Generation) system tailored for shopping mall customer support and enterprise concierge services. Built using a modern, scalable stack featuring FastAPI, LangChain, Google Gemini, and ChromaDB.

## 🌟 Key Features

* **Advanced Vector Search:** Powered by ChromaDB and HuggingFace embeddings (`all-MiniLM-L6-v2`) for ultra-fast, context-aware semantic retrieval.
* **Gemini LLM:** Leverages Google's `Gemini 2.0 Flash` model via Google Gen AI SDK for rapid, human-like responses.
* **Strict Citation Support:** Every response returns source context snippets, ensuring transparency and reducing LLM hallucinations.
* **Asynchronous Backend:** Built with FastAPI for high-throughput, low-latency API handling.
* **React Frontend:** User-friendly chat interface
* **Production Preparedness:** Equipped with robust error handling, structured logging, health-check endpoints, and full CORS support.


## 🧩 Architecture Flow

```text
[User Query] ──> [FastAPI Endpoint] ──> [LangChain RAG Chain]
                                                 │
 [Gemini LLM Response] <── [ChromaDB Vector] <───┘
```

## 📊 Performance & Scalability Metrics

| Metric | Measurement / Target | Technical Notes |
| :--- | :--- | :--- |
| **Average Latency** | 1000ms - 2000ms | Includes Embedding Generation + Vector Search + LLM Inference |
| **Time to First Token**| ~1.2 seconds | Highly optimized using lightweight token payloads |
| **Concurrency** | Scalable via Cloud Run | Stateless container design allows horizontal autoscaling |
| **Cost per Request** | ~$0.0005 USD | Highly cost-efficient infrastructure utilizing Gemini API |

## ⚙️ Tech Stack

* **Backend:** Python 3.11+, FastAPI, LangChain
* **Vector Database:** ChromaDB
* **LLM Platform:** Google Gemini Enterprise (Vertex AI / Google AI Studio)
* **Embeddings:** HuggingFace Core (`all-MiniLM-L6-v2`)
* **Frontend:** React 18, Vite, CSS3
* **Deployment Ready:** Docker, Google Cloud Run

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+
- Google API Key (Get one at Google AI Studio)
- Virtual environment (optional but recommended)
- Git

### Backend Setup & Data Ingestion

```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
# Create a .env file in the root directory with the following keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GCP_PROJECT_ID=your_gcp_project_id_here
GOOGLE_APPLICATION_CREDENTIALS=backend/credentials.json
ENVIRONMENT=development # Change to 'production' when deploying to Cloud Run

```

#(Optional) Run data ingestion to build the vector index:
python data/ingest.py



### Frontend Setup

```bash
cd frontend
npm install
```

### Running Locally

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\Activate.ps1
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:5173/`


## API Endpoints

Health Check
```http
GET /health
```

Response:
```json
{
"status": "healthy",
"version": "1.0.0"
}
```

Chat
Method & Route: POST /api/chat

Headers: Content-Type: application/json

Payload:
```json
{
"query": "What are Nike store hours?"
}
```

Response:
```json
{
"answer": "Nike Store is open from 10:00 AM to 10:00 PM daily.",
"sources": [
{
"text": "Store: Nike Store. Hours: 10:00 AM - 10:00 PM"
}
],
"latency_ms": 1200
}
```

## 📁 Project Structure

```text
rag-chatbot-enterprise/
├── backend/
│   ├── app.py                 # FastAPI application entry point
│   ├── config.py              # System configuration and settings
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (API Keys, Secrets)
│   ├── services/
│   │   └── rag_service.py     # Core RAG logic (LangChain/Embeddings)
│   └── data/
│       └── mall_data.json     # Mock dataset for mall inquiries
        └── ingest.py          # Script to populate ChromaDB vector store 
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   └── App.css            # Global application styles
│   └── package.json           # Node.js dependencies and scripts
├── .gitignore
└── README.md
```


## Deployment

Coming soon: Docker + Google Cloud Run deployment

## Future Improvements

- [ ] Docker + Cloud Run deployment
- [ ] Add BM25 hybrid search
- [ ] Implement cross-encoder reranking
- [ ] Add user feedback loop
- [ ] Multi-language support
- [ ] Advanced monitoring dashboard

## License

MIT

## Author

Gonzalo Morales - AI Engineer