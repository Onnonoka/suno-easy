import time
import requests

from .exceptions import TaskFailed, SunoAPIError
from .music import MusicResource
from .lyrics import LyricsResource
from .persona import PersonaResource
from .audio import AudioResource


class SunoClient:
    """Main client to interact with the Suno API.

    This client acts as the central orchestrator and HTTP session manager,
    exposing sub-resources to interact with different domain endpoints.

    Attributes:
        music (MusicResource): Endpoints related to music generation and extension.
        lyrics (LyricsResource): Endpoints related to lyrics generation.
        persona (PersonaResource): Endpoints related to persona creation.
        audio (AudioResource): Endpoints related to audio processing (separations, MIDI, covers).
    """

    BASE_URL = "https://api.sunoapi.org"

    def __init__(self, api_key: str):
        """Initializes the SunoClient with a bearer token.

        Args:
            api_key (str): The API key for authorization.
        """
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

        # Composition: Initialize sub-resources
        self.music = MusicResource(self)
        self.lyrics = LyricsResource(self)
        self.persona = PersonaResource(self)
        self.audio = AudioResource(self)

    def post(self, url: str, json: dict) -> dict:
        """Sends a POST request to the API.

        Args:
            url (str): The endpoint path.
            json (dict): The JSON payload.

        Returns:
            dict: The JSON response.

        Raises:
            SunoAPIError: If the API returns an HTTP error.
        """
        r = self.session.post(self.BASE_URL + url, json=json)
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        return r.json()

    def get(self, url: str, params: dict | None = None) -> dict:
        """Sends a GET request to the API.

        Args:
            url (str): The endpoint path.
            params (dict, optional): The query parameters.

        Returns:
            dict: The JSON response.

        Raises:
            SunoAPIError: If the API returns an HTTP error.
        """
        r = self.session.get(self.BASE_URL + url, params=params)
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        return r.json()

    def get_task_info(self, task_id: str, endpoint: str = "/api/v1/generate/record-info") -> dict:
        """Fetches the raw response data of a task.

        Args:
            task_id (str): The ID of the task to retrieve.
            endpoint (str): The API endpoint path. Defaults to "/api/v1/generate/record-info".

        Returns:
            dict: The raw data dictionary returned by the API.
        """
        return self.get(endpoint, params={"taskId": task_id})["data"]

    def wait_task(
        self,
        task_id: str,
        endpoint: str = "/api/v1/generate/record-info",
        timeout: int = 300,
        poll_interval: int = 3
    ) -> dict:
        """Polls the API and waits for a task to complete.

        Args:
            task_id (str): The ID of the task to poll.
            endpoint (str): The API endpoint path. Defaults to "/api/v1/generate/record-info".
            timeout (int): Maximum wait time in seconds. Defaults to 300.
            poll_interval (int): Time in seconds between polling requests. Defaults to 3.

        Returns:
            dict: The completed task raw response.

        Raises:
            TimeoutError: If the task does not finish within the timeout period.
            TaskFailed: If the task fails or encounters an error.
        """
        start = time.time()

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout} seconds")

            res = self.get_task_info(task_id, endpoint)
            status = res.get("status")
            success_flag = res.get("successFlag")
            error_msg = res.get("errorMessage") or res.get("errorMsg")

            if (
                status == "FAILED"
                or success_flag == "FAILED"
                or (isinstance(success_flag, int) and success_flag < 0)
                or (status is not None and "FAIL" in str(status).upper())
                or (success_flag is not None and "FAIL" in str(success_flag).upper())
                or error_msg
            ):
                if error_msg or status == "FAILED" or success_flag == "FAILED" or (isinstance(success_flag, int) and success_flag < 0):
                    raise TaskFailed(res)

            is_complete = False
            if status == "SUCCESS" or success_flag == "SUCCESS":
                is_complete = True
            elif success_flag == 1 or success_flag == "1":
                is_complete = True
            elif "midiData" in res and isinstance(res["midiData"], dict) and res["midiData"].get("state") == "complete":
                is_complete = True

            if is_complete:
                return res

            time.sleep(poll_interval)