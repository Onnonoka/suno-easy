class SunoError(Exception):
    """Base exception for all Suno Easy library errors."""
    pass


class TaskFailed(SunoError):
    """Raised when a task status is FAILED or has error messages."""
    def __init__(self, task_info: dict):
        self.task_info = task_info
        super().__init__(f"Task failed: {task_info.get('errorMessage') or task_info.get('errorMsg') or task_info}")


class SunoAPIError(SunoError):
    """Raised when the Suno API returns an HTTP error code."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"Suno API error ({status_code}): {message}")