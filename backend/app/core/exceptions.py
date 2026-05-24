class AppException(Exception):
    status_code: int = 500
    message: str = "Internal server error"

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class FileValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)


class EmbeddingError(AppException):
    def __init__(self, message: str = "Failed to generate embeddings"):
        super().__init__(message=message, status_code=500)


class RetrievalError(AppException):
    def __init__(self, message: str = "Failed to retrieve relevant documents"):
        super().__init__(message=message, status_code=500)


class LLMError(AppException):
    def __init__(self, message: str = "Failed to generate response from LLM"):
        super().__init__(message=message, status_code=500)
