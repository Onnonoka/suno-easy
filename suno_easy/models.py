from dataclasses import dataclass
import requests


@dataclass
class Song:
    id: str
    title: str
    audio_url: str | None = None
    stream_url: str | None = None
    image_url: str | None = None
    prompt: str | None = None
    tags: str | None = None
    duration: float | None = None
    model_name: str | None = None
    create_time: str | None = None

    def download(self, path: str):
        if not self.audio_url:
            raise ValueError("No audio_url available")

        r = requests.get(self.audio_url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

    def download_image(self, path: str):
        if not self.image_url:
            raise ValueError("No image_url available")

        r = requests.get(self.image_url)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)

    @classmethod
    def from_task_data(cls, task_data: dict) -> list["Song"]:
        response_data = task_data.get("response", {})
        songs_list = []
        if isinstance(response_data, dict):
            songs_list = response_data.get("sunoData") or response_data.get("songs") or []
        if not songs_list:
            songs_list = task_data.get("songs") or task_data.get("sunoData") or []
        
        return [
            cls(
                id=song["id"],
                title=song.get("title", ""),
                audio_url=song.get("audioUrl"),
                stream_url=song.get("streamAudioUrl"),
                image_url=song.get("imageUrl"),
                prompt=song.get("prompt"),
                tags=song.get("tags"),
                duration=song.get("duration"),
                model_name=song.get("modelName"),
                create_time=song.get("createTime")
            )
            for song in songs_list
        ]


@dataclass
class Lyrics:
    text: str
    title: str
    status: str | None = None
    error_message: str | None = None

    @classmethod
    def from_task_data(cls, task_data: dict) -> list["Lyrics"]:
        response_data = task_data.get("response", {})
        lyrics_list = []
        if isinstance(response_data, dict):
            lyrics_list = response_data.get("data") or []
        if not lyrics_list:
            lyrics_list = task_data.get("data") or []
        
        return [
            cls(
                text=lyric.get("text", ""),
                title=lyric.get("title", ""),
                status=lyric.get("status"),
                error_message=lyric.get("errorMessage")
            )
            for lyric in lyrics_list
        ]


@dataclass
class CoverImage:
    images: list[str]

    @classmethod
    def from_task_data(cls, task_data: dict) -> "CoverImage":
        response_data = task_data.get("response", {})
        images = []
        if isinstance(response_data, dict):
            images = response_data.get("images") or []
        if not images:
            images = task_data.get("images") or []
        return cls(images=images)


@dataclass
class SeparatedStems:
    vocal_url: str | None = None
    instrumental_url: str | None = None
    backing_vocals_url: str | None = None
    drums_url: str | None = None
    bass_url: str | None = None
    guitar_url: str | None = None
    keyboard_url: str | None = None
    percussion_url: str | None = None
    strings_url: str | None = None
    synth_url: str | None = None
    fx_url: str | None = None
    brass_url: str | None = None
    woodwinds_url: str | None = None

    def download_vocal(self, path: str):
        if not self.vocal_url:
            raise ValueError("No vocal_url available")
        self._download_file(self.vocal_url, path)

    def download_instrumental(self, path: str):
        if not self.instrumental_url:
            raise ValueError("No instrumental_url available")
        self._download_file(self.instrumental_url, path)

    def _download_file(self, url: str, path: str):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

    @classmethod
    def from_task_data(cls, task_data: dict) -> "SeparatedStems":
        response_data = task_data.get("response", {})
        if not isinstance(response_data, dict):
            response_data = {}
        src = response_data if response_data else task_data
        return cls(
            vocal_url=src.get("vocalUrl"),
            instrumental_url=src.get("instrumentalUrl"),
            backing_vocals_url=src.get("backingVocalsUrl"),
            drums_url=src.get("drumsUrl"),
            bass_url=src.get("bassUrl"),
            guitar_url=src.get("guitarUrl"),
            keyboard_url=src.get("keyboardUrl"),
            percussion_url=src.get("percussionUrl"),
            strings_url=src.get("stringsUrl"),
            synth_url=src.get("synthUrl"),
            fx_url=src.get("fxUrl"),
            brass_url=src.get("brassUrl"),
            woodwinds_url=src.get("woodwindsUrl")
        )


@dataclass
class MIDINote:
    pitch: int
    start: float
    end: float
    velocity: float


@dataclass
class MIDIInstrument:
    name: str
    notes: list[MIDINote]


@dataclass
class MIDIData:
    state: str
    instruments: list[MIDIInstrument]

    @classmethod
    def from_task_data(cls, task_data: dict) -> "MIDIData":
        midi_data = task_data.get("midiData", {})
        if not isinstance(midi_data, dict):
            midi_data = {}
        
        instruments_list = []
        for inst in midi_data.get("instruments", []):
            notes = [
                MIDINote(
                    pitch=note.get("pitch", 0),
                    start=note.get("start", 0.0),
                    end=note.get("end", 0.0),
                    velocity=note.get("velocity", 0.0)
                )
                for note in inst.get("notes", [])
            ]
            instruments_list.append(
                MIDIInstrument(
                    name=inst.get("name", ""),
                    notes=notes
                )
            )
        
        return cls(
            state=midi_data.get("state", ""),
            instruments=instruments_list
        )