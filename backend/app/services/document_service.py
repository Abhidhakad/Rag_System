import logging
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.core.config import config
from app.core.exceptions import FileValidationError

logger = logging.getLogger(__name__)


def extract_text(filepath: str) -> str:
    """
    Extract text from a PDF file using pypdf.
    Falls back gracefully if a page fails.
    """
    reader = PdfReader(filepath)
    texts: list[str] = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text and text.strip():
                texts.append(text.strip())
        except Exception as e:
            logger.warning(f"Failed to extract text from page {i}: {e}")
            continue

    if not texts:
        raise FileValidationError("No extractable text found in the PDF")

    return "\n\n".join(texts)


def chunk_text(text: str) -> list[str]:
    """
    Chunk strategy: RecursiveCharacterTextSplitter with chunk_size ~1000 and
    overlap ~150. This balances semantic coherence (not splitting mid-sentence)
    with granularity for retrieval. Overlap prevents loss of context at
    chunk boundaries.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len,
    )

    chunks = splitter.split_text(text)
    logger.info(f"Split document into {len(chunks)} chunks (size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")
    return chunks
