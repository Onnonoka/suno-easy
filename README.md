# suno-easy 🎵

> [!IMPORTANT]
> **Disclaimer**: This is an unofficial, community-driven Python SDK wrapper for the Suno API (`sunoapi.org`). It is not affiliated with, endorsed, sponsored, or supported by Suno, Inc. or the official Suno AI platform.

`suno-easy` is a lightweight, modern, and fully-typed Python SDK for the Suno AI API ([docs.sunoapi.org](https://docs.sunoapi.org/)).

**📖 [Full documentation](docs/README.md)** — guides, resource reference, webhooks, models, API coverage.

---

## Features

- **Resource-oriented API** — eight endpoint groups on a single client:

  `client.music` · `client.lyrics` · `client.audio` · `client.persona` · `client.account` · `client.video` · `client.upload` · `client.voice`

- **100 % API coverage** — all documented Suno REST endpoints + webhook parsers ([details](docs/api-coverage.md))
- **Polling or webhooks** — `wait=True/False`, `Task` handles, `wait_until="stream"`
- **Typed models** — `Song`, `Lyrics`, `CustomVoice`, `UploadedFile`, … ([models](docs/models.md))
- **PEP 561** — ships `py.typed` for editor/type-checker support

---

## Installation

```bash
pip install suno-easy
```

Latest version: **0.2.0**

From source:

```bash
pip install -e .
```

Development:

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

Requires **Python ≥ 3.8**. Current version: **0.2.0**.

---

## Quickstart

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

print(songs[0].audio_url)
songs[0].download(f"{songs[0].title}.mp3")
```

```bash
export SUNO_API_KEY="your_api_key"
python examples/quickstart.py
```

More examples: [examples/README.md](examples/README.md) · [Voice workflow](docs/resources/voice.md) · [Webhooks](docs/webhooks.md)

---

## API coverage

The SDK covers **100 % of documented Suno REST endpoints** (34 total) and **all webhook callback types**.

Full tables: **[docs/api-coverage.md](docs/api-coverage.md)**

### File Upload — 3/3

Host: `https://sunoapiorg.redpandaai.co`

| Endpoint | SDK |
|---|---|
| `POST /api/file-url-upload` | `client.upload.upload_url()` |
| `POST /api/file-base64-upload` | `client.upload.upload_base64()` |
| `POST /api/file-stream-upload` | `client.upload.upload_stream()` |

### Suno API — 25/25

Host: `https://api.sunoapi.org`

| Endpoint | SDK |
|---|---|
| `POST /api/v1/generate` | `client.music.generate()` |
| `POST /api/v1/generate/extend` | `client.music.extend()` |
| `POST /api/v1/generate/mashup` | `client.music.mashup()` |
| `POST /api/v1/generate/replace-section` | `client.music.replace_section()` |
| `POST /api/v1/generate/sounds` | `client.music.generate_sounds()` |
| `POST /api/v1/generate/upload-cover` | `client.audio.cover()` |
| `POST /api/v1/generate/upload-extend` | `client.audio.extend()` |
| `POST /api/v1/generate/add-vocals` | `client.audio.add_vocals()` |
| `POST /api/v1/generate/add-instrumental` | `client.audio.add_instrumental()` |
| `POST /api/v1/generate/generate-persona` | `client.persona.create()` |
| `POST /api/v1/generate/get-timestamped-lyrics` | `client.lyrics.get_timestamped()` |
| `GET /api/v1/generate/credit` | `client.account.get_credits()` |
| `GET /api/v1/generate/record-info` | `client.music.get_task()` |
| `POST /api/v1/lyrics` | `client.lyrics.generate()` |
| `GET /api/v1/lyrics/record-info` | `client.lyrics.get()` / `get_task()` |
| `POST /api/v1/vocal-removal/generate` | `client.audio.separate_vocals()` |
| `GET /api/v1/vocal-removal/record-info` | `client.audio.get_separated_stems()` |
| `POST /api/v1/midi/generate` | `client.audio.generate_midi()` |
| `GET /api/v1/midi/record-info` | `client.audio.get_midi()` |
| `POST /api/v1/wav/generate` | `client.audio.convert_wav()` |
| `GET /api/v1/wav/record-info` | `client.audio.get_wav()` |
| `POST /api/v1/style/generate` | `client.audio.boost_style()` |
| `POST /api/v1/suno/cover/generate` | `client.audio.generate_cover_image()` |
| `GET /api/v1/suno/cover/record-info` | `client.audio.get_cover_image()` |
| `POST /api/v1/mp4/generate` | `client.video.create()` |
| `GET /api/v1/mp4/record-info` | `client.video.get()` |

### Suno Voice — 6/6

| Endpoint | SDK |
|---|---|
| `POST /api/v1/voice/validate` | `client.voice.validate()` |
| `GET /api/v1/voice/validate-info` | `client.voice.get_validate_info()` |
| `POST /api/v1/voice/generate` | `client.voice.generate()` |
| `GET /api/v1/voice/record-info` | `client.voice.get_record()` |
| `POST /api/v1/voice/regenerate` | `client.voice.regenerate()` |
| `POST /api/v1/voice/check-voice` | `client.voice.check()` |

### Webhook parsers

| Callback | Parser |
|---|---|
| Music / extend / mashup / sounds / … | `parse_music_webhook` |
| Lyrics | `parse_lyrics_webhook` |
| Cover image | `parse_cover_image_webhook` |
| Vocal separation | `parse_vocal_separation_webhook` |
| MIDI | `parse_midi_webhook` |
| WAV | `parse_wav_webhook` |
| Video | `parse_video_webhook` |
| Voice validate / regenerate | `parse_voice_validate_webhook` |
| Voice generate | `parse_voice_generate_webhook` |
| Auto-detect | `dispatch_webhook` |

---

## Documentation

| Guide | Link |
|---|---|
| Index | [docs/README.md](docs/README.md) |
| Getting started | [docs/getting-started.md](docs/getting-started.md) |
| Client & hosts | [docs/client.md](docs/client.md) |
| Tasks & polling | [docs/tasks-and-polling.md](docs/tasks-and-polling.md) |
| Webhooks | [docs/webhooks.md](docs/webhooks.md) |
| API coverage (full) | [docs/api-coverage.md](docs/api-coverage.md) |
| Models | [docs/models.md](docs/models.md) |
| Enums | [docs/enums.md](docs/enums.md) |
| Errors | [docs/errors.md](docs/errors.md) |
| Resources | [docs/resources/](docs/resources/) |

---

## Repository structure

```text
suno-easy/
├── suno_easy/           # SDK package
├── docs/                # Full documentation
├── tests/
├── examples/
├── .github/workflows/   # CI
└── pyproject.toml
```

---

## Breaking changes (since v0.1.0)

| Before | Now |
|---|---|
| `wait=False` returned `str` | Returns `Task` |
| `persona.create(music_id, name)` | `persona.create(task_id, audio_id, name, description, …)` |
| `music.remaster(...)` | Removed |
| `audio.separate_vocals(..., audio_id=None)` | `audio_id` required |
| No default callback URL | `DEFAULT_CALLBACK_URL` injected automatically |

---

## Roadmap

- [x] Phases 0–3: full API, voice webhooks, CI, `py.typed`, documentation
- [x] Examples per feature ([examples/](examples/README.md))
- [x] PyPI publish (v0.2.0)

---

## License

MIT License
