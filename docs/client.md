# Client configuration

## SunoClient

```python
from suno_easy import SunoClient, DEFAULT_CALLBACK_URL, DEFAULT_UPLOAD_BASE_URL

client = SunoClient(
    api_key="your_api_key",
    callback_url="https://yourdomain.com/suno/webhook",  # optional
    upload_base_url=DEFAULT_UPLOAD_BASE_URL,             # optional
)
```

| Parameter | Default | Purpose |
|---|---|---|
| `api_key` | required | Bearer token sent as `Authorization: Bearer …` |
| `callback_url` | `DEFAULT_CALLBACK_URL` | Injected as `callBackUrl` on async endpoints |
| `upload_base_url` | `DEFAULT_UPLOAD_BASE_URL` | Host for `client.upload.*` |

## API hosts

The SDK talks to **two separate hosts**:

| Host | Constant | Used for |
|---|---|---|
| `https://api.sunoapi.org` | (built into `SunoClient.BASE_URL`) | Music, lyrics, audio, persona, account, video, voice |
| `https://sunoapiorg.redpandaai.co` | `DEFAULT_UPLOAD_BASE_URL` | Temporary file upload (`client.upload.*`) |

Uploaded files are **automatically deleted after 3 days**.

## HTTP helpers

Low-level methods on `SunoClient` (used internally by resources):

| Method | Description |
|---|---|
| `post(url, json)` | POST JSON to main API; validates envelope `code == 200` |
| `get(url, params)` | GET from main API |
| `get_task_info(task_id, endpoint)` | Poll task status |
| `wait_task(task_id, endpoint, …)` | Poll until complete or failed |
| `apply_callback(payload, callback_url)` | Inject `callBackUrl` into a payload |
| `resolve_callback_url(callback_url)` | Per-call or client default callback URL |

## Resources

All high-level API access goes through resource attributes:

```python
client.music
client.lyrics
client.audio
client.persona
client.account
client.video
client.upload
client.voice
```

See the [resource reference](README.md#resources-api-reference).
