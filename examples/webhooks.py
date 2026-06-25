#!/usr/bin/env python3
"""Smoke test: webhook parsers (no API key required).

Usage:
    python examples/webhooks.py
"""

from suno_easy import (
    TaskFailed,
    dispatch_webhook,
    parse_lyrics_webhook,
    parse_music_webhook,
    parse_voice_generate_webhook,
    parse_voice_validate_webhook,
    parse_wav_webhook,
)


def demo(name: str, parser, payload: dict):
    print(f"\n--- {name} ---")
    try:
        event, result = parser(payload)
        print(f"  task_id: {event.task_id}")
        print(f"  result:  {result!r}")
    except TaskFailed as exc:
        print(f"  TaskFailed (expected for error payloads): {exc.args[0]}")


def main():
    demo(
        "music",
        parse_music_webhook,
        {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "t1",
                "data": [{"id": "s1", "title": "Test", "audio_url": "https://example.com/a.mp3"}],
            },
        },
    )

    demo(
        "lyrics",
        parse_lyrics_webhook,
        {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "t2",
                "data": [{"text": "[Verse]\nHello", "title": "Lyric"}],
            },
        },
    )

    demo(
        "voice validate",
        parse_voice_validate_webhook,
        {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v1",
                "validateInfo": "Sing this phrase clearly",
                "status": "wait_validating",
            },
        },
    )

    demo(
        "voice generate",
        parse_voice_generate_webhook,
        {
            "code": 200,
            "msg": "success",
            "data": {"taskId": "v2", "voiceId": "voice_abc", "status": "success"},
        },
    )

    demo(
        "wav",
        parse_wav_webhook,
        {
            "code": 200,
            "msg": "ok",
            "data": {"taskId": "w1", "audioWavUrl": "https://example.com/t.wav"},
        },
    )

    print("\n--- dispatch_webhook (auto-detect) ---")
    _, result = dispatch_webhook(
        {
            "code": 200,
            "msg": "success",
            "data": {"taskId": "v3", "voiceId": "voice_xyz", "status": "success"},
        }
    )
    print(f"  detected voice generate: {result!r}")

    print("\nAll webhook parser demos passed.")


if __name__ == "__main__":
    main()
