# suno-easy 🎵

> [!IMPORTANT]
> **Disclaimer**: This is an unofficial, community-driven Python SDK wrapper for the Suno API (`sunoapi.org`). It is not affiliated with, endorsed, sponsored, or supported by Suno, Inc. or the official Suno AI platform.

`suno-easy` is a lightweight, modern, and fully-typed Python SDK for the Suno AI API ([docs.sunoapi.org](https://docs.sunoapi.org/)).

---

## Features

- **Resource-oriented API** — eight endpoint groups on a single client:

  `client.music` · `client.lyrics` · `client.audio` · `client.persona` · `client.account` · `client.video` · `client.upload` · `client.voice`

- **Polling or webhooks** — `wait=True/False`, `Task` handles, `wait_until="stream"`, and webhook parsers
- **Typed models** — `Song`, `Lyrics`, `Persona`, `Credits`, `WavFile`, `MusicVideo`, `UploadedFile`, `CustomVoice`, …
- **Built-in downloads** — streaming helpers on `Song`, `WavFile`, `MusicVideo`, and `SeparatedStems`
- **API enums** — `ModelVersion`, `PersonaModel`, `VocalGender`, `SeparationMode`, `SingerSkillLevel`, `VoiceLanguage`
- **PEP 561** — ships `py.typed` for editor/type-checker support

---

## Repository Structure

```text
suno-easy/
├── suno_easy/
│   ├── __init__.py          # Public exports
│   ├── client.py            # SunoClient, HTTP, polling
│   ├── py.typed             # PEP 561 marker
│   ├── exceptions.py
│   ├── tasks.py             # Compatibility shim
│   ├── _core/               # Task, constants, payload helpers, enums
│   ├── models/              # Response dataclasses
│   ├── resources/           # account, audio, lyrics, music, persona,
│   │                        # upload, video, voice
│   └── webhooks/            # Callback payload parsers
├── tests/
│   ├── test_client.py
│   ├── test_core/
│   ├── test_models/
│   ├── test_resources/
│   └── test_webhooks/
├── examples/
│   └── quickstart.py
├── .github/workflows/       # CI (pytest on push / PR)
└── pyproject.toml
```

---

## Installation

```bash
pip install -e .
```

For development (includes pytest):

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

Requires **Python ≥ 3.8**. Current package version: **0.2.0**.

---

## Client configuration

```python
from suno_easy import SunoClient, DEFAULT_CALLBACK_URL, DEFAULT_UPLOAD_BASE_URL

client = SunoClient(
    api_key="your_api_key",
    callback_url="https://yourdomain.com/suno/webhook",  # optional
    upload_base_url=DEFAULT_UPLOAD_BASE_URL,             # optional override
)
```

| Parameter | Default | Purpose |
|---|---|---|
| `api_key` | — | Bearer token ([API key page](https://sunoapi.org/api-key)) |
| `callback_url` | `DEFAULT_CALLBACK_URL` | Webhook URL injected as `callBackUrl` on async endpoints |
| `upload_base_url` | `DEFAULT_UPLOAD_BASE_URL` | Host for temporary file uploads (separate from the main API) |

**Two API hosts**

| Host | Used for |
|---|---|
| `https://api.sunoapi.org` | Music, lyrics, audio, persona, account, video, voice |
| `https://sunoapiorg.redpandaai.co` | File upload (`client.upload.*`) — files expire after 3 days |

---

## Callback URL (polling vs webhooks)

The Suno API requires a `callBackUrl` on async endpoints. The SDK supports both workflows.

### Polling only (default)

No webhook server needed. The SDK sends a documented placeholder automatically:

```python
from suno_easy import SunoClient, DEFAULT_CALLBACK_URL

client = SunoClient(api_key="...")
print(DEFAULT_CALLBACK_URL)  # https://example.com/suno-callback
```

### Webhooks

Point to your own endpoint on the client or per call:

```python
client = SunoClient(
    api_key="...",
    callback_url="https://yourdomain.com/suno/webhook",
)

task = client.music.generate(..., wait=False)
# On your server: event, result = dispatch_webhook(request.json)
```

---

## Quickstart

### Run the example script

```bash
export SUNO_API_KEY="your_api_key"

# Optional: override webhook URL
export SUNO_CALLBACK_URL="https://yourdomain.com/suno/webhook"

python examples/quickstart.py
```

Without `SUNO_API_KEY`, the script still runs the local webhook parsing demo.

### Generate music (polling)

```python
from suno_easy import SunoClient, ModelVersion

client = SunoClient(api_key="your_api_key")

songs = client.music.generate(
    prompt="A peaceful acoustic guitar melody",
    style="Folk, Acoustic",
    title="Morning Breeze",
    model=ModelVersion.V4_5ALL,
    instrumental=True,
)

for song in songs:
    print(song.title, song.audio_url)
    song.download(f"{song.title}.mp3")
```

### Early stream URL (~30–40 s)

```python
songs = client.music.generate(
    prompt="...",
    style="Pop",
    title="Demo",
    wait_until="stream",
)
print(songs[0].stream_url)
```

### Async task handle

```python
task = client.music.generate(..., wait=False)
print(task.task_id)

status = task.info()   # manual polling
songs = task.wait()    # block until complete
```

### Check remaining credits

```python
credits = client.account.get_credits()
print(credits.remaining)
```

### Upload a file (temporary URL)

```python
uploaded = client.upload.upload_url(
    "https://example.com/my-track.mp3",
    upload_path="audio/uploads",
    file_name="track.mp3",
)
print(uploaded.download_url)  # use in other endpoints (expires in 3 days)
```

### Suno Voice workflow

```python
from suno_easy import VoiceLanguage, SingerSkillLevel

# 1. Generate a validation phrase from a vocal segment
info = client.voice.validate(
    voice_url="https://example.com/source-vocal.mp3",
    vocal_start_s=0,
    vocal_end_s=10,
    language=VoiceLanguage.EN,
)
print(info.validate_info)  # phrase the user must sing

# 2. Submit verification recording → custom voice
voice = client.voice.generate(
    info.task_id,
    verify_url="https://example.com/verification-recording.mp3",
    voice_name="Bright Pop",
    singer_skill_level=SingerSkillLevel.INTERMEDIATE,
)
print(voice.voice_id)

# 3. Confirm availability
check = client.voice.check(info.task_id)
print(check.is_available)
```

### Create a persona

```python
persona = client.persona.create(
    task_id="music_task_id",
    audio_id="song_audio_id",
    name="Bright Pop Voice",
    description="Upbeat pop vocals with clear articulation",
)
print(persona.persona_id)
```

### Separate vocals

```python
from suno_easy import SeparationMode

stems = client.audio.separate_vocals(
    task_id="music_task_id",
    audio_id="song_audio_id",
    mode=SeparationMode.SEPARATE_VOCAL,
)
stems.download_vocal("vocals.mp3")
```

### Handle a webhook on your server

```python
from suno_easy import dispatch_webhook, parse_music_webhook, parse_lyrics_webhook

def handle_suno_callback(body: dict):
    # Best-effort routing by payload shape
    event, result = dispatch_webhook(body)
    return event.callback_type

    # Or target a specific parser:
    # event, songs = parse_music_webhook(body)
    # event, lyrics = parse_lyrics_webhook(body)
```

---

## API Reference

### `client.music`
- `generate(...)`, `extend(...)`, `generate_instrumental(...)`
- `mashup(upload_urls, ...)`, `replace_section(...)`, `generate_sounds(...)`
- `get_task(task_id) -> dict`

Tuning parameters on `generate` / `extend` / `mashup`: `persona_id`, `persona_model`, `negative_tags`, `vocal_gender`, `style_weight`, `weirdness_constraint`, `audio_weight`.

### `client.lyrics`
- `generate(...) -> list[Lyrics] | Task`
- `get(task_id) -> list[Lyrics]`
- `get_timestamped(task_id, audio_id) -> TimestampedLyrics`
- `get_task(task_id) -> dict`

### `client.audio`
- `cover(...)`, `extend(...)`, `add_vocals(...)`, `add_instrumental(...)`
- `separate_vocals(task_id, audio_id, mode=...)`
- `convert_wav(task_id, audio_id, ...) -> WavFile | Task`
- `boost_style(content) -> StyleBoost`
- `generate_midi(...)`, `generate_cover_image(...)`
- `get_wav(...)`, `get_separated_stems(...)`, `get_midi(...)`, `get_cover_image(...)`

### `client.account`
- `get_credits() -> Credits`

### `client.video`
- `create(task_id, audio_id, ...) -> MusicVideo | Task`
- `get(task_id) -> MusicVideo`
- `get_task(task_id) -> dict`

### `client.persona`
- `create(task_id, audio_id, name, description, ...) -> Persona`

### `client.upload`
- `upload_url(file_url, upload_path, file_name=None) -> UploadedFile`
- `upload_base64(base64_data, upload_path, file_name=None) -> UploadedFile`
- `upload_stream(file, upload_path, file_name=None) -> UploadedFile`

Uses `DEFAULT_UPLOAD_BASE_URL` (not the main Suno API host). Uploaded files are temporary and auto-deleted after **3 days**.

### `client.voice`
- `validate(voice_url, vocal_start_s, vocal_end_s, ...) -> VoiceValidationInfo | Task`
- `get_validate_info(task_id) -> VoiceValidationInfo`
- `generate(task_id, verify_url, ...) -> CustomVoice | Task`
- `get_record(task_id) -> CustomVoice`
- `regenerate(task_id, callback_url=None) -> str` — note: upstream field is `calBackUrl`
- `check(task_id) -> VoiceCheck`

### Webhooks
- `parse_music_webhook`, `parse_lyrics_webhook`, `parse_cover_image_webhook`
- `parse_vocal_separation_webhook`, `parse_midi_webhook`
- `parse_wav_webhook`, `parse_video_webhook`
- `parse_webhook`, `dispatch_webhook`

### Public exports

**Constants:** `DEFAULT_CALLBACK_URL`, `DEFAULT_UPLOAD_BASE_URL`

**Enums:** `ModelVersion`, `PersonaModel`, `VocalGender`, `SeparationMode`, `SingerSkillLevel`, `VoiceLanguage`

**Task API:** `Task`, `TaskKind`, `RECORD_INFO_ENDPOINTS`

**Models:** `Song`, `Lyrics`, `AlignedWord`, `TimestampedLyrics`, `CoverImage`, `MusicVideo`, `SeparatedStems`, `WavFile`, `MIDIData`, `MIDINote`, `MIDIInstrument`, `Persona`, `Credits`, `StyleBoost`, `UploadedFile`, `VoiceValidationInfo`, `CustomVoice`, `VoiceCheck`

**Exceptions:** `SunoError`, `SunoAPIError`, `TaskFailed`

---

## Breaking changes (since v0.1.0)

| Before | Now |
|---|---|
| `wait=False` returned `str` | Returns `Task` (use `task.task_id` or `str(task)`) |
| `persona.create(music_id, name)` | `persona.create(task_id, audio_id, name, description, ...)` |
| `music.remaster(...)` | Removed (endpoint not in official API) |
| `audio.separate_vocals(..., audio_id=None)` | `audio_id` is required |
| `add_vocals` / `add_instrumental` | Several fields are now required (see API reference) |
| No default callback URL | `DEFAULT_CALLBACK_URL` injected automatically |

---

## Testing

Run the full suite locally:

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

CI runs the same suite on **Python 3.10** and **3.12** (see `.github/workflows/test.yml`).

| Path | Covers |
|---|---|
| `tests/test_client.py` | HTTP client, callback URL, polling helpers |
| `tests/test_core/` | `Task` handle, `TaskKind` endpoints |
| `tests/test_models/` | Dataclass parsing (`Song`, upload, voice, …) |
| `tests/test_resources/` | Payload construction per resource |
| `tests/test_webhooks/` | Callback payload parsers, `dispatch_webhook` |

---

## Roadmap

- [x] Phase 0–1: SDK architecture, tasks, webhooks
- [x] Phase 2: credits, timestamped lyrics, WAV, video, mashup, sounds
- [x] Phase 3: file upload API, Suno Voice API, CI, `py.typed`
- [ ] PyPI publish (v0.2.0)

---

## License

MIT License
