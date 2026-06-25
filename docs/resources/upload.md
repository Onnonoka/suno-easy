# client.upload

Temporary file upload API (separate host from main Suno API).

Files are **automatically deleted after 3 days**.

## Host

Default: `DEFAULT_UPLOAD_BASE_URL` → `https://sunoapiorg.redpandaai.co`

Override on the client:

```python
from suno_easy import SunoClient, DEFAULT_UPLOAD_BASE_URL

client = SunoClient(api_key="...", upload_base_url=DEFAULT_UPLOAD_BASE_URL)
```

## upload_url

Upload a file already hosted at a public HTTP(S) URL.

```python
uploaded = client.upload.upload_url(
    file_url="https://example.com/track.mp3",
    upload_path="audio/uploads",
    file_name="track.mp3",  # optional
)
print(uploaded.download_url)
```

**Endpoint:** `POST /api/file-url-upload`

## upload_base64

Best for small files (< 10 MB). Accepts raw Base64 or `data:…;base64,…` URLs.

```python
uploaded = client.upload.upload_base64(
    base64_data="iVBORw0KGgo…",
    upload_path="images/base64",
    file_name="cover.png",
)
```

**Endpoint:** `POST /api/file-base64-upload`

## upload_stream

Multipart upload from a local path or file-like object.

```python
# From path
uploaded = client.upload.upload_stream(
    "/path/to/track.mp3",
    upload_path="audio/stream",
)

# From file object
with open("track.mp3", "rb") as f:
    uploaded = client.upload.upload_stream(f, upload_path="audio/stream", file_name="track.mp3")
```

**Endpoint:** `POST /api/file-stream-upload`

## UploadedFile fields

| Field | Description |
|---|---|
| `file_name` | Stored filename |
| `file_path` | Path in temporary storage |
| `download_url` | Public URL to use in other Suno endpoints |
| `file_size` | Size in bytes |
| `mime_type` | MIME type |
| `uploaded_at` | ISO timestamp |

## Typical workflow

```python
# 1. Upload source audio
uploaded = client.upload.upload_stream("my-song.mp3", upload_path="audio/user")

# 2. Use download_url in generation
songs = client.audio.cover(
    upload_url=uploaded.download_url,
    style="Rock",
    title="Rock Version",
    prompt="Electric guitar cover",
)
```

## See also

- [client.audio](audio.md) — upload-based generation methods
- [API coverage](../api-coverage.md)
