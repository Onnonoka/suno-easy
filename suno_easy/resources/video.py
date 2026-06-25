from .._core.submit import submit_api_task
from .._core.tasks import Task, TaskKind, RECORD_INFO_ENDPOINTS
from ..models import MusicVideo


class VideoResource:
    """Resource manager for music video generation."""

    def __init__(self, client):
        self.client = client

    def get_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.VIDEO])

    def create(
        self,
        task_id: str,
        audio_id: str,
        author: str | None = None,
        domain_name: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 600,
    ) -> Task[MusicVideo] | MusicVideo:
        payload = {"taskId": task_id, "audioId": audio_id}
        if author is not None:
            payload["author"] = author
        if domain_name is not None:
            payload["domainName"] = domain_name
        return submit_api_task(
            self.client,
            "/api/v1/mp4/generate",
            payload,
            TaskKind.VIDEO,
            MusicVideo.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
        )

    def get(self, task_id: str) -> MusicVideo:
        return MusicVideo.from_task_data(self.get_task(task_id))
