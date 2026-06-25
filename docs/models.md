# Models

All response types are `@dataclass` instances with `from_api_data` / `from_task_data` / `from_callback_item` constructors.

## Music

### Song

Returned by music generation, extension, mashup, cover, add vocals/instrumental, sounds, replace section.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Suno track ID |
| `title` | `str` | Track title |
| `audio_url` | `str \| None` | Final MP3 URL |
| `stream_url` | `str \| None` | Early stream URL |
| `source_stream_url` | `str \| None` | Original stream URL |
| `image_url` | `str \| None` | Cover art URL |
| `prompt` | `str \| None` | Lyrics / prompt text |
| `tags` | `str \| None` | Style tags |
| `duration` | `float \| None` | Duration in seconds |
| `model_name` | `str \| None` | Model used |

Methods: `download(path)`, `download_image(path)`

## Lyrics

### Lyrics

| Field | Type |
|---|---|
| `text` | `str` |
| `title` | `str` |
| `status` | `str \| None` |
| `error_message` | `str \| None` |

### TimestampedLyrics

| Field | Type |
|---|---|
| `aligned_words` | `list[AlignedWord]` |
| `waveform_data` | `list[float]` |
| `hoot_cer` | `float \| None` |
| `is_streamed` | `bool \| None` |

### AlignedWord

| Field | Type |
|---|---|
| `word` | `str` |
| `start_s` | `float` |
| `end_s` | `float` |
| `success` | `bool \| None` |
| `palign` | `int \| None` |

## Audio processing

### SeparatedStems

Vocal separation result. Methods: `download_vocal(path)`, `download_instrumental(path)`, …

### WavFile

| Field | Type |
|---|---|
| `wav_url` | `str \| None` |
| `task_id` | `str \| None` |

Method: `download(path)`

### MIDIData

MIDI note data with nested `MIDINote` and `MIDIInstrument`.

### CoverImage

| Field | Type |
|---|---|
| `images` | `list[str]` |

### StyleBoost

Synchronous style enhancement result.

| Field | Type |
|---|---|
| `result` | `str` |
| `task_id` | `str \| None` |
| `credits_consumed` | `float \| None` |
| `credits_remaining` | `float \| None` |

## Persona & account

### Persona

| Field | Type |
|---|---|
| `persona_id` | `str` |
| `name` | `str \| None` |
| `description` | `str \| None` |

### Credits

| Field | Type |
|---|---|
| `remaining` | `int` |

## Video

### MusicVideo

| Field | Type |
|---|---|
| `video_url` | `str \| None` |
| `task_id` | `str \| None` |
| `music_id` | `str \| None` |

Method: `download(path)`

## Upload

### UploadedFile

Temporary upload result (3-day retention).

| Field | Type |
|---|---|
| `file_name` | `str` |
| `file_path` | `str` |
| `download_url` | `str` |
| `file_size` | `int` |
| `mime_type` | `str` |
| `uploaded_at` | `str` |

## Voice

### VoiceValidationInfo

| Field | Type |
|---|---|
| `task_id` | `str` |
| `validate_info` | `str \| None` | Phrase user must sing |
| `status` | `str \| None` |
| `error_code` | `int \| None` |
| `error_message` | `str \| None` |

### CustomVoice

| Field | Type |
|---|---|
| `task_id` | `str` |
| `voice_id` | `str \| None` |
| `status` | `str \| None` |
| `error_code` | `int \| None` |
| `error_message` | `str \| None` |

### VoiceCheck

| Field | Type |
|---|---|
| `is_available` | `bool` |
