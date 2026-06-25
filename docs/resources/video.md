# client.video

Music video (MP4) generation.

## create

```python
video = client.video.create(
    task_id="music-task-id",
    audio_id="song-audio-id",
    author="Artist Name",       # optional
    domain_name="example.com",  # optional
    wait=True,
)

print(video.video_url)
video.download("music-video.mp4")
```

**Returns:** `MusicVideo` or `Task[MusicVideo]`  
**Endpoint:** `POST /api/v1/mp4/generate`

## get

```python
video = client.video.get("video-task-id")
```

Parses `GET /api/v1/mp4/record-info` into `MusicVideo`.

## get_task

```python
raw = client.video.get_task("video-task-id")
```

## Webhook

```python
from suno_easy import parse_video_webhook
event, video = parse_video_webhook(body)
```

## See also

- [Models](../models.md) — `MusicVideo`
