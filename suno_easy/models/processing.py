from dataclasses import dataclass

import requests


@dataclass
class WavFile:
    wav_url: str | None = None
    task_id: str | None = None
    music_id: str | None = None

    def download(self, path: str):
        if not self.wav_url:
            raise ValueError("No wav_url available")
        r = requests.get(self.wav_url, stream=True)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

    @classmethod
    def from_task_data(cls, task_data: dict) -> "WavFile":
        response = task_data.get("response") or {}
        if not isinstance(response, dict):
            response = {}
        wav_url = (
            response.get("audioWavUrl")
            or response.get("audio_wav_url")
            or task_data.get("audioWavUrl")
            or task_data.get("audio_wav_url")
        )
        return cls(
            wav_url=wav_url,
            task_id=task_data.get("taskId") or task_data.get("task_id"),
            music_id=task_data.get("musicId") or task_data.get("music_id"),
        )


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
    def from_callback_data(cls, data: dict) -> "SeparatedStems":
        return cls(
            vocal_url=data.get("vocalUrl") or data.get("vocal_url"),
            instrumental_url=data.get("instrumentalUrl") or data.get("instrumental_url"),
            backing_vocals_url=data.get("backingVocalsUrl") or data.get("backing_vocals_url"),
            drums_url=data.get("drumsUrl") or data.get("drums_url"),
            bass_url=data.get("bassUrl") or data.get("bass_url"),
            guitar_url=data.get("guitarUrl") or data.get("guitar_url"),
            keyboard_url=data.get("keyboardUrl") or data.get("keyboard_url"),
            percussion_url=data.get("percussionUrl") or data.get("percussion_url"),
            strings_url=data.get("stringsUrl") or data.get("strings_url"),
            synth_url=data.get("synthUrl") or data.get("synth_url"),
            fx_url=data.get("fxUrl") or data.get("fx_url"),
            brass_url=data.get("brassUrl") or data.get("brass_url"),
            woodwinds_url=data.get("woodwindsUrl") or data.get("woodwinds_url"),
        )

    @classmethod
    def from_task_data(cls, task_data: dict) -> "SeparatedStems":
        response_data = task_data.get("response", {})
        if not isinstance(response_data, dict):
            response_data = {}
        src = response_data if response_data else task_data
        return cls.from_callback_data(src)


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
    def from_callback_data(cls, data: dict) -> "MIDIData":
        if not isinstance(data, dict):
            data = {}

        instruments_list = []
        for inst in data.get("instruments", []):
            notes = [
                MIDINote(
                    pitch=note.get("pitch", 0),
                    start=note.get("start", 0.0),
                    end=note.get("end", 0.0),
                    velocity=note.get("velocity", 0.0),
                )
                for note in inst.get("notes", [])
            ]
            instruments_list.append(
                MIDIInstrument(name=inst.get("name", ""), notes=notes)
            )

        return cls(state=data.get("state", ""), instruments=instruments_list)

    @classmethod
    def from_task_data(cls, task_data: dict) -> "MIDIData":
        midi_data = task_data.get("midiData", {})
        if not isinstance(midi_data, dict):
            midi_data = {}
        return cls.from_callback_data(midi_data)
