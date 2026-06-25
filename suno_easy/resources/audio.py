from __future__ import annotations

from typing import Union

from .._core.payload import add_tuning_params, model_value
from .._core.submit import submit_api_task
from .._core.tasks import Task, TaskKind, RECORD_INFO_ENDPOINTS
from .._core.types import ModelVersion, PersonaModel, SeparationMode, VocalGender
from ..models import Song, CoverImage, SeparatedStems, MIDIData


class AudioResource:
    """Resource manager for audio processing."""

    def __init__(self, client):
        self.client = client

    def get_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.MUSIC])

    def get_cover_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.COVER_IMAGE])

    def get_vocal_separation_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.VOCAL_SEPARATION])

    def get_midi_task(self, task_id: str) -> dict:
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.MIDI])

    def cover(
        self,
        upload_url: str,
        style: str,
        title: str,
        prompt: str = "",
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
        custom_mode: bool = True,
        instrumental: bool = False,
        persona_id: str | None = None,
        persona_model: Union[PersonaModel, str, None] = None,
        negative_tags: str | None = None,
        vocal_gender: Union[VocalGender, str, None] = None,
        style_weight: float | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "uploadUrl": upload_url,
            "style": style,
            "title": title,
            "prompt": prompt,
            "model": model_value(model),
            "customMode": custom_mode,
            "instrumental": instrumental,
        }
        add_tuning_params(
            payload,
            negative_tags=negative_tags,
            vocal_gender=vocal_gender,
            style_weight=style_weight,
            weirdness_constraint=weirdness_constraint,
            audio_weight=audio_weight,
            persona_id=persona_id,
            persona_model=persona_model,
        )
        return submit_api_task(
            self.client,
            "/api/v1/generate/upload-cover",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def extend(
        self,
        upload_url: str,
        continue_at: int,
        prompt: str,
        style: str = "",
        title: str = "",
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
        default_param_flag: bool = True,
        instrumental: bool = False,
        persona_id: str | None = None,
        persona_model: Union[PersonaModel, str, None] = None,
        negative_tags: str | None = None,
        vocal_gender: Union[VocalGender, str, None] = None,
        style_weight: float | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "uploadUrl": upload_url,
            "continueAt": continue_at,
            "prompt": prompt,
            "style": style,
            "title": title,
            "model": model_value(model),
            "defaultParamFlag": default_param_flag,
            "instrumental": instrumental,
        }
        add_tuning_params(
            payload,
            negative_tags=negative_tags,
            vocal_gender=vocal_gender,
            style_weight=style_weight,
            weirdness_constraint=weirdness_constraint,
            audio_weight=audio_weight,
            persona_id=persona_id,
            persona_model=persona_model,
        )
        return submit_api_task(
            self.client,
            "/api/v1/generate/upload-extend",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def generate_cover_image(
        self,
        task_id: str,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
    ) -> Task[CoverImage] | CoverImage:
        payload = {"taskId": task_id}
        return submit_api_task(
            self.client,
            "/api/v1/suno/cover/generate",
            payload,
            TaskKind.COVER_IMAGE,
            CoverImage.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
        )

    def get_cover_image(self, task_id: str) -> CoverImage:
        task_data = self.client.get_task_info(task_id, endpoint=RECORD_INFO_ENDPOINTS[TaskKind.COVER_IMAGE])
        return CoverImage.from_task_data(task_data)

    def separate_vocals(
        self,
        task_id: str,
        audio_id: str,
        mode: Union[SeparationMode, str] = SeparationMode.SEPARATE_VOCAL,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
    ) -> Task[SeparatedStems] | SeparatedStems:
        payload = {
            "taskId": task_id,
            "audioId": audio_id,
            "type": mode.value if isinstance(mode, SeparationMode) else mode,
        }
        return submit_api_task(
            self.client,
            "/api/v1/vocal-removal/generate",
            payload,
            TaskKind.VOCAL_SEPARATION,
            SeparatedStems.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
        )

    def get_separated_stems(self, task_id: str) -> SeparatedStems:
        task_data = self.client.get_task_info(
            task_id, endpoint=RECORD_INFO_ENDPOINTS[TaskKind.VOCAL_SEPARATION]
        )
        return SeparatedStems.from_task_data(task_data)

    def generate_midi(
        self,
        task_id: str,
        audio_id: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
    ) -> Task[MIDIData] | MIDIData:
        payload = {"taskId": task_id}
        if audio_id is not None:
            payload["audioId"] = audio_id
        return submit_api_task(
            self.client,
            "/api/v1/midi/generate",
            payload,
            TaskKind.MIDI,
            MIDIData.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
        )

    def get_midi(self, task_id: str) -> MIDIData:
        task_data = self.client.get_task_info(task_id, endpoint=RECORD_INFO_ENDPOINTS[TaskKind.MIDI])
        return MIDIData.from_task_data(task_data)

    def add_vocals(
        self,
        upload_url: str,
        prompt: str,
        title: str,
        style: str,
        negative_tags: str,
        vocal_gender: Union[VocalGender, str, None] = None,
        style_weight: float | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        model: Union[ModelVersion, str, None] = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "uploadUrl": upload_url,
            "prompt": prompt,
            "title": title,
            "style": style,
            "negativeTags": negative_tags,
        }
        add_tuning_params(
            payload,
            vocal_gender=vocal_gender,
            style_weight=style_weight,
            weirdness_constraint=weirdness_constraint,
            audio_weight=audio_weight,
        )
        if model is not None:
            payload["model"] = model_value(model)
        return submit_api_task(
            self.client,
            "/api/v1/generate/add-vocals",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def add_instrumental(
        self,
        upload_url: str,
        title: str,
        tags: str,
        negative_tags: str,
        vocal_gender: Union[VocalGender, str, None] = None,
        style_weight: float | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        model: Union[ModelVersion, str, None] = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "uploadUrl": upload_url,
            "title": title,
            "tags": tags,
            "negativeTags": negative_tags,
        }
        add_tuning_params(
            payload,
            vocal_gender=vocal_gender,
            style_weight=style_weight,
            weirdness_constraint=weirdness_constraint,
            audio_weight=audio_weight,
        )
        if model is not None:
            payload["model"] = model_value(model)
        return submit_api_task(
            self.client,
            "/api/v1/generate/add-instrumental",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )
