from pydantic import BaseModel


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | list | None = None


class UploadResponse(BaseModel):
    filename: str
    doc_id: str
    chunk_count: int


class Citation(BaseModel):
    content: str
    chunk_index: int
    score: float


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
