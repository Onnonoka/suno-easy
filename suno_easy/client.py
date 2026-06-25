import time
from typing import Literal

import requests

from ._core.constants import DEFAULT_CALLBACK_URL
from .exceptions import TaskFailed, SunoAPIError
from .resources import AudioResource, LyricsResource, MusicResource, PersonaResource

WaitUntil = Literal["complete", "stream"]


class SunoClient:
    """Main client to interact with the Suno API."""

    BASE_URL = "https://api.sunoapi.org"

    def __init__(self, api_key: str, callback_url: str | None = None):
        """Initialize the Suno client.

        Args:
            api_key: Bearer token for the Suno API.
            callback_url: Webhook URL sent as ``callBackUrl`` on async endpoints.
                Defaults to :data:`~suno_easy.DEFAULT_CALLBACK_URL`, a documented
                placeholder for polling-only usage. Set your own URL when handling
                webhooks on your server.
        """
        self.callback_url = callback_url if callback_url is not None else DEFAULT_CALLBACK_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

        self.music = MusicResource(self)
        self.lyrics = LyricsResource(self)
        self.persona = PersonaResource(self)
        self.audio = AudioResource(self)

    def resolve_callback_url(self, callback_url: str | None = None) -> str:
        """Return the effective callback URL (per-call override or client default)."""
        if callback_url is not None:
            return callback_url
        return self.callback_url

    def apply_callback(self, payload: dict, callback_url: str | None = None) -> dict:
        """Inject ``callBackUrl`` into a request payload."""
        payload["callBackUrl"] = self.resolve_callback_url(callback_url)
        return payload

    @staticmethod
    def _validate_response(body: dict, response_text: str) -> dict:
        """Raise on Suno envelope errors (API may return HTTP 200 with code != 200)."""
        code = body.get("code")
        if code is not None and int(code) != 200:
            message = body.get("msg") or body.get("message") or response_text
            raise SunoAPIError(message, status_code=int(code), response_text=response_text)
        return body

    def post(self, url: str, json: dict) -> dict:
        r = self.session.post(self.BASE_URL + url, json=json)
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        return self._validate_response(r.json(), r.text)

    def get(self, url: str, params: dict | None = None) -> dict:
        r = self.session.get(self.BASE_URL + url, params=params)
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        return self._validate_response(r.json(), r.text)

    def get_task_info(self, task_id: str, endpoint: str = "/api/v1/generate/record-info") -> dict:
        return self.get(endpoint, params={"taskId": task_id})["data"]

    @staticmethod
    def _task_failed(res: dict) -> bool:
        status = res.get("status")
        success_flag = res.get("successFlag")

        if status == "FAILED" or success_flag == "FAILED":
            return True
        if isinstance(success_flag, int) and success_flag < 0:
            return True
        if status is not None and str(status).upper() in {"FAILED", "ERROR"}:
            return True
        if success_flag is not None and "FAIL" in str(success_flag).upper():
            return True
        return False

    @staticmethod
    def _task_complete(res: dict, wait_until: WaitUntil) -> bool:
        if wait_until == "stream":
            response_data = res.get("response", {})
            songs_list = []
            if isinstance(response_data, dict):
                songs_list = response_data.get("sunoData") or response_data.get("songs") or []
            if not songs_list:
                songs_list = res.get("songs") or res.get("sunoData") or []
            for song in songs_list:
                if song.get("streamAudioUrl") or song.get("stream_audio_url"):
                    return True

        status = res.get("status")
        success_flag = res.get("successFlag")

        if status == "SUCCESS" or success_flag == "SUCCESS":
            return True
        if success_flag == 1 or success_flag == "1":
            return True
        if "midiData" in res and isinstance(res["midiData"], dict):
            if res["midiData"].get("state") == "complete":
                return True
        return False

    def wait_task(
        self,
        task_id: str,
        endpoint: str = "/api/v1/generate/record-info",
        timeout: int = 300,
        poll_interval: int = 3,
        wait_until: WaitUntil = "complete",
    ) -> dict:
        start = time.time()

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout} seconds")

            res = self.get_task_info(task_id, endpoint)

            if self._task_failed(res):
                raise TaskFailed(res)

            if self._task_complete(res, wait_until):
                return res

            time.sleep(poll_interval)
