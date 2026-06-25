#!/usr/bin/env python3
"""Smoke test: instrumental music generation (blocking poll).

Usage:
    export SUNO_API_KEY="your_key"
    python examples/music.py

Optional — reuse IDs in other examples:
    export SUNO_TASK_ID="<task_id>"
    export SUNO_AUDIO_ID="<song id>"
"""

from _common import make_client
from suno_easy import ModelVersion, SunoAPIError, TaskFailed


def main():
    client = make_client()
    print("Generating instrumental track (wait=True, may take a few minutes)…")

    try:
        task = client.music.generate(
            prompt="",
            style="Ambient, Piano, Calm",
            title="SDK Smoke Test",
            model=ModelVersion.V4_5ALL,
            instrumental=True,
            wait=False,
        )
        print(f"Task ID: {task.task_id}")
        songs = task.wait(timeout=600)
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
        return
    except TaskFailed as exc:
        print(f"Task failed: {exc.args[0]}")
        return

    for song in songs:
        print(f"  id:         {song.id}")
        print(f"  title:      {song.title}")
        print(f"  audio_url:  {song.audio_url}")
        print(f"  stream_url: {song.stream_url}")

    if songs:
        print("\nReuse in other examples:")
        print(f"  export SUNO_TASK_ID={task.task_id!r}")
        print(f"  export SUNO_AUDIO_ID={songs[0].id!r}")


if __name__ == "__main__":
    main()
