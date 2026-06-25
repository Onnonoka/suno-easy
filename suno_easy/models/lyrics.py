from dataclasses import dataclass, field


@dataclass
class AlignedWord:
    word: str
    start_s: float
    end_s: float
    success: bool | None = None
    palign: int | None = None


@dataclass
class TimestampedLyrics:
    aligned_words: list[AlignedWord] = field(default_factory=list)
    waveform_data: list[float] = field(default_factory=list)
    hoot_cer: float | None = None
    is_streamed: bool | None = None

    @classmethod
    def from_api_data(cls, data: dict) -> "TimestampedLyrics":
        words = []
        for item in data.get("alignedWords") or []:
            words.append(
                AlignedWord(
                    word=item.get("word", ""),
                    start_s=float(item.get("startS", 0)),
                    end_s=float(item.get("endS", 0)),
                    success=item.get("success"),
                    palign=item.get("palign"),
                )
            )
        return cls(
            aligned_words=words,
            waveform_data=list(data.get("waveformData") or []),
            hoot_cer=data.get("hootCer"),
            is_streamed=data.get("isStreamed"),
        )


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
