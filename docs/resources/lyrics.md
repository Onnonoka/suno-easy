# client.lyrics

Lyrics generation and timestamped lyrics retrieval.

## Methods

### generate

```python
from suno_easy import SunoClient

client = SunoClient(api_key="...")

# Blocking
lyrics = client.lyrics.generate(prompt="A song about Mars exploration")

# Async
task = client.lyrics.generate(prompt="...", wait=False)
lyrics = task.wait()
```

**Returns:** `list[Lyrics]` or `Task[list[Lyrics]]`  
**Endpoint:** `POST /api/v1/lyrics`

### get

Parse completed lyrics from task record.

```python
lyrics = client.lyrics.get("task-id")
```

Uses `GET /api/v1/lyrics/record-info` internally.

### get_timestamped

Word-level synchronized lyrics for playback UI.

```python
from suno_easy import TimestampedLyrics

result: TimestampedLyrics = client.lyrics.get_timestamped(
    task_id="music-task-id",
    audio_id="song-audio-id",
)

for word in result.aligned_words:
    print(word.word, word.start_s, word.end_s)
```

**Returns:** `TimestampedLyrics` (synchronous)  
**Endpoint:** `POST /api/v1/generate/get-timestamped-lyrics`

### get_task

```python
raw = client.lyrics.get_task("task-id")
```

## Webhook

```python
from suno_easy import parse_lyrics_webhook
event, lyrics = parse_lyrics_webhook(body)
```

## See also

- [Models](../models.md) — `Lyrics`, `TimestampedLyrics`, `AlignedWord`
