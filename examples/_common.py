"""Shared helpers for suno-easy examples."""

from __future__ import annotations

import os
import sys

from suno_easy import SunoClient


def require_api_key() -> str:
    api_key = os.environ.get("SUNO_API_KEY")
    if not api_key:
        print("Error: set SUNO_API_KEY to run this example.", file=sys.stderr)
        sys.exit(1)
    return api_key


def make_client() -> SunoClient:
    callback_url = os.environ.get("SUNO_CALLBACK_URL")
    kwargs = {"api_key": require_api_key()}
    if callback_url:
        kwargs["callback_url"] = callback_url
    return SunoClient(**kwargs)


def env_or_exit(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Error: set {name} to run this example.", file=sys.stderr)
        sys.exit(1)
    return value
