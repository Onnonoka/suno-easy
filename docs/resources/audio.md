# client.audio

Audio upload workflows, processing, and enhancement.

## Upload-based generation

### cover

Transform an uploaded track into a new style (upload & cover).

```python
songs = client.audio.cover(
    upload_url="https://example.com/original.mp3",
    style="Jazz",
    title="Jazz Cover",
    prompt="Smooth jazz arrangement",
)
```

**Endpoint:** `POST /api/v1/generate/upload-cover`

### extend

Extend an uploaded audio file (upload & extend).

```python
songs = client.audio.extend(
    upload_url="https://example.com/track.mp3",
    continue_at=30,
    prompt="Continue the melody",
    style="Electronic",
    title="Extended",
)
```

**Endpoint:** `POST /api/v1/generate/upload-extend`

### add_vocals

Layer AI vocals on an instrumental.

Required: `upload_url`, `prompt`, `title`, `style`, `negative_tags`

```python
songs = client.audio.add_vocals(
    upload_url="https://example.com/instrumental.mp3",
    prompt="A love song about the stars",
    title="Starlight",
    style="Pop",
    negative_tags="rap, metal",
)
```

**Endpoint:** `POST /api/v1/generate/add-vocals`

### add_instrumental

Add instrumental backing to a vocal track.

Required: `upload_url`, `title`, `tags`, `negative_tags`

```python
songs = client.audio.add_instrumental(
    upload_url="https://example.com/vocals.mp3",
    title="With Backing",
    tags="Pop, Ballad",
    negative_tags="metal",
)
```

**Endpoint:** `POST /api/v1/generate/add-instrumental`

## Processing

### separate_vocals

```python
from suno_easy import SeparationMode

stems = client.audio.separate_vocals(
    task_id="music-task-id",
    audio_id="song-audio-id",
    mode=SeparationMode.SPLIT_STEM,
)
stems.download_vocal("vocals.mp3")
```

**Endpoint:** `POST /api/v1/vocal-removal/generate`

### convert_wav

```python
wav = client.audio.convert_wav("task-id", "audio-id", wait=True)
wav.download("track.wav")
```

**Endpoint:** `POST /api/v1/wav/generate`

### generate_midi

```python
midi = client.audio.generate_midi("task-id", "audio-id", wait=True)
```

**Endpoint:** `POST /api/v1/midi/generate`

### generate_cover_image

```python
cover = client.audio.generate_cover_image("task-id", "audio-id", wait=True)
print(cover.images)
```

**Endpoint:** `POST /api/v1/suno/cover/generate`

### boost_style

Synchronous — no task, no webhook.

```python
boost = client.audio.boost_style("upbeat indie pop with jangly guitars")
print(boost.result)
```

**Endpoint:** `POST /api/v1/style/generate`

## Result fetchers

| Method | Returns | Record-info endpoint |
|---|---|---|
| `get_wav(task_id)` | `WavFile` | `/api/v1/wav/record-info` |
| `get_separated_stems(task_id)` | `SeparatedStems` | `/api/v1/vocal-removal/record-info` |
| `get_midi(task_id)` | `MIDIData` | `/api/v1/midi/record-info` |
| `get_cover_image(task_id)` | `CoverImage` | `/api/v1/suno/cover/record-info` |
| `get_task(task_id)` | `dict` | `/api/v1/generate/record-info` |

## Webhooks

| Task | Parser |
|---|---|
| Vocal separation | `parse_vocal_separation_webhook` |
| MIDI | `parse_midi_webhook` |
| WAV | `parse_wav_webhook` |
| Cover image | `parse_cover_image_webhook` |
| Cover / extend / add vocals / add instrumental | `parse_music_webhook` |

## See also

- [client.upload](upload.md) — host files before using `upload_url`
- [Enums](../enums.md) — `SeparationMode`
