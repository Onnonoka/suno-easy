# Errors

```python
from suno_easy import SunoAPIError, TaskFailed, SunoError
```

## SunoAPIError

Raised on HTTP failures or Suno envelope errors (`code != 200` in JSON body, even when HTTP status is 200).

```python
try:
    client.music.generate(...)
except SunoAPIError as exc:
    print(exc.status_code)   # HTTP or envelope code
    print(exc.message)       # API msg / response text
    print(exc.response_text) # raw body
```

Common causes: invalid API key (401), insufficient credits, malformed payload.

## TaskFailed

Raised when polling detects a failed async task, or when a webhook parser receives an error callback.

```python
try:
    songs = task.wait()
except TaskFailed as exc:
    data = exc.args[0]  # dict with status, errorMessage, taskId, …
```

Also raised by webhook parsers on error payloads:

```python
try:
    parse_voice_validate_webhook(body)
except TaskFailed:
    ...
```

## SunoError

Base class for SDK errors.

## TimeoutError

Standard Python `TimeoutError` when `wait_task` or voice polling exceeds `timeout`.

## Recommended pattern

```python
from suno_easy import SunoClient, SunoAPIError, TaskFailed

client = SunoClient(api_key="...")

try:
    songs = client.music.generate(prompt="...", style="Pop", title="Demo")
except SunoAPIError as exc:
    # Request rejected by API
    ...
except TaskFailed as exc:
    # Task started but failed during generation
    ...
except TimeoutError:
    # Polling timed out
    ...
```
