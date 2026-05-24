import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import config
from app.core.exceptions import LLMError
from app.models.schemas import Citation
from app.services.embedding_service import generate_embedding
from app.services.vector_service import vector_store

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based ONLY on the provided document context.

Rules:
- Answer clearly and concisely using only the context below.
- If the answer cannot be found in the context, say "I cannot find an answer to that question in the provided documents."
- Do NOT make up information or use outside knowledge.
- Cite the relevant chunk(s) by number when referencing specific information.
- If the context is empty, tell the user no documents have been uploaded yet."""


def _build_context(hits: list[dict]) -> str:
    parts = []
    for i, hit in enumerate(hits):
        parts.append(f"[Chunk {i + 1}] (relevance: {hit['score']:.2f})\n{hit['content']}")
    return "\n\n".join(parts)


def answer_question(question: str) -> tuple[str, list[Citation]]:
    """
    Full RAG pipeline: embed query -> retrieve chunks -> generate answer.
    Returns (answer_text, citations_list).
    """
    query_embedding = generate_embedding(question)

    hits = vector_store.search(query_embedding, top_k=config.RETRIEVAL_TOP_K)

    if not hits:
        return "No relevant documents found. Please upload a document first.", []

    context = _build_context(hits)

    citations = [
        Citation(content=hit["content"], chunk_index=i, score=hit["score"])
        for i, hit in enumerate(hits)
    ]

    try:
        llm = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            max_output_tokens=config.LLM_MAX_TOKENS,
        )
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", f"Context:\n{context}\n\nQuestion: {question}"),
        ]
        response = llm.invoke(messages)
        answer = response.content.strip()
        logger.info("Generated answer for question")
        return answer, citations

    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise LLMError("Failed to generate answer from language model")
