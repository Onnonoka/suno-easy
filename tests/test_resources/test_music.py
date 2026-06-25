import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, ModelVersion, PersonaModel, VocalGender


class TestMusicResource(unittest.TestCase):
    @patch("requests.Session.post")
    def test_generate_injects_callback_and_tuning(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "t1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k", callback_url="https://hooks.example.com/suno")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.music.generate(
                prompt="hello",
                style="Pop",
                title="Test",
                model=ModelVersion.V4_5ALL,
                negative_tags="metal",
                vocal_gender=VocalGender.FEMALE,
                persona_id="persona-1",
                persona_model=PersonaModel.STYLE,
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["callBackUrl"], "https://hooks.example.com/suno")
        self.assertEqual(payload["negativeTags"], "metal")
        self.assertEqual(payload["vocalGender"], "f")
        self.assertEqual(payload["personaId"], "persona-1")
        self.assertEqual(payload["personaModel"], "style_persona")
        self.assertEqual(payload["model"], "V4_5ALL")

    def test_remaster_removed(self):
        self.assertFalse(hasattr(SunoClient(api_key="k").music, "remaster"))


if __name__ == "__main__":
    unittest.main()
