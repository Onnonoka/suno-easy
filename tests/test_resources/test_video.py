import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, MusicVideo, Task, TaskKind


class TestVideoResource(unittest.TestCase):
    @patch.object(SunoClient, "get_task_info")
    def test_get_task_uses_video_endpoint(self, mock_get_task_info):
        mock_get_task_info.return_value = {"status": "SUCCESS", "response": {"videoUrl": "https://x/v.mp4"}}

        client = SunoClient(api_key="k")
        task_data = client.video.get_task("vid-1")

        mock_get_task_info.assert_called_once_with("vid-1", "/api/v1/mp4/record-info")
        self.assertEqual(task_data["status"], "SUCCESS")

    @patch.object(SunoClient, "get_task_info")
    def test_get_parses_music_video(self, mock_get_task_info):
        mock_get_task_info.return_value = {"response": {"videoUrl": "https://x/v.mp4"}}

        video = SunoClient(api_key="k").video.get("vid-1")
        self.assertIsInstance(video, MusicVideo)
        self.assertEqual(video.video_url, "https://x/v.mp4")

    @patch("requests.Session.post")
    def test_create_with_optional_fields(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(client, "wait_task", return_value={"response": {"videoUrl": "https://x/v.mp4"}}):
            client.video.create(
                "task-1",
                "audio-1",
                author="Artist",
                domain_name="example.com",
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["author"], "Artist")
        self.assertEqual(payload["domainName"], "example.com")
        self.assertIn("/api/v1/mp4/generate", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_create_wait_false_returns_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v1"}}
        mock_post.return_value = mock_response

        task = SunoClient(api_key="k").video.create("task-1", "audio-1", wait=False)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.task_id, "v1")
        self.assertEqual(task.kind, TaskKind.VIDEO)


if __name__ == "__main__":
    unittest.main()
