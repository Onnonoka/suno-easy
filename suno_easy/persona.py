class PersonaResource:
    """Resource manager for persona creation."""

    def __init__(self, client):
        """Initializes the PersonaResource with a client reference.

        Args:
            client (SunoClient): The parent client instance.
        """
        self.client = client

    def create(self, music_id: str, name: str) -> dict:
        """Creates a personalized music persona based on a generated music ID.

        Args:
            music_id (str): The ID of the generated music track to create the persona from.
            name (str): The name of the persona.

        Returns:
            dict: A dictionary containing the generated persona's details (such as personaId).
        """
        res = self.client.post(
            "/api/v1/generate/persona",
            {
                "musicId": music_id,
                "name": name
            }
        )

        return res["data"]