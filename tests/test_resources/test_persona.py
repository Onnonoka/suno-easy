import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, Persona


class TestPersonaResource(unittest.TestCase):
    @patch("requests.Session.post")
    def test_create_uses_correct_endpoint_and_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {
            "code": 200,
            "data": {
                "personaId": "p1",
                "name": "My Persona",
                "description": "Bright pop vocals",
            },
        }
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        persona = client.persona.create(
            task_id="task-1",
            audio_id="audio-1",
            name="My Persona",
            description="Bright pop vocals",
            vocal_start=10.0,
            vocal_end=45.0,
            style="Pop",
        )

        self.assertIsInstance(persona, Persona)
        self.assertEqual(persona.persona_id, "p1")
        self.assertIn("/api/v1/generate/generate-persona", mock_post.call_args.args[0])

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["taskId"], "task-1")
        self.assertEqual(payload["audioId"], "audio-1")
        self.assertEqual(payload["vocalStart"], 10.0)
        self.assertEqual(payload["vocalEnd"], 45.0)
        self.assertEqual(payload["style"], "Pop")


if __name__ == "__main__":
    unittest.main()
