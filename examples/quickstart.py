#!/usr/bin/env python3
"""Quickstart example for suno-easy."""

import os
from suno_easy import SunoClient, DEFAULT_CALLBACK_URL, SunoAPIError, parse_lyrics_webhook


def demo_webhook_parsing(task_id: str = "demo-task-id"):
    """Runs locally without an API key."""
    fake_callback = {
        "code": 200,
        "msg": "All generated successfully.",
        "data": {
            "callbackType": "complete",
            "taskId": task_id,
            "data": [
                {
                    "text": "[Verse]\nRed dust rising on the horizon",
                    "title": "Mars Bound",
                    "status": "complete",
                }
            ],
        },
    }
    event, lyrics = parse_lyrics_webhook(fake_callback)
    print(f"Webhook stage: {event.callback_type}, title: {lyrics[0].title}")


def main():
    api_key = os.environ.get("SUNO_API_KEY")
    has_api_key = bool(api_key)

    if not has_api_key:
        print("[!] SUNO_API_KEY not set — skipping live API call.")
        print("    Set SUNO_API_KEY to exercise client.lyrics.generate().")

    client = SunoClient(api_key=api_key or "placeholder")
    webhook_client = SunoClient(
        api_key=api_key or "placeholder",
        callback_url=os.environ.get("SUNO_CALLBACK_URL", "https://yourdomain.com/suno/webhook"),
    )

    print(f"Polling client callback: {client.callback_url}")
    print(f"Placeholder documented as: {DEFAULT_CALLBACK_URL}")
    print(f"Webhook client callback: {webhook_client.callback_url}")

    print("\n--- Webhook parsing demo (no API key required) ---")
    demo_webhook_parsing()

    if not has_api_key:
        return

    print("\n--- Live lyrics generation (async) ---")
    try:
        task = client.lyrics.generate(
            prompt="A song about embarking on a journey to Mars",
            wait=False,
        )
        print(f"Task ID: {task.task_id}")
        print("Poll with task.info() or task.wait()")
        demo_webhook_parsing(task.task_id)
    except SunoAPIError as e:
        print(f"API error ({e.status_code}): {e.message}")


if __name__ == "__main__":
    main()
