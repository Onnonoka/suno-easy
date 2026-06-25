from dataclasses import dataclass


@dataclass
class Lyrics:
    text: str
    title: str
    status: str | None = None
    error_message: str | None = None

    @classmethod
    def from_task_data(cls, task_data: dict) -> list["Lyrics"]:
        response_data = task_data.get("response", {})
        lyrics_list = []
        if isinstance(response_data, dict):
            lyrics_list = response_data.get("data") or []
        if not lyrics_list:
            lyrics_list = task_data.get("data") or []

        return [cls.from_callback_item(lyric) for lyric in lyrics_list]

    @classmethod
    def from_callback_item(cls, item: dict) -> "Lyrics":
        return cls(
            text=item.get("text", ""),
            title=item.get("title", ""),
            status=item.get("status"),
            error_message=item.get("errorMessage") or item.get("error_message"),
        )
