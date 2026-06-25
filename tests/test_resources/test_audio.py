import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, SeparationMode


class TestAudioResource(unittest.TestCase):
    @patch("requests.Session.post")
    def test_separate_vocals_requires_audio_id_in_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "stem-1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {}}):
            client.audio.separate_vocals(
                task_id="task-1",
                audio_id="audio-1",
                mode=SeparationMode.SPLIT_STEM,
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["audioId"], "audio-1")
        self.assertEqual(payload["type"], "split_stem")
        self.assertEqual(payload["callBackUrl"], client.callback_url)

    @patch("requests.Session.post")
    def test_add_vocals_sends_required_fields(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.audio.add_vocals(
                upload_url="https://example.com/instrumental.mp3",
                prompt="A love song about the stars",
                title="Starlight",
                style="Pop",
                negative_tags="rap, metal",
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["style"], "Pop")
        self.assertEqual(payload["negativeTags"], "rap, metal")


if __name__ == "__main__":
    unittest.main()
