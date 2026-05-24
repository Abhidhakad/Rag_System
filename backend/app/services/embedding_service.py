import logging

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import config

logger = logging.getLogger(__name__)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks using Google's embedding model.
    Returns a list of float vectors. Raises on failure so callers can handle
    gracefully.
    """
    if not texts:
        return []

    try:
        embeddings_model = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)
        embeddings = embeddings_model.embed_documents(texts)
        logger.info(f"Generated {len(embeddings)} embeddings (model={config.EMBEDDING_MODEL})")
        return embeddings
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise


def generate_embedding(text: str) -> list[float]:
    return generate_embeddings([text])[0]
