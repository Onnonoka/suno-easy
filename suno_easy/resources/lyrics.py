from .._core.submit import submit_api_task
from .._core.tasks import Task, TaskKind, RECORD_INFO_ENDPOINTS
from ..models import Lyrics


class LyricsResource:
    """Resource manager for lyrics generation."""

    def __init__(self, client):
        self.client = client

    def get_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.LYRICS])

    def generate(
        self,
        prompt: str,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 120,
    ) -> Task[list[Lyrics]] | list[Lyrics]:
        payload = {"prompt": prompt}
        return submit_api_task(
            self.client,
            "/api/v1/lyrics",
            payload,
            TaskKind.LYRICS,
            Lyrics.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
        )

    def get(self, task_id: str) -> list[Lyrics]:
        return Lyrics.from_task_data(self.get_task(task_id))
