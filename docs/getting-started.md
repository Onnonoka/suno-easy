# Getting started

## Requirements

- Python **≥ 3.8**
- A Suno API key from the [API key management page](https://sunoapi.org/api-key)

## Installation

From a clone of the repository:

```bash
pip install -e .
```

For development (includes pytest):

```bash
pip install -e ".[dev]"
```

## First request

```python
from suno_easy import SunoClient, ModelVersion

client = SunoClient(api_key="your_api_key")

songs = client.music.generate(
    prompt="A calm piano melody at sunset",
    style="Ambient, Piano",
    title="Golden Hour",
    model=ModelVersion.V4_5ALL,
    instrumental=True,
)

print(songs[0].audio_url)
```

## Environment variables

The example script uses:

| Variable | Purpose |
|---|---|
| `SUNO_API_KEY` | Bearer token for live API calls |
| `SUNO_CALLBACK_URL` | Optional webhook URL override |

```bash
export SUNO_API_KEY="your_api_key"
python examples/quickstart.py
```

## Example script

See **[examples/README.md](../examples/README.md)** for all smoke-test scripts.

```bash
export SUNO_API_KEY="your_api_key"
python examples/account.py      # fast check
python examples/webhooks.py     # no API key
python examples/music.py        # full generation
```

## Next steps

- [Client configuration](client.md) — callback URL, upload host
- [Tasks & polling](tasks-and-polling.md) — async workflows
- [API coverage](api-coverage.md) — full endpoint map
