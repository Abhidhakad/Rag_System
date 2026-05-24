import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import config
from app.models.schemas import APIResponse, QueryRequest, QueryResponse
from app.services.document_service import chunk_text, extract_text
from app.services.embedding_service import generate_embeddings
from app.services.rag_service import answer_question
from app.services.vector_service import vector_store
from app.utils.file_utils import save_upload, validate_file

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health_check():
    return APIResponse(
        success=True,
        message="Service is running",
        data={
            "app": config.APP_NAME,
            "version": config.APP_VERSION,
            "documents_in_store": vector_store.count(),
        },
    )


@router.post("/documents/upload", response_model=APIResponse)
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    validate_file(file.filename or "unknown.pdf", len(contents))

    filepath, doc_id = save_upload(contents, file.filename or "document.pdf")

    logger.info(f"Processing uploaded file: {file.filename} (id={doc_id})")

    text = extract_text(filepath)
    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    metadata = [{"doc_id": doc_id, "filename": file.filename, "chunk_index": i} for i in range(len(chunks))]
    vector_store.add_chunks(chunks, embeddings, metadata)

    logger.info(f"Document '{file.filename}' processed: {len(chunks)} chunks stored")

    return APIResponse(
        success=True,
        message="Document processed successfully",
        data={
            "filename": file.filename,
            "doc_id": doc_id,
            "chunk_count": len(chunks),
        },
    )


@router.post("/chat/query", response_model=APIResponse)
async def query_documents(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"Processing query: '{req.question[:80]}...'")

    answer, citations = answer_question(req.question)

    return APIResponse(
        success=True,
        message="Answer generated",
        data=QueryResponse(answer=answer, citations=citations).model_dump(),
    )
