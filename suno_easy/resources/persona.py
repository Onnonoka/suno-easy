from ..models import Persona


class PersonaResource:
    """Resource manager for persona creation."""

    def __init__(self, client):
        self.client = client

    def create(
        self,
        task_id: str,
        audio_id: str,
        name: str,
        description: str,
        vocal_start: float | None = None,
        vocal_end: float | None = None,
        style: str | None = None,
    ) -> Persona:
        """Create a style persona from an existing generated track."""
        payload = {
            "taskId": task_id,
            "audioId": audio_id,
            "name": name,
            "description": description,
        }
        if vocal_start is not None:
            payload["vocalStart"] = vocal_start
        if vocal_end is not None:
            payload["vocalEnd"] = vocal_end
        if style is not None:
            payload["style"] = style

        response = self.client.post("/api/v1/generate/generate-persona", payload)
        return Persona.from_api_data(response["data"])
