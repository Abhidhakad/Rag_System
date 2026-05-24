# RAG Document Q&A System

A production-ready Retrieval-Augmented Generation system for querying PDF documents using natural language. Built with FastAPI, ChromaDB, and OpenAI.

## Architecture

```
User Uploads PDF → FastAPI → Extract Text → Chunk → Embed → ChromaDB
                                                          ↓
User Asks Question → Embed Query → Semantic Search → Retrieve Chunks
                                                          ↓
                                              LLM Generates Answer + Citations
```

**Stack:**
- Backend: FastAPI (Python)
- Embeddings: OpenAI `text-embedding-3-small`
- Vector DB: ChromaDB (persistent)
- LLM: OpenAI GPT-4o-mini
- Frontend: React + Tailwind CSS

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Add your OPENAI_API_KEY
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at `http://localhost:5173`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | OpenAI API key (required) |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model name |
| `LLM_MODEL` | `gpt-4o-mini` | LLM model for answer generation |
| `LLM_TEMPERATURE` | `0.3` | LLM temperature (lower = more factual) |
| `LLM_MAX_TOKENS` | `1024` | Max tokens for responses |
| `CHROMA_PERSIST_DIR` | `chroma_db` | Vector DB storage path |
| `CHUNK_SIZE` | `1000` | Text chunk size |
| `CHUNK_OVERLAP` | `150` | Chunk overlap |
| `RETRIEVAL_TOP_K` | `4` | Number of chunks to retrieve |
| `MAX_UPLOAD_SIZE_MB` | `10` | Max upload file size |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Allowed CORS origins |

## API Endpoints

### `GET /api/health`
Health check with system info.

**Response:**
```json
{
  "success": true,
  "message": "Service is running",
  "data": {
    "app": "RAG Document Q&A",
    "version": "1.0.0",
    "documents_in_store": 3
  }
}
```

### `POST /api/documents/upload`
Upload and process a PDF document.

**Request:** `multipart/form-data` with `file` field.

**Response:**
```json
{
  "success": true,
  "message": "Document processed successfully",
  "data": {
    "filename": "report.pdf",
    "doc_id": "abc-123",
    "chunk_count": 24
  }
}
```

### `POST /api/chat/query`
Ask a question about uploaded documents.

**Request:**
```json
{
  "question": "What is the revenue in 2025?"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Answer generated",
  "data": {
    "answer": "According to the document, the revenue in 2025 was $12.4M...",
    "citations": [
      {
        "content": "The company reported revenue of $12.4M in 2025...",
        "chunk_index": 0,
        "score": 0.92
      }
    ]
  }
}
```

## Assumptions

- PDF is the primary document format (extensible to others)
- OpenAI is used for both embeddings and LLM (swapable via config)
- Documents are processed synchronously on upload
- ChromaDB runs embedded (no separate server needed)
- Queries are stateless (no conversation history)

## Future Improvements

- Support for more file types (DOCX, TXT, MD)
- Conversation memory / multi-turn chat
- Reranking stage for retrieval accuracy
- Hybrid search (dense + sparse embeddings)
- User authentication and multi-tenant collections
- Async document processing for large files
- Streaming LLM responses
- Document management (list, delete)
- Rate limiting and request validation
- Docker Compose setup
