#!/usr/bin/env python3
"""Smoke test: style boost (sync, no task).

Usage:
    export SUNO_API_KEY="your_key"
    python examples/audio_boost_style.py
"""

from _common import make_client
from suno_easy import SunoAPIError


def main():
    client = make_client()
    try:
        result = client.audio.boost_style("upbeat indie pop with jangly guitars and warm vocals")
        print(f"Enhanced style: {result.result}")
        if result.credits_remaining is not None:
            print(f"Credits remaining: {result.credits_remaining}")
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")


if __name__ == "__main__":
    main()
