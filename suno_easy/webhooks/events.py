from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class CallbackType(str, Enum):
    TEXT = "text"
    FIRST = "first"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class WebhookEvent:
    """Normalized webhook envelope sent by Suno to ``callBackUrl``."""

    code: int
    message: str
    callback_type: str
    task_id: str
    raw: dict[str, Any]

    @property
    def is_success(self) -> bool:
        return self.code == 200

    @property
    def is_error(self) -> bool:
        return self.callback_type == CallbackType.ERROR.value or self.code >= 400

    @property
    def is_final(self) -> bool:
        return self.callback_type in (
            CallbackType.COMPLETE.value,
            CallbackType.ERROR.value,
        )

    @property
    def is_partial(self) -> bool:
        return self.callback_type in (
            CallbackType.TEXT.value,
            CallbackType.FIRST.value,
        )
