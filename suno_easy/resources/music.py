from __future__ import annotations

from typing import Union

from .._core.payload import add_tuning_params, model_value
from .._core.submit import submit_api_task
from .._core.tasks import Task, TaskKind, RECORD_INFO_ENDPOINTS
from .._core.types import ModelVersion, PersonaModel, VocalGender
from ..models import Song


class MusicResource:
    """Resource manager for music generation and extension."""

    def __init__(self, client):
        self.client = client

    def get_task(self, task_id: str) -> dict:
        """Fetch raw task details for a music generation task."""
        return self.client.get_task_info(task_id, RECORD_INFO_ENDPOINTS[TaskKind.MUSIC])

    def generate(
        self,
        prompt: str,
        style: str = "",
        title: str = "",
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
        instrumental: bool = False,
        custom_mode: bool = True,
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
            "customMode": custom_mode,
            "prompt": prompt,
            "style": style,
            "title": title,
            "instrumental": instrumental,
            "model": model_value(model),
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
            "/api/v1/generate",
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
        audio_id: str,
        continue_at: int,
        prompt: str,
        style: str = "",
        title: str = "",
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
        default_param_flag: bool = True,
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
            "audioId": audio_id,
            "continueAt": continue_at,
            "prompt": prompt,
            "style": style,
            "title": title,
            "model": model_value(model),
            "defaultParamFlag": default_param_flag,
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
            "/api/v1/generate/extend",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def generate_instrumental(
        self,
        style: str,
        title: str,
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
        **kwargs,
    ) -> Task[list[Song]] | list[Song]:
        return self.generate(
            prompt="",
            style=style,
            title=title,
            model=model,
            instrumental=True,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
            **kwargs,
        )

    def mashup(
        self,
        upload_urls: list[str],
        custom_mode: bool = True,
        prompt: str = "",
        style: str = "",
        title: str = "",
        instrumental: bool = False,
        model: Union[ModelVersion, str] = ModelVersion.V4_5ALL,
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
            "uploadUrlList": upload_urls,
            "customMode": custom_mode,
            "prompt": prompt,
            "style": style,
            "title": title,
            "instrumental": instrumental,
            "model": model_value(model),
        }
        add_tuning_params(
            payload,
            vocal_gender=vocal_gender,
            style_weight=style_weight,
            weirdness_constraint=weirdness_constraint,
            audio_weight=audio_weight,
        )
        return submit_api_task(
            self.client,
            "/api/v1/generate/mashup",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def replace_section(
        self,
        task_id: str,
        audio_id: str,
        prompt: str,
        tags: str,
        title: str,
        full_lyrics: str,
        infill_start_s: float,
        infill_end_s: float,
        negative_tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "taskId": task_id,
            "audioId": audio_id,
            "prompt": prompt,
            "tags": tags,
            "title": title,
            "fullLyrics": full_lyrics,
            "infillStartS": infill_start_s,
            "infillEndS": infill_end_s,
        }
        if negative_tags is not None:
            payload["negativeTags"] = negative_tags
        return submit_api_task(
            self.client,
            "/api/v1/generate/replace-section",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )

    def generate_sounds(
        self,
        prompt: str,
        model: Union[ModelVersion, str] = ModelVersion.V5,
        sound_loop: bool | None = None,
        sound_tempo: int | None = None,
        sound_key: str | None = None,
        grab_lyrics: bool | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        wait_until: str = "complete",
    ) -> Task[list[Song]] | list[Song]:
        payload = {
            "prompt": prompt,
            "model": model_value(model),
        }
        if sound_loop is not None:
            payload["soundLoop"] = sound_loop
        if sound_tempo is not None:
            payload["soundTempo"] = sound_tempo
        if sound_key is not None:
            payload["soundKey"] = sound_key
        if grab_lyrics is not None:
            payload["grabLyrics"] = grab_lyrics
        return submit_api_task(
            self.client,
            "/api/v1/generate/sounds",
            payload,
            TaskKind.MUSIC,
            Song.from_task_data,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout,
            wait_until=wait_until,
        )
