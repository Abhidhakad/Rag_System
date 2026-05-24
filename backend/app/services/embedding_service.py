import logging
from functools import lru_cache

from openai import OpenAI

from app.core.config import config

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=config.OPENAI_API_KEY)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks using OpenAI's embedding model.
    Returns a list of float vectors. Raises on failure so callers can handle
    gracefully.
    """
    if not texts:
        return []

    try:
        client = get_openai_client()
        response = client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=texts,
        )
        embeddings = [item.embedding for item in response.data]
        logger.info(f"Generated {len(embeddings)} embeddings (model={config.EMBEDDING_MODEL})")
        return embeddings
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise


def generate_embedding(text: str) -> list[float]:
    return generate_embeddings([text])[0]
