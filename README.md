# suno-easy 🎵

> [!IMPORTANT]
> **Disclaimer**: This is an unofficial, community-driven Python SDK wrapper for the Suno API (`sunoapi.org`). It is not affiliated with, endorsed, sponsored, or supported by Suno, Inc. or the official Suno AI platform.

`suno-easy` is a lightweight, modern, and fully-typed Python SDK for the Suno AI API ([sunoapi.org](https://docs.sunoapi.org/)). 

It provides an intuitive, object-oriented interface to generate music, write lyrics, create voice personas, separate audio stems, and generate MIDI notes from audio files.

---

## Features

- **Clean Namespace Organization**: Resources are grouped logically (`client.music`, `client.lyrics`, `client.audio`, `client.persona`).
- **Fully Typed**: Rich python dataclasses for responses (`Song`, `Lyrics`, `SeparatedStems`, `MIDIData`, `CoverImage`).
- **Smart Polling**: Methods can either block and return the processed result (`wait=True`) or instantly return a `taskId` for asynchronous workflows (`wait=False`).
- **Built-in Downloads**: Download audio tracks, cover images, and isolated stems with built-in streaming helpers.
- **Robust Error Handling**: Distinct exceptions for HTTP failures (`SunoAPIError`) and generation failures (`TaskFailed`).

---

## Repository Structure

```text
suno-easy/
├── suno_easy/          # Core SDK library source code
│   ├── __init__.py     # Exposed client, models, and exceptions
│   ├── client.py       # Main SunoClient orchestrator
│   ├── models.py       # Strongly typed dataclasses representing API payloads
│   ├── audio.py        # Audio processing sub-resource (stems, MIDI, covers)
│   ├── music.py        # Music generation and extension sub-resource
│   ├── lyrics.py       # Lyrics generation sub-resource
│   ├── persona.py      # Voice/style persona sub-resource
│   ├── exceptions.py   # SDK custom exception classes
│   └── utils.py        # Internal utility and polling helpers
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_client.py  # Mocked HTTP interface unit tests
├── examples/           # Basic usage examples
│   └── quickstart.py   # Quickstart example script
├── pyproject.toml      # PEP 621 compliant project packaging configuration
├── requirements.txt    # Runtime dependencies
├── requirements-dev.txt# Development and testing requirements
├── LICENSE             # MIT License file
└── README.md           # Project documentation
```

---

## Installation

This SDK requires `requests`. You can install the package directly from source:

```bash
pip install .
```

Or for development (editable mode):

```bash
pip install -e .
```

---

## Quickstart

### 1. Initialize the Client

```python
from suno_easy import SunoClient

client = SunoClient(api_key="your_suno_api_key_here")
```

### 2. Generate Music

Generate a track in custom mode (requires prompt, style, and title). By default, this blocks until the songs are generated (usually 2-3 minutes) and returns a list containing two song variations.

```python
songs = client.music.generate(
    prompt="A peaceful acoustic guitar melody with soft strings",
    style="Folk, Acoustic",
    title="Morning Breeze",
    instrumental=True
)

for song in songs:
    print(f"Song generated: {song.title} (ID: {song.id})")
    print(f"Audio URL: {song.audio_url}")
    
    # Download the track and its cover image
    song.download(f"{song.title}.mp3")
    song.download_image(f"{song.title}.jpg")
```

### 3. Generate Lyrics

Create AI-generated lyrics structure markers like `[Verse]` or `[Chorus]`.

```python
lyrics_list = client.lyrics.generate(prompt="a song about embarking on a journey to Mars")

for lyrics in lyrics_list:
    print(f"Title Idea: {lyrics.title}")
    print(lyrics.text)
```

### 4. Separate Vocals (Stem Separation)

Separate an existing song task into vocals and instrumental tracks. Supports 2-stem (`separate_vocal`) and up to 12-stem (`split_stem`) separation.

```python
stems = client.audio.separate_vocals(
    task_id="original_music_task_id",
    mode="separate_vocal" # or "split_stem"
)

print(f"Vocal URL: {stems.vocal_url}")
print(f"Instrumental URL: {stems.instrumental_url}")

# Download isolated files
stems.download_vocal("vocals.mp3")
stems.download_instrumental("instrumental.mp3")
```

### 5. Convert Audio to MIDI

Convert separated audio tracks into MIDI note structures.

```python
midi_data = client.audio.generate_midi(task_id="vocal_removal_task_id")

print(f"MIDI Generation State: {midi_data.state}")
for instrument in midi_data.instruments:
    print(f"Instrument: {instrument.name}")
    for note in instrument.notes[:5]: # Print first 5 notes
        print(f"  Note pitch: {note.pitch}, start: {note.start}s, end: {note.end}s")
```

---

## Asynchronous Workflows (Webhooks & Background Tasks)

If you don't want the methods to block your program execution, set `wait=False`. The client will instantly return the `taskId` string. You can then poll later or receive webhook callbacks on your server.

```python
# Starts music generation and returns instantly
task_id = client.music.generate(
    prompt="Lo-fi hip hop beat for studying",
    style="Lo-Fi",
    title="Study Session",
    wait=False,
    callback_url="https://yourdomain.com/webhook"
)

print(f"Music generation started. Task ID: {task_id}")

# Manually retrieve info later
task_info = client.music.get_task_info(task_id)
print(f"Status: {task_info.get('status')}")
```

---

## API Reference

### `client.music`
*   `generate(...) -> list[Song] | str`: Generates songs from prompts.
*   `extend(...) -> list[Song] | str`: Extends an existing song from a timestamp.
*   `generate_instrumental(...) -> list[Song] | str`: Generates instrumentals.
*   `remaster(music_id, ...) -> list[Song] | str`: Improves the quality of a song.

### `client.lyrics`
*   `generate(prompt, ...) -> list[Lyrics] | str`: Generates lyrics.
*   `get(task_id) -> list[Lyrics]`: Retrieves lyrics from a completed task.

### `client.audio`
*   `cover(upload_url, style, title, ...) -> list[Song] | str`: Applies a style cover to an uploaded audio.
*   `extend(upload_url, continue_at, prompt, ...) -> list[Song] | str`: Extends an uploaded audio track.
*   `separate_vocals(task_id, mode, ...) -> SeparatedStems | str`: Split vocals and instrumentation.
*   `get_separated_stems(task_id) -> SeparatedStems`: Retrieves separated stems.
*   `generate_midi(task_id, ...) -> MIDIData | str`: Converts audio stems to MIDI notes.
*   `get_midi(task_id) -> MIDIData`: Retrieves MIDI notes.
*   `add_vocals(upload_url, prompt, ...) -> list[Song] | str`: Adds vocals to an instrumental track.
*   `add_instrumental(upload_url, title, tags, ...) -> list[Song] | str`: Adds backing instruments to vocals.

### `client.persona`
*   `create(music_id, name) -> dict`: Creates a voice/style persona from a track.

---

## License

This project is licensed under the MIT License.
