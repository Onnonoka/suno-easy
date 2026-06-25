# suno-easy 🎵

> [!IMPORTANT]
> **Disclaimer**: This is an unofficial, community-driven Python SDK wrapper for the Suno API (`sunoapi.org`). It is not affiliated with, endorsed, sponsored, or supported by Suno, Inc. or the official Suno AI platform.

`suno-easy` is a lightweight, modern, and fully-typed Python SDK for the Suno AI API ([docs.sunoapi.org](https://docs.sunoapi.org/)).

---

## Features

- **Resource-oriented API**: `client.music`, `client.lyrics`, `client.audio`, `client.persona`
- **Polling or webhooks**: `wait=True/False`, `Task` handles, and webhook parsers
- **Typed models**: `Song`, `Lyrics`, `Persona`, `SeparatedStems`, `MIDIData`, `CoverImage`
- **Built-in downloads**: streaming helpers on `Song` and `SeparatedStems`
- **API enums**: `ModelVersion`, `PersonaModel`, `VocalGender`, `SeparationMode`

---

## Repository Structure

```text
suno-easy/
├── suno_easy/
│   ├── __init__.py          # Public exports
│   ├── client.py            # SunoClient, HTTP, polling
│   ├── exceptions.py
│   ├── tasks.py             # Compatibility shim
│   ├── _core/               # Task, constants, payload helpers, enums
│   ├── models/              # Response dataclasses
│   ├── resources/           # API endpoint groups
│   └── webhooks/            # Callback payload parsers
├── tests/
│   ├── test_client.py
│   ├── test_core/
│   ├── test_models/
│   ├── test_resources/
│   └── test_webhooks/
├── examples/
│   └── quickstart.py
└── pyproject.toml
```

---

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e .
python -m unittest discover -s tests -v
```

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
# On your server: event, songs = parse_music_webhook(request.json)
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
from suno_easy import parse_music_webhook, parse_lyrics_webhook

# FastAPI / Flask handler pseudo-code
def handle_suno_callback(body: dict):
    if "audio_url" in str(body):
        event, songs = parse_music_webhook(body)
    else:
        event, lyrics = parse_lyrics_webhook(body)
    return event.callback_type
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

### Webhooks
- `parse_music_webhook`, `parse_lyrics_webhook`, `parse_cover_image_webhook`
- `parse_vocal_separation_webhook`, `parse_midi_webhook`
- `parse_wav_webhook`, `parse_video_webhook`
- `parse_webhook`, `dispatch_webhook`

### Public constants & enums
- `DEFAULT_CALLBACK_URL`
- `ModelVersion`, `PersonaModel`, `VocalGender`, `SeparationMode`
- `Task`, `TaskKind`, `RECORD_INFO_ENDPOINTS`
- `Credits`, `TimestampedLyrics`, `WavFile`, `MusicVideo`, `StyleBoost`

---

## Breaking changes (since initial release)

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

Run the full suite:

```bash
python -m unittest discover -s tests -v
```

Test layout:

| Path | Covers |
|---|---|
| `tests/test_client.py` | HTTP client, callback URL, polling helpers |
| `tests/test_core/` | `Task` handle |
| `tests/test_models/` | Dataclass parsing |
| `tests/test_resources/` | Payload construction per resource |
| `tests/test_webhooks/` | Callback payload parsers |

---

## Roadmap (Phase 3)

- File upload API (`client.upload.*`)
- Suno Voice API (`client.voice.*`)
- CI, `py.typed`, PyPI publish

---

## License

MIT License
