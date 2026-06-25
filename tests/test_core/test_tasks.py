import unittest
from unittest.mock import patch

from suno_easy import SunoClient, Task, TaskKind, RECORD_INFO_ENDPOINTS


class TestTask(unittest.TestCase):
    def test_task_str_and_repr(self):
        task = Task(
            task_id="abc123",
            kind=TaskKind.MUSIC,
            _client=SunoClient(api_key="k"),
            _parse=lambda d: [],
        )
        self.assertEqual(str(task), "abc123")
        self.assertEqual(task.task_id, "abc123")
        self.assertIn("music", repr(task))

    def test_wav_and_video_endpoints(self):
        self.assertEqual(RECORD_INFO_ENDPOINTS[TaskKind.WAV], "/api/v1/wav/record-info")
        self.assertEqual(RECORD_INFO_ENDPOINTS[TaskKind.VIDEO], "/api/v1/mp4/record-info")

        wav_task = Task(
            task_id="wav-1",
            kind=TaskKind.WAV,
            _client=SunoClient(api_key="k"),
            _parse=lambda d: d,
        )
        video_task = Task(
            task_id="vid-1",
            kind=TaskKind.VIDEO,
            _client=SunoClient(api_key="k"),
            _parse=lambda d: d,
        )
        self.assertEqual(wav_task.record_info_endpoint, "/api/v1/wav/record-info")
        self.assertEqual(video_task.record_info_endpoint, "/api/v1/mp4/record-info")

    @patch.object(SunoClient, "get_task_info")
    def test_wav_task_info_uses_correct_endpoint(self, mock_get_task_info):
        mock_get_task_info.return_value = {"status": "PENDING"}

        task = Task(
            task_id="wav-1",
            kind=TaskKind.WAV,
            _client=SunoClient(api_key="k"),
            _parse=lambda d: d,
        )
        task.info()

        mock_get_task_info.assert_called_once_with("wav-1", "/api/v1/wav/record-info")


if __name__ == "__main__":
    unittest.main()
