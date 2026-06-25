from dataclasses import dataclass

import requests


@dataclass
class MusicVideo:
    video_url: str | None = None
    task_id: str | None = None
    music_id: str | None = None

    def download(self, path: str):
        if not self.video_url:
            raise ValueError("No video_url available")
        r = requests.get(self.video_url, stream=True)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

    @classmethod
    def from_task_data(cls, task_data: dict) -> "MusicVideo":
        response = task_data.get("response") or {}
        if not isinstance(response, dict):
            response = {}
        video_url = (
            response.get("videoUrl")
            or response.get("video_url")
            or task_data.get("videoUrl")
            or task_data.get("video_url")
        )
        return cls(
            video_url=video_url,
            task_id=task_data.get("taskId") or task_data.get("task_id"),
            music_id=task_data.get("musicId") or task_data.get("music_id"),
        )


@dataclass
class CoverImage:
    images: list[str]

    @classmethod
    def from_task_data(cls, task_data: dict) -> "CoverImage":
        response_data = task_data.get("response", {})
        images = []
        if isinstance(response_data, dict):
            images = response_data.get("images") or []
        if not images:
            images = task_data.get("images") or []
        return cls(images=images)
