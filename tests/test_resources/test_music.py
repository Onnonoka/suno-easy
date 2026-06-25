import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, ModelVersion, PersonaModel, VocalGender, Task, TaskKind


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

    @patch("requests.Session.post")
    def test_mashup_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "m1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.music.mashup(
                upload_urls=["https://a.com/1.mp3", "https://a.com/2.mp3"],
                style="Electronic",
                title="Mash",
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(len(payload["uploadUrlList"]), 2)
        self.assertIn("/api/v1/generate/mashup", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_generate_sounds(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "s1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.music.generate_sounds("ambient pad", sound_loop=True, wait=True)

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "V5")
        self.assertTrue(payload["soundLoop"])

    @patch("requests.Session.post")
    def test_generate_sounds_optional_params(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "s2"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.music.generate_sounds(
                "drum loop",
                sound_tempo=120,
                sound_key="C",
                grab_lyrics=True,
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["soundTempo"], 120)
        self.assertEqual(payload["soundKey"], "C")
        self.assertTrue(payload["grabLyrics"])

    @patch("requests.Session.post")
    def test_replace_section_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "r1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"sunoData": []}}):
            client.music.replace_section(
                task_id="task-1",
                audio_id="audio-1",
                prompt="New chorus lyrics",
                tags="Pop",
                title="Remixed",
                full_lyrics="[Verse] Old\n[Chorus] New",
                infill_start_s=30.0,
                infill_end_s=45.0,
                negative_tags="metal",
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["taskId"], "task-1")
        self.assertEqual(payload["audioId"], "audio-1")
        self.assertEqual(payload["infillStartS"], 30.0)
        self.assertEqual(payload["infillEndS"], 45.0)
        self.assertEqual(payload["negativeTags"], "metal")
        self.assertIn("/api/v1/generate/replace-section", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_mashup_wait_false_returns_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "m2"}}
        mock_post.return_value = mock_response

        task = SunoClient(api_key="k").music.mashup(
            upload_urls=["https://a.com/1.mp3"],
            wait=False,
        )
        self.assertIsInstance(task, Task)
        self.assertEqual(task.task_id, "m2")
        self.assertEqual(task.kind, TaskKind.MUSIC)


if __name__ == "__main__":
    unittest.main()
