#!/usr/bin/env python3
"""Smoke test: account credits (sync, fast).

Usage:
    export SUNO_API_KEY="your_key"
    python examples/account.py
"""

from _common import make_client
from suno_easy import SunoAPIError


def main():
    client = make_client()
    try:
        credits = client.account.get_credits()
        print(f"Credits remaining: {credits.remaining}")
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")


if __name__ == "__main__":
    main()
