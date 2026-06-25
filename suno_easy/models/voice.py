from dataclasses import dataclass


@dataclass
class VoiceValidationInfo:
    task_id: str
    validate_info: str | None = None
    status: str | None = None
    error_code: int | None = None
    error_message: str | None = None

    @classmethod
    def from_api_data(cls, data: dict) -> "VoiceValidationInfo":
        return cls(
            task_id=data.get("taskId") or data.get("task_id") or "",
            validate_info=data.get("validateInfo") or data.get("validate_info"),
            status=data.get("status"),
            error_code=data.get("errorCode") or data.get("error_code"),
            error_message=data.get("errorMessage") or data.get("error_message"),
        )


@dataclass
class CustomVoice:
    task_id: str
    voice_id: str | None = None
    status: str | None = None
    error_code: int | None = None
    error_message: str | None = None

    @classmethod
    def from_api_data(cls, data: dict) -> "CustomVoice":
        return cls(
            task_id=data.get("taskId") or data.get("task_id") or "",
            voice_id=data.get("voiceId") or data.get("voice_id"),
            status=data.get("status"),
            error_code=data.get("errorCode") or data.get("error_code"),
            error_message=data.get("errorMessage") or data.get("error_message"),
        )


@dataclass
class VoiceCheck:
    is_available: bool

    @classmethod
    def from_api_data(cls, data: dict) -> "VoiceCheck":
        return cls(is_available=bool(data.get("isAvailable") or data.get("is_available")))
