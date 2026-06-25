from .models import Song, CoverImage, SeparatedStems, MIDIData


class AudioResource:
    """Resource manager for audio processing (vocal separation, MIDI, covers, uploading)."""

    def __init__(self, client):
        """Initializes the AudioResource with a client reference.

        Args:
            client (SunoClient): The parent client instance.
        """
        self.client = client

    def cover(
        self,
        upload_url: str,
        style: str,
        title: str,
        prompt: str = "",
        model: str = "V4_5ALL",
        custom_mode: bool = True,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Uploads an audio track and transforms it into a new style (Cover).

        Args:
            upload_url (str): Public URL of the audio file to cover.
            style (str): Musical style for the cover. Required if custom_mode is True. Defaults to "".
            title (str): Title for the cover track. Required if custom_mode is True. Defaults to "".
            prompt (str): Optional prompt describing changes/vocals. Defaults to "".
            model (str): Model version. Defaults to "V4_5ALL".
            custom_mode (bool): Use custom mode. Defaults to True.
            callback_url (str, optional): Webhook URL for completion notification.
            wait (bool): If True, poll and wait for task completion. Defaults to True.
            timeout (int): Max time in seconds to wait for task completion. Defaults to 300.

        Returns:
            str | list[Song]: A list of covered Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "uploadUrl": upload_url,
            "style": style,
            "title": title,
            "prompt": prompt,
            "model": model,
            "customMode": custom_mode
        }
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/generate/upload-cover", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)

    def extend(
        self,
        upload_url: str,
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
        """Uploads an audio file and extends it.

        Args:
            upload_url (str): Public URL of the audio file to extend.
            continue_at (int): Time in seconds in the original track where extension starts.
            prompt (str): Text prompt describing the continuation.
            style (str): Musical style for the continuation. Defaults to "".
            title (str): Title for the extended track. Defaults to "".
            model (str): Model version. Defaults to "V4_5ALL".
            default_param_flag (bool): If True, uses custom parameters. Defaults to True.
            persona_id (str, optional): Optional Persona ID.
            persona_model (str, optional): Persona model type ("style_persona" or "voice_persona").
            callback_url (str, optional): Webhook URL for callback notification.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | list[Song]: A list of extended Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "uploadUrl": upload_url,
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

        res = self.client.post("/api/v1/generate/upload-extend", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)

    def generate_cover_image(
        self,
        task_id: str,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | CoverImage:
        """Generates a personalized cover image for a music task.

        Args:
            task_id (str): Task ID of the original music generation.
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | CoverImage: A CoverImage object if wait is True, otherwise the taskId as a string.
        """
        payload = {"taskId": task_id}
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/suno/cover/generate", payload)
        new_task_id = res["data"]["taskId"]

        if not wait:
            return new_task_id

        task_data = self.client.wait_task(new_task_id, endpoint="/api/v1/suno/cover/record-info", timeout=timeout)
        return CoverImage.from_task_data(task_data)

    def get_cover_image(self, task_id: str) -> CoverImage:
        """Retrieves the cover image details for a cover task.

        Args:
            task_id (str): The ID of the cover task.

        Returns:
            CoverImage: The CoverImage object containing generated image URLs.
        """
        task_data = self.client.get_task_info(task_id, endpoint="/api/v1/suno/cover/record-info")
        return CoverImage.from_task_data(task_data)

    def separate_vocals(
        self,
        task_id: str,
        mode: str = "separate_vocal",
        audio_id: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | SeparatedStems:
        """Separates vocals from instruments.

        Args:
            task_id (str): Task ID of the original music generation.
            mode (str): Separation mode: "separate_vocal" (2 stems) or "split_stem" (up to 12 stems).
                Defaults to "separate_vocal".
            audio_id (str, optional): Optional specific audio variation ID to process.
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | SeparatedStems: A SeparatedStems object if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "taskId": task_id,
            "type": mode
        }
        if audio_id:
            payload["audioId"] = audio_id
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/vocal-removal/generate", payload)
        new_task_id = res["data"]["taskId"]

        if not wait:
            return new_task_id

        task_data = self.client.wait_task(new_task_id, endpoint="/api/v1/vocal-removal/record-info", timeout=timeout)
        return SeparatedStems.from_task_data(task_data)

    def get_separated_stems(self, task_id: str) -> SeparatedStems:
        """Retrieves stem separation results.

        Args:
            task_id (str): The ID of the vocal separation task.

        Returns:
            SeparatedStems: The SeparatedStems object containing urls of processed stems.
        """
        task_data = self.client.get_task_info(task_id, endpoint="/api/v1/vocal-removal/record-info")
        return SeparatedStems.from_task_data(task_data)

    def generate_midi(
        self,
        task_id: str,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | MIDIData:
        """Converts separated audio tracks into MIDI format.

        Args:
            task_id (str): Task ID of the vocal removal task.
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | MIDIData: A MIDIData object if wait is True, otherwise the taskId as a string.
        """
        payload = {"taskId": task_id}
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/midi/generate", payload)
        new_task_id = res["data"]["taskId"]

        if not wait:
            return new_task_id

        task_data = self.client.wait_task(new_task_id, endpoint="/api/v1/midi/record-info", timeout=timeout)
        return MIDIData.from_task_data(task_data)

    def get_midi(self, task_id: str) -> MIDIData:
        """Retrieves generated MIDI note/instrument data.

        Args:
            task_id (str): The ID of the MIDI generation task.

        Returns:
            MIDIData: The MIDIData object containing instrument and note details.
        """
        task_data = self.client.get_task_info(task_id, endpoint="/api/v1/midi/record-info")
        return MIDIData.from_task_data(task_data)

    def add_vocals(
        self,
        upload_url: str,
        prompt: str,
        style: str = "",
        title: str = "",
        negative_tags: str | None = None,
        vocal_gender: str | None = None,
        style_weight: float | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        model: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Adds vocals to an instrumental track.

        Args:
            upload_url (str): Public URL of the instrumental audio track.
            prompt (str): Text prompt describing the vocal lyrics/style.
            style (str): Musical style. Defaults to "".
            title (str): Title for the track. Defaults to "".
            negative_tags (str, optional): Characteristics to exclude.
            vocal_gender (str, optional): Preferred vocal gender.
            style_weight (float, optional): Weight parameter.
            weirdness_constraint (float, optional): Tuning parameter.
            audio_weight (float, optional): Tuning parameter.
            model (str, optional): Model version.
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | list[Song]: A list of Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "uploadUrl": upload_url,
            "prompt": prompt,
            "style": style,
            "title": title
        }
        if negative_tags is not None:
            payload["negativeTags"] = negative_tags
        if vocal_gender is not None:
            payload["vocalGender"] = vocal_gender
        if style_weight is not None:
            payload["styleWeight"] = style_weight
        if weirdness_constraint is not None:
            payload["weirdnessConstraint"] = weirdness_constraint
        if audio_weight is not None:
            payload["audioWeight"] = audio_weight
        if model is not None:
            payload["model"] = model
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/generate/add-vocals", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)

    def add_instrumental(
        self,
        upload_url: str,
        title: str,
        tags: str = "",
        negative_tags: str | None = None,
        weirdness_constraint: float | None = None,
        audio_weight: float | None = None,
        model: str | None = None,
        callback_url: str | None = None,
        wait: bool = True,
        timeout: int = 300
    ) -> str | list[Song]:
        """Adds instrumental backing to an audio track (e.g. vocals).

        Args:
            upload_url (str): Public URL of the vocal/melody track.
            title (str): Title for the track.
            tags (str): Desired style and characteristics for the accompaniment. Defaults to "".
            negative_tags (str, optional): Styles or instruments to exclude.
            weirdness_constraint (float, optional): Tuning parameter.
            audio_weight (float, optional): Tuning parameter.
            model (str, optional): Model version.
            callback_url (str, optional): Webhook URL.
            wait (bool): If True, poll and wait for completion. Defaults to True.
            timeout (int): Max wait time in seconds. Defaults to 300.

        Returns:
            str | list[Song]: A list of Song objects if wait is True, otherwise the taskId as a string.
        """
        payload = {
            "uploadUrl": upload_url,
            "title": title,
            "tags": tags
        }
        if negative_tags is not None:
            payload["negativeTags"] = negative_tags
        if weirdness_constraint is not None:
            payload["weirdnessConstraint"] = weirdness_constraint
        if audio_weight is not None:
            payload["audioWeight"] = audio_weight
        if model is not None:
            payload["model"] = model
        if callback_url:
            payload["callBackUrl"] = callback_url

        res = self.client.post("/api/v1/generate/add-instrumental", payload)
        task_id = res["data"]["taskId"]

        if not wait:
            return task_id

        task_data = self.client.wait_task(task_id, endpoint="/api/v1/generate/record-info", timeout=timeout)
        return Song.from_task_data(task_data)
