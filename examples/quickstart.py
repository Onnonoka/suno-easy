#!/usr/bin/env python3
"""
Quickstart example for suno-easy.
This script demonstrates how to initialize the SunoClient and run basic actions
such as generating music, generating lyrics, and separating stems.

Make sure you have installed the requirements:
    pip install -e .
Or run it locally if suno_easy is in your python path.
"""

import os
from suno_easy import SunoClient, SunoError


def main():
    # 1. Initialize client using an API key from environment variables
    # (or replace with your actual API key)
    api_key = os.environ.get("SUNO_API_KEY", "your_suno_api_key_here")
    if api_key == "your_suno_api_key_here":
        print("[!] Using placeholder API key. Set SUNO_API_KEY env var for actual calls.")

    client = SunoClient(api_key=api_key)
    print("SunoClient initialized successfully.")

    # 2. Example: Generate lyrics (using dry-run info, or wrapped in try-except)
    print("\n--- Generating Lyrics ---")
    try:
        # We set wait=False for demonstration to avoid blocking and show async flow
        print("Starting lyric generation (non-blocking/async)...")
        task_id = client.lyrics.generate(
            prompt="A song about embarking on a journey to Mars",
            wait=False
        )
        print(f"Lyrics generation started! Task ID: {task_id}")
        print("In a real application, you would poll client.music.get_task_info(task_id)")
        print("or wait for a webhook callback.")

    except SunoError as e:
        print(f"An error occurred during the Suno API call: {e}")


if __name__ == "__main__":
    main()
