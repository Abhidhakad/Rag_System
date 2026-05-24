import logging
from typing import Any

import chromadb
from chromadb.config import Settings

from app.core.config import config
from app.core.exceptions import RetrievalError

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Wraps ChromaDB with persistent storage and a clean interface.
    Each collection is isolated by name for multi-doc support.
    """

    def __init__(self):
        self._client = chromadb.PersistentClient(
            path=config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=config.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = metadata or [{} for _ in chunks]

        self._collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.info(f"Added {len(chunks)} chunks to collection '{config.CHROMA_COLLECTION_NAME}'")
        return ids

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[dict[str, Any]]:
        try:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
            )
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise RetrievalError("Failed to query vector store")

        if not results["ids"] or not results["ids"][0]:
            return []

        documents = results["documents"][0] if results.get("documents") else []
        distances = results["distances"][0] if results.get("distances") else []
        metadatas = results["metadatas"][0] if results.get("metadatas") else []
        ids = results["ids"][0]

        hits = []
        for i in range(len(ids)):
            hits.append({
                "id": ids[i],
                "content": documents[i] if i < len(documents) else "",
                "score": 1.0 - distances[i] if i < len(distances) else 0.0,
                "metadata": metadatas[i] if i < len(metadatas) else {},
            })

        return hits

    def count(self) -> int:
        return self._collection.count()


vector_store = VectorStore()
