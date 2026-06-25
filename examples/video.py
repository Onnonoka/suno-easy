#!/usr/bin/env python3
"""Smoke test: music video generation (requires an existing Suno track).

Run examples/music.py first, then:

    export SUNO_API_KEY="your_key"
    export SUNO_TASK_ID="music_task_id"
    export SUNO_AUDIO_ID="song_audio_id"
    python examples/video.py
"""

from _common import env_or_exit, make_client
from suno_easy import SunoAPIError, TaskFailed


def main():
    task_id = env_or_exit("SUNO_TASK_ID")
    audio_id = env_or_exit("SUNO_AUDIO_ID")

    client = make_client()
    print(f"Creating music video (task={task_id}, audio={audio_id})…")

    try:
        video = client.video.create(task_id, audio_id, wait=True, timeout=600)
        print(f"  video_url: {video.video_url}")
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
    except TaskFailed as exc:
        print(f"Task failed: {exc.args[0]}")


if __name__ == "__main__":
    main()
