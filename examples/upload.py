#!/usr/bin/env python3
"""Smoke test: temporary file upload.

Usage:
    export SUNO_API_KEY="your_key"

    # Option A — upload a public URL you control:
    export SUNO_FILE_URL="https://example.com/sample.mp3"
    python examples/upload.py

    # Option B — no env var: uploads a tiny local test file via stream
    python examples/upload.py
"""

import os
import tempfile

from _common import make_client
from suno_easy import SunoAPIError


def main():
    client = make_client()
    file_url = os.environ.get("SUNO_FILE_URL")

    try:
        if file_url:
            print(f"Uploading from URL: {file_url}")
            uploaded = client.upload.upload_url(
                file_url,
                upload_path="suno-easy/smoke",
                file_name="sample.mp3",
            )
        else:
            print("No SUNO_FILE_URL — uploading tiny local file via stream…")
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                tmp.write(b"suno-easy upload smoke test")
                tmp_path = tmp.name
            uploaded = client.upload.upload_stream(
                tmp_path,
                upload_path="suno-easy/smoke",
                file_name="smoke-test.txt",
            )
            os.unlink(tmp_path)

        print(f"  download_url: {uploaded.download_url}")
        print(f"  file_name:    {uploaded.file_name}")
        print(f"  file_size:    {uploaded.file_size}")
        print(f"  expires:      ~3 days")
        print("\nReuse in audio.cover / voice.validate:")
        print(f"  export SUNO_FILE_URL={uploaded.download_url!r}")
    except SunoAPIError as exc:
        print(f"API error ({exc.status_code}): {exc.message}")


if __name__ == "__main__":
    main()
