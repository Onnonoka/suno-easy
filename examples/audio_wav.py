#!/usr/bin/env python3
"""Smoke test: WAV conversion (requires an existing Suno track).

Run examples/music.py first, then:

    export SUNO_API_KEY="your_key"
    export SUNO_TASK_ID="music_task_id"
    export SUNO_AUDIO_ID="song_audio_id"
    python examples/audio_wav.py
"""

from _common import env_or_exit, make_client
from suno_easy import SunoAPIError, TaskFailed


def main():
    task_id = env_or_exit("SUNO_TASK_ID")
    audio_id = env_or_exit("SUNO_AUDIO_ID")

    client = make_client()
    print(f"Converting to WAV (task={task_id}, audio={audio_id})…")

    try:
        wav = client.audio.convert_wav(task_id, audio_id, wait=True, timeout=600)
        print(f"  wav_url: {wav.wav_url}")
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
    except TaskFailed as exc:
        print(f"Task failed: {exc.args[0]}")


if __name__ == "__main__":
    main()
