import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, SeparationMode, WavFile, StyleBoost, Task, TaskKind


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

    @patch("requests.Session.post")
    def test_convert_wav(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "wav-1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"audioWavUrl": "https://x/w.wav"}}):
            wav = client.audio.convert_wav("task-1", "audio-1", wait=True)

        self.assertIsInstance(wav, WavFile)
        self.assertEqual(wav.wav_url, "https://x/w.wav")
        self.assertIn("/api/v1/wav/generate", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_boost_style(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {
            "code": 200,
            "data": {"result": "Enhanced pop style", "successFlag": "1"},
        }
        mock_post.return_value = mock_response

        result = SunoClient(api_key="k").audio.boost_style("upbeat pop")
        self.assertIsInstance(result, StyleBoost)
        self.assertEqual(result.result, "Enhanced pop style")
        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["content"], "upbeat pop")
        self.assertIn("/api/v1/style/generate", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_convert_wav_wait_false_returns_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "wav-2"}}
        mock_post.return_value = mock_response

        task = SunoClient(api_key="k").audio.convert_wav("task-1", "audio-1", wait=False)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.task_id, "wav-2")
        self.assertEqual(task.kind, TaskKind.WAV)

    @patch.object(SunoClient, "get_task_info")
    def test_get_wav(self, mock_get_task_info):
        mock_get_task_info.return_value = {"response": {"audioWavUrl": "https://x/track.wav"}}

        wav = SunoClient(api_key="k").audio.get_wav("wav-1")
        self.assertIsInstance(wav, WavFile)
        self.assertEqual(wav.wav_url, "https://x/track.wav")
        mock_get_task_info.assert_called_once_with("wav-1", "/api/v1/wav/record-info")


if __name__ == "__main__":
    unittest.main()
