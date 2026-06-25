from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable, Generic, Literal, TypeVar

if TYPE_CHECKING:
    from ..client import SunoClient

T = TypeVar("T")
WaitUntil = Literal["complete", "stream"]


class TaskKind(str, Enum):
    """Identifies the async task type and its record-info endpoint."""

    MUSIC = "music"
    LYRICS = "lyrics"
    COVER_IMAGE = "cover_image"
    VOCAL_SEPARATION = "vocal_separation"
    MIDI = "midi"


RECORD_INFO_ENDPOINTS: dict[TaskKind, str] = {
    TaskKind.MUSIC: "/api/v1/generate/record-info",
    TaskKind.LYRICS: "/api/v1/lyrics/record-info",
    TaskKind.COVER_IMAGE: "/api/v1/suno/cover/record-info",
    TaskKind.VOCAL_SEPARATION: "/api/v1/vocal-removal/record-info",
    TaskKind.MIDI: "/api/v1/midi/record-info",
}


@dataclass
class Task(Generic[T]):
    """Handle for an async Suno API task."""

    task_id: str
    kind: TaskKind
    _client: SunoClient
    _parse: Callable[[dict], T]
    record_info_endpoint: str | None = None

    def __post_init__(self) -> None:
        if self.record_info_endpoint is None:
            self.record_info_endpoint = RECORD_INFO_ENDPOINTS[self.kind]

    def info(self) -> dict:
        """Fetch the current task state from the API (manual polling)."""
        return self._client.get_task_info(self.task_id, self.record_info_endpoint)

    def wait(
        self,
        timeout: int = 300,
        poll_interval: int = 3,
        wait_until: WaitUntil = "complete",
    ) -> T:
        """Poll until the task reaches the requested stage and return the parsed result."""
        task_data = self._client.wait_task(
            self.task_id,
            endpoint=self.record_info_endpoint,
            timeout=timeout,
            poll_interval=poll_interval,
            wait_until=wait_until,
        )
        return self._parse(task_data)

    def __str__(self) -> str:
        return self.task_id

    def __repr__(self) -> str:
        return f"Task(task_id={self.task_id!r}, kind={self.kind.value!r})"


def submit_task(
    client: SunoClient,
    task_id: str,
    kind: TaskKind,
    parse: Callable[[dict], T],
    *,
    wait: bool = True,
    timeout: int = 300,
    endpoint: str | None = None,
    wait_until: WaitUntil = "complete",
) -> Task[T] | T:
    """Create a :class:`Task` and optionally block until completion."""
    task = Task(
        task_id=task_id,
        kind=kind,
        _client=client,
        _parse=parse,
        record_info_endpoint=endpoint or RECORD_INFO_ENDPOINTS[kind],
    )
    if wait:
        return task.wait(timeout=timeout, wait_until=wait_until)
    return task
