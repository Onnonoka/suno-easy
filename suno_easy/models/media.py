from dataclasses import dataclass


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
