from dataclasses import dataclass


@dataclass
class StyleBoost:
    task_id: str | None
    result: str
    credits_consumed: float | None = None
    credits_remaining: float | None = None
    success_flag: str | None = None
    error_message: str | None = None

    @classmethod
    def from_api_data(cls, data: dict) -> "StyleBoost":
        return cls(
            task_id=data.get("taskId"),
            result=data.get("result", ""),
            credits_consumed=data.get("creditsConsumed"),
            credits_remaining=data.get("creditsRemaining"),
            success_flag=str(data.get("successFlag")) if data.get("successFlag") is not None else None,
            error_message=data.get("errorMessage"),
        )
