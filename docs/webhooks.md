# Webhooks

Async Suno endpoints accept a `callBackUrl`. When the task completes, Suno POSTs JSON to your server.

## Setup on the client

```python
client = SunoClient(
    api_key="...",
    callback_url="https://yourdomain.com/suno/webhook",
)

task = client.music.generate(..., wait=False)
# Handle result on your server when the callback arrives
```

Per-call override: pass `callback_url=` to any async method.

## Server handler (recommended)

Use `dispatch_webhook` for automatic routing by payload shape:

```python
from suno_easy import dispatch_webhook, TaskFailed

def handle_suno_post(body: dict) -> dict:
    try:
        event, result = dispatch_webhook(body)
        # result type depends on task: list[Song], VoiceValidationInfo, WavFile, …
        return {"ok": True, "task_id": event.task_id}
    except TaskFailed as exc:
        return {"ok": False, "error": str(exc)}
```

Always respond **HTTP 200** within **15 seconds** (Suno requirement).

## Targeted parsers

When you know the task type:

```python
from suno_easy import (
    parse_music_webhook,
    parse_lyrics_webhook,
    parse_wav_webhook,
    parse_video_webhook,
    parse_voice_validate_webhook,
    parse_voice_generate_webhook,
)

event, songs = parse_music_webhook(body)
event, lyrics = parse_lyrics_webhook(body)
event, wav = parse_wav_webhook(body)
event, video = parse_video_webhook(body)
event, info = parse_voice_validate_webhook(body)
event, voice = parse_voice_generate_webhook(body)
```

## WebhookEvent envelope

`parse_webhook(body)` returns normalized metadata:

```python
from suno_easy import parse_webhook

event = parse_webhook(body)
event.code          # 200 on success
event.message       # API msg field
event.task_id       # from data.taskId / data.task_id
event.callback_type # e.g. "complete", "error" (music/lyrics)
event.is_success
event.is_error
event.is_final      # complete or error stage
```

Voice callbacks use `code` + `data.status` instead of `callbackType`.

## Parser reference

| Parser | Success result | Raises `TaskFailed` when |
|---|---|---|
| `parse_music_webhook` | `list[Song]` | `callbackType == error` or `code >= 400` |
| `parse_lyrics_webhook` | `list[Lyrics]` | same |
| `parse_cover_image_webhook` | `CoverImage` | same |
| `parse_vocal_separation_webhook` | `SeparatedStems` | same |
| `parse_midi_webhook` | `MIDIData` | same |
| `parse_wav_webhook` | `WavFile` | same |
| `parse_video_webhook` | `MusicVideo` | same |
| `parse_voice_validate_webhook` | `VoiceValidationInfo` | `code >= 400` or status `fail` / `processing_validate_fail` |
| `parse_voice_generate_webhook` | `CustomVoice` | `code >= 400` or status `fail` |
| `parse_voice_regenerate_webhook` | `VoiceValidationInfo` | same as validate |

## dispatch_webhook routing logic

1. Lyrics — `data.data[0]` contains `"text"`
2. Music — `data.data[0]` contains `"audio_url"` / `"audioUrl"`
3. Voice generate — `data.voiceId` present
4. Voice validate — `data.validateInfo` or status `wait_validating`
5. WAV — `audioWavUrl` in response/data
6. Video — `videoUrl` in response/data
7. Fallback — raw `data` or `TaskFailed` on error envelope

## Flask example

```python
from flask import Flask, request, jsonify
from suno_easy import dispatch_webhook, TaskFailed

app = Flask(__name__)

@app.post("/suno/webhook")
def suno_webhook():
    try:
        event, result = dispatch_webhook(request.json)
        # persist result…
        return jsonify({"status": "received", "task_id": event.task_id}), 200
    except TaskFailed as exc:
        return jsonify({"status": "failed", "detail": str(exc)}), 200
```

## Polling-only mode

If you do not run a webhook server, use the default placeholder URL and poll with `task.wait()` or resource `get_*` methods. See [Tasks & polling](tasks-and-polling.md).
