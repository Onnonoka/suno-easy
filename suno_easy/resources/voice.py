from __future__ import annotations

import time
from typing import Union

from .._core.tasks import Task, TaskKind, RECORD_INFO_ENDPOINTS
from .._core.types import SingerSkillLevel, VoiceLanguage
from ..exceptions import TaskFailed
from ..models import CustomVoice, VoiceCheck, VoiceValidationInfo

_VALIDATE_READY = {"wait_validating"}
_VALIDATE_FAILED = {"processing_validate_fail", "fail"}
_VOICE_READY = {"success"}
_VOICE_FAILED = {"fail"}


class VoiceResource:
    """Resource manager for Suno Voice custom voice workflow."""

    def __init__(self, client):
        self.client = client

    def get_validate_info(self, task_id: str) -> VoiceValidationInfo:
        """Fetch validation phrase generation status."""
        response = self.client.get(
            "/api/v1/voice/validate-info",
            params={"taskId": task_id},
        )
        return VoiceValidationInfo.from_api_data(response["data"])

    def get_record(self, task_id: str) -> CustomVoice:
        """Fetch custom voice generation status."""
        response = self.client.get(
            "/api/v1/voice/record-info",
            params={"taskId": task_id},
        )
        return CustomVoice.from_api_data(response["data"])

    def validate(
        self,
        voice_url: str,
        vocal_start_s: int,
        vocal_end_s: int,
        language: Union[VoiceLanguage, str] | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300,
        poll_interval: int = 3,
    ) -> Task[VoiceValidationInfo] | VoiceValidationInfo:
        """Generate a validation phrase from a source vocal segment."""
        payload: dict = {
            "voiceUrl": voice_url,
            "vocalStartS": vocal_start_s,
            "vocalEndS": vocal_end_s,
        }
        if language is not None:
            payload["language"] = language.value if isinstance(language, VoiceLanguage) else language
        self.client.apply_callback(payload, callback_url)
        response = self.client.post("/api/v1/voice/validate", payload)
        task_id = response["data"]["taskId"]
        if not wait:
            return Task(
                task_id=task_id,
                kind=TaskKind.VOICE_VALIDATE,
                _client=self.client,
                _parse=VoiceValidationInfo.from_api_data,
                record_info_endpoint=RECORD_INFO_ENDPOINTS[TaskKind.VOICE_VALIDATE],
            )
        return self._wait_validate_info(task_id, timeout, poll_interval)

    def generate(
        self,
        task_id: str,
        verify_url: str,
        voice_name: str | None = None,
        description: str | None = None,
        style: str | None = None,
        singer_skill_level: Union[SingerSkillLevel, str] = SingerSkillLevel.BEGINNER,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 600,
        poll_interval: int = 3,
    ) -> Task[CustomVoice] | CustomVoice:
        """Create a custom voice from the user's verification recording."""
        payload: dict = {"taskId": task_id, "verifyUrl": verify_url}
        if voice_name is not None:
            payload["voiceName"] = voice_name
        if description is not None:
            payload["description"] = description
        if style is not None:
            payload["style"] = style
        payload["singerSkillLevel"] = (
            singer_skill_level.value
            if isinstance(singer_skill_level, SingerSkillLevel)
            else singer_skill_level
        )
        self.client.apply_callback(payload, callback_url)
        response = self.client.post("/api/v1/voice/generate", payload)
        voice_task_id = response["data"]["taskId"]
        if not wait:
            return Task(
                task_id=voice_task_id,
                kind=TaskKind.VOICE,
                _client=self.client,
                _parse=CustomVoice.from_api_data,
                record_info_endpoint=RECORD_INFO_ENDPOINTS[TaskKind.VOICE],
            )
        return self._wait_voice_record(voice_task_id, timeout, poll_interval)

    def regenerate(self, task_id: str, callback_url: str | None = None) -> str:
        """Regenerate the validation phrase for an existing task.

        Note: the upstream API uses the field name ``calBackUrl`` (typo).
        """
        payload = {
            "taskId": task_id,
            "calBackUrl": self.client.resolve_callback_url(callback_url),
        }
        response = self.client.post("/api/v1/voice/regenerate", payload)
        return response["data"]["taskId"]

    def check(self, task_id: str) -> VoiceCheck:
        """Check whether a generated custom voice is available."""
        response = self.client.post("/api/v1/voice/check-voice", {"task_id": task_id})
        return VoiceCheck.from_api_data(response["data"])

    def _wait_validate_info(
        self,
        task_id: str,
        timeout: int,
        poll_interval: int,
    ) -> VoiceValidationInfo:
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"Voice validation task {task_id} timed out after {timeout} seconds")

            info = self.get_validate_info(task_id)
            if info.status in _VALIDATE_FAILED:
                raise TaskFailed(
                    {
                        "taskId": task_id,
                        "status": info.status,
                        "errorMessage": info.error_message,
                        "errorCode": info.error_code,
                    }
                )
            if info.status in _VALIDATE_READY and info.validate_info:
                return info

            time.sleep(poll_interval)

    def _wait_voice_record(
        self,
        task_id: str,
        timeout: int,
        poll_interval: int,
    ) -> CustomVoice:
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"Voice generation task {task_id} timed out after {timeout} seconds")

            record = self.get_record(task_id)
            if record.status in _VOICE_FAILED:
                raise TaskFailed(
                    {
                        "taskId": task_id,
                        "status": record.status,
                        "errorMessage": record.error_message,
                        "errorCode": record.error_code,
                    }
                )
            if record.status in _VOICE_READY and record.voice_id:
                return record

            time.sleep(poll_interval)
