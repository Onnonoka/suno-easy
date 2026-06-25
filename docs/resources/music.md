# client.music

Music generation and manipulation.

## Methods

### generate

Create music from a text prompt.

```python
from suno_easy import SunoClient, ModelVersion, VocalGender, PersonaModel

songs = client.music.generate(
    prompt="[Verse]\nWalking through the city lights",
    style="Synthpop, 80s",
    title="Neon Dreams",
    model=ModelVersion.V4_5ALL,
    instrumental=False,
    custom_mode=True,
    negative_tags="metal, rap",
    vocal_gender=VocalGender.FEMALE,
    persona_id="persona-id",
    persona_model=PersonaModel.STYLE,
    style_weight=0.7,
    weirdness_constraint=0.5,
    audio_weight=0.5,
    wait=True,
    wait_until="complete",  # or "stream"
)
```

**Returns:** `list[Song]` or `Task[list[Song]]`  
**Endpoint:** `POST /api/v1/generate`

### extend

Extend an existing Suno track.

```python
songs = client.music.extend(
    audio_id="song-audio-id",
    continue_at=60,
    prompt="Continue the chorus",
    style="Pop",
    title="Extended Mix",
)
```

**Endpoint:** `POST /api/v1/generate/extend`

### generate_instrumental

Shortcut for `generate(..., instrumental=True)`.

### mashup

Blend two or more audio URLs.

```python
songs = client.music.mashup(
    upload_urls=["https://example.com/a.mp3", "https://example.com/b.mp3"],
    style="Electronic",
    title="Mashup",
)
```

**Endpoint:** `POST /api/v1/generate/mashup`

### replace_section

Replace a time segment within a track.

```python
songs = client.music.replace_section(
    task_id="task-id",
    audio_id="audio-id",
    prompt="New chorus lyrics",
    tags="Pop",
    title="Remixed",
    full_lyrics="[Verse] …\n[Chorus] …",
    infill_start_s=30.0,
    infill_end_s=45.0,
    negative_tags="metal",
)
```

**Endpoint:** `POST /api/v1/generate/replace-section`

### generate_sounds

Generate sound effects / loops (defaults to model V5).

```python
songs = client.music.generate_sounds(
    prompt="ambient pad texture",
    sound_loop=True,
    sound_tempo=120,
    sound_key="C",
    grab_lyrics=True,
)
```

**Endpoint:** `POST /api/v1/generate/sounds`

### get_task

Fetch raw task JSON from the API.

```python
raw = client.music.get_task("task-id")
```

**Endpoint:** `GET /api/v1/generate/record-info`

## Webhook

Music-shaped callbacks (generate, extend, mashup, sounds, replace, etc.):

```python
from suno_easy import parse_music_webhook
event, songs = parse_music_webhook(request.json)
```

## See also

- [Enums](../enums.md) — `ModelVersion`, `VocalGender`
- [Models](../models.md) — `Song`
- [API coverage](../api-coverage.md)
