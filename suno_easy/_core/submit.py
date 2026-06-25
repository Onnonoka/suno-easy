from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar

from .tasks import Task, TaskKind, submit_task

if TYPE_CHECKING:
    from ..client import SunoClient

T = TypeVar("T")


def submit_api_task(
    client: SunoClient,
    path: str,
    payload: dict,
    kind: TaskKind,
    parse: Callable[[dict], T],
    *,
    callback_url: str | None = None,
    wait: bool = True,
    timeout: int = 300,
    wait_until: str = "complete",
) -> Task[T] | T:
    """POST an async endpoint, inject callback URL, and return a Task or result."""
    client.apply_callback(payload, callback_url)
    response = client.post(path, payload)
    return submit_task(
        client,
        response["data"]["taskId"],
        kind,
        parse,
        wait=wait,
        timeout=timeout,
        wait_until=wait_until,
    )
