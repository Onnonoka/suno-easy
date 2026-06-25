# Examples

Runnable smoke tests for the SDK. All live examples require:

```bash
export SUNO_API_KEY="your_api_key"
```

Optional:

```bash
export SUNO_CALLBACK_URL="https://yourdomain.com/suno/webhook"
```

## No API key needed

| Script | What it tests |
|---|---|
| [webhooks.py](webhooks.py) | Webhook parsers (`parse_*`, `dispatch_webhook`) |
| [quickstart.py](quickstart.py) | Webhook demo + optional live lyrics task |

## Quick live checks (start here)

| Script | What it tests | Typical duration |
|---|---|---|
| [account.py](account.py) | `client.account.get_credits()` | < 1 s |
| [audio_boost_style.py](audio_boost_style.py) | `client.audio.boost_style()` | < 5 s |
| [upload.py](upload.py) | `client.upload.*` | < 5 s |

## Generation (uses credits)

| Script | What it tests | Notes |
|---|---|---|
| [lyrics.py](lyrics.py) | `client.lyrics.generate()` | ~1–2 min |
| [music.py](music.py) | `client.music.generate()` | ~2–5 min |

## Chained examples (need IDs from a prior run)

Run [music.py](music.py) first, then set:

```bash
export SUNO_TASK_ID="…"    # from task.info() or API dashboard
export SUNO_AUDIO_ID="…"   # printed by music.py (song id)
```

| Script | What it tests |
|---|---|
| [audio_wav.py](audio_wav.py) | `client.audio.convert_wav()` |
| [video.py](video.py) | `client.video.create()` |

## Voice workflow

```bash
export SUNO_VOICE_URL="https://example.com/vocal-sample.mp3"
python examples/voice.py

# After recording the validation phrase:
export SUNO_VERIFY_URL="https://example.com/verification.mp3"
python examples/voice.py
```

## Suggested smoke-test order

```bash
python examples/webhooks.py          # local, no key
python examples/account.py           # verify key works
python examples/audio_boost_style.py
python examples/upload.py
python examples/lyrics.py
python examples/music.py             # save SUNO_AUDIO_ID for chained tests
# optional:
python examples/audio_wav.py
python examples/video.py
python examples/voice.py
```

See [docs/](../docs/README.md) for full API reference.
