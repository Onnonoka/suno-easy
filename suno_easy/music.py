from .models import Song


class MusicResource:
    """Resource manager for music generation, extension, and remastering."""

    def __init__(self, client):
        """Initializes the MusicResource with a client reference.

        Args:
            client (SunoClient): The parent client instance.
        """
        self.client = client

    def generate(
        self,
        prompt: str,
        style: str = "",
        title: str = "",
        model: str = "V4_5ALL",
        instrumental: bool = False,
        custom_mode: bool = True,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Generates music based on a prompt.

        Args:
            prompt (str): Text prompt describing the music.
            style (str): Musical style. Required if custom_mode is True. Defaults to "".
            title (str): Title of the generated music. Required if custom_mode is True. Defaults to "".
            model (str): Model version to use. Defaults to "V4_5ALL".
            instrumental (bool): Generate instrumental music without vocals. Defaults to False.
            custom_mode (bool): Use custom mode. Defaults to True.
            callback_url (str, optional): Webhook URL for callback notification.
            wait (bool): If True, poll and wait for task completion. Defaults to True.
            timeout (int): Max time in seconds to wait for task completion. Defaults to 300.

        Returns:
            str | list[Song]: A list of generated Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "customMode": custom_mode,
            "prompt": prompt,
            "style": style,
            "title": title,
            "instrumental": instrumental,
            "model": model
        }
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/generate", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)

    def extend(
        self,
        audio_id: str,
        continue_at: int,
        prompt: str,
        style: str = "",
        title: str = "",
        model: str = "V4_5ALL",
        default_param_flag: bool = True,
        persona_id: str | None = None,
        persona_model: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Extends an existing audio track.

        Args:
            audio_id (str): The ID of the original music track to extend.
            continue_at (int): Time in seconds in the original track where extension starts.
            prompt (str): Text prompt describing the continuation of the music.
            style (str): Musical style for the continuation. Defaults to "".
            title (str): Title for the extended track. Defaults to "".
            model (str): Model version (should match source track). Defaults to "V4_5ALL".
            default_param_flag (bool): If True, uses custom parameters. Defaults to True.
            persona_id (str, optional): Optional Persona ID.
            persona_model (str, optional): Persona model type ("style_persona" or "voice_persona").
            callback_url (str, optional): Webhook URL for callback notification.
            wait (bool): If True, poll and wait for task completion. Defaults to True.
            timeout (int): Max time in seconds to wait for task completion. Defaults to 300.

        Returns:
            str | list[Song]: A list of extended Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "audioId": audio_id,
            "continueAt": continue_at,
            "prompt": prompt,
            "style": style,
            "title": title,
            "model": model,
            "defaultParamFlag": default_param_flag
        }
        if persona_id:
            payload["personaId"] = persona_id
        if persona_model:
            payload["personaModel"] = persona_model
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/generate/extend", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)

    def generate_instrumental(
        self,
        style: str,
        title: str,
        model: str = "V4_5ALL",
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Helper to generate instrumental music.

        Args:
            style (str): Musical style.
            title (str): Title of the music.
            model (str): Model version. Defaults to "V4_5ALL".
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | list[Song]: A list of generated Song objects if wait is True, otherwise the taskId as a string.
        """
        return self.generate(
            prompt="",
            style=style,
            title=title,
            model=model,
            instrumental=True,
            callback_url=callback_url,
            wait=wait,
            timeout=timeout
        )

    def remaster(
        self,
        music_id: str,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Remasters an existing track to improve production quality/mix.

        Args:
            music_id (str): ID of the generated track to remaster.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | list[Song]: A list of remastered Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "musicId": music_id
        }

        res = self.client.post("/api/v1/generate/remaster", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)
