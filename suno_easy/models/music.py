from dataclasses import dataclass

import requests


@dataclass
class Song:
    id: str
    title: str
    audio_url: str | None = None
    stream_url: str | None = None
    source_audio_url: str | None = None
    source_stream_url: str | None = None
    image_url: str | None = None
    source_image_url: str | None = None
    prompt: str | None = None
    tags: str | None = None
    duration: float | None = None
    model_name: str | None = None
    create_time: str | None = None

    def download(self, path: str):
        if not self.audio_url:
            raise ValueError("No audio_url available")

        r = requests.get(self.audio_url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

    def download_image(self, path: str):
        if not self.image_url:
            raise ValueError("No image_url available")

        r = requests.get(self.image_url)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)

    @classmethod
    def from_task_data(cls, task_data: dict) -> list["Song"]:
        response_data = task_data.get("response", {})
        songs_list = []
        if isinstance(response_data, dict):
            songs_list = response_data.get("sunoData") or response_data.get("songs") or []
        if not songs_list:
            songs_list = task_data.get("songs") or task_data.get("sunoData") or []

        return [cls.from_callback_item(song) for song in songs_list]

    @classmethod
    def from_callback_item(cls, item: dict) -> "Song":
        """Build a Song from polling (camelCase) or webhook (snake_case) payloads."""
        return cls(
            id=item["id"],
            title=item.get("title", ""),
            audio_url=item.get("audioUrl") or item.get("audio_url"),
            stream_url=item.get("streamAudioUrl") or item.get("stream_audio_url"),
            source_audio_url=item.get("sourceAudioUrl") or item.get("source_audio_url"),
            source_stream_url=item.get("sourceStreamAudioUrl") or item.get("source_stream_audio_url"),
            image_url=item.get("imageUrl") or item.get("image_url"),
            source_image_url=item.get("sourceImageUrl") or item.get("source_image_url"),
            prompt=item.get("prompt"),
            tags=item.get("tags"),
            duration=item.get("duration"),
            model_name=item.get("modelName") or item.get("model_name"),
            create_time=item.get("createTime") or item.get("create_time"),
        )
