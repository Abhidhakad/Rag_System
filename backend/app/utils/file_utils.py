import os
import uuid
from pathlib import Path

from app.core.config import config
from app.core.exceptions import FileValidationError


def validate_file(filename: str, size: int) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in config.ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"File type '{ext}' is not allowed. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
        )
    if size > config.max_upload_bytes:
        raise FileValidationError(
            f"File size exceeds {config.MAX_UPLOAD_SIZE_MB}MB limit"
        )


def save_upload(file_bytes: bytes, original_filename: str) -> str:
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)

    doc_id = str(uuid.uuid4())
    ext = Path(original_filename).suffix
    safe_name = f"{doc_id}{ext}"
    filepath = os.path.join(config.UPLOAD_DIR, safe_name)

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    return filepath, doc_id
