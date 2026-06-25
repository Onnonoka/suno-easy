#!/usr/bin/env python3
"""Smoke test: lyrics generation (async task + wait).

Usage:
    export SUNO_API_KEY="your_key"
    python examples/lyrics.py
"""

from _common import make_client
from suno_easy import SunoAPIError, TaskFailed


def main():
    client = make_client()
    print("Generating lyrics…")

    try:
        task = client.lyrics.generate(
            prompt="A short song about testing a Python SDK under starlight",
            wait=False,
        )
        print(f"Task ID: {task.task_id}")
        lyrics = task.wait(timeout=120)
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
        return
    except TaskFailed as exc:
        print(f"Task failed: {exc.args[0]}")
        return

    for item in lyrics:
        print(f"\nTitle: {item.title}")
        print(item.text[:500])
        if len(item.text) > 500:
            print("…")


if __name__ == "__main__":
    main()
