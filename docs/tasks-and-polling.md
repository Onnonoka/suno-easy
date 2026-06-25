# Tasks & polling

Most Suno endpoints are **async**: they return a `taskId` and complete later via polling or webhook.

## Blocking vs non-blocking

```python
# Blocking — polls until done, returns parsed result
songs = client.music.generate(..., wait=True)

# Non-blocking — returns a Task handle immediately
task = client.music.generate(..., wait=False)
print(task.task_id)

songs = task.wait()       # block later
raw = task.info()         # single poll, raw API dict
```

`wait=False` returns a `Task` object (not a bare string).

## wait_until

For music generation, you can receive stream URLs early:

```python
songs = client.music.generate(
    ...,
    wait_until="stream",  # ~30–40 s instead of full completion
)
print(songs[0].stream_url)
```

Values: `"complete"` (default) or `"stream"`.

## Task kinds

Each async endpoint maps to a `TaskKind` and a record-info URL:

| TaskKind | Record-info endpoint |
|---|---|
| `MUSIC` | `/api/v1/generate/record-info` |
| `LYRICS` | `/api/v1/lyrics/record-info` |
| `COVER_IMAGE` | `/api/v1/suno/cover/record-info` |
| `VOCAL_SEPARATION` | `/api/v1/vocal-removal/record-info` |
| `MIDI` | `/api/v1/midi/record-info` |
| `WAV` | `/api/v1/wav/record-info` |
| `VIDEO` | `/api/v1/mp4/record-info` |
| `VOICE_VALIDATE` | `/api/v1/voice/validate-info` |
| `VOICE` | `/api/v1/voice/record-info` |

Access constants via:

```python
from suno_easy import TaskKind, RECORD_INFO_ENDPOINTS
```

## Callback URL without a server

If you only poll, the SDK injects a documented placeholder:

```python
from suno_easy import DEFAULT_CALLBACK_URL
# https://example.com/suno-callback
```

No webhook server is required for polling-only workflows.

## Voice polling

`client.voice` uses custom wait logic internally when `wait=True`:

- **validate** — waits until `status == wait_validating` and `validateInfo` is present
- **generate** — waits until `status == success` and `voiceId` is present

On failure, `TaskFailed` is raised with `errorMessage` from the API.

## Timeouts

Most methods accept `timeout` (seconds) and `poll_interval` (seconds between polls). Defaults vary by resource (e.g. voice generate defaults to 600 s).
