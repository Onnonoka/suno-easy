#!/usr/bin/env python3
"""Smoke test: Suno Voice workflow (multi-step, can take several minutes).

Requires a publicly accessible vocal sample URL.

    export SUNO_API_KEY="your_key"
    export SUNO_VOICE_URL="https://example.com/vocal-sample.mp3"
    python examples/voice.py

Optional — skip step 2 (generate) if you only want the validation phrase:
    # stops after validate

Optional — run full workflow including custom voice creation:
    export SUNO_VERIFY_URL="https://example.com/verification-recording.mp3"
    python examples/voice.py
"""

import os

from _common import env_or_exit, make_client
from suno_easy import SingerSkillLevel, SunoAPIError, TaskFailed, VoiceLanguage


def main():
    voice_url = env_or_exit("SUNO_VOICE_URL")
    verify_url = os.environ.get("SUNO_VERIFY_URL")

    client = make_client()
    print("Step 1 — generate validation phrase…")

    try:
        info = client.voice.validate(
            voice_url,
            vocal_start_s=0,
            vocal_end_s=10,
            language=VoiceLanguage.EN,
            wait=True,
            timeout=600,
        )
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
        return
    except TaskFailed as exc:
        print(f"Validate failed: {exc.args[0]}")
        return

    print(f"  task_id:       {info.task_id}")
    print(f"  validate_info: {info.validate_info}")

    if not verify_url:
        print("\nRecord the phrase above, upload the audio, then re-run with:")
        print(f"  export SUNO_VERIFY_URL='https://…'")
        return

    print("\nStep 2 — generate custom voice…")
    try:
        voice = client.voice.generate(
            info.task_id,
            verify_url,
            voice_name="SDK Smoke Voice",
            singer_skill_level=SingerSkillLevel.BEGINNER,
            wait=True,
            timeout=600,
        )
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")
        return
    except TaskFailed as exc:
        print(f"Generate failed: {exc.args[0]}")
        return

    print(f"  voice_id: {voice.voice_id}")
    print(f"  status:   {voice.status}")

    check = client.voice.check(info.task_id)
    print(f"  available: {check.is_available}")


if __name__ == "__main__":
    main()
