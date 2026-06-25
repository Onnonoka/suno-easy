import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, SunoAPIError, DEFAULT_CALLBACK_URL
from suno_easy.client import SunoClient as SunoClientClass
from suno_easy import TaskFailed


class TestSunoClient(unittest.TestCase):
    def setUp(self):
        self.client = SunoClient(api_key="test_key")

    def test_client_initialization(self):
        self.assertEqual(
            self.client.session.headers.get("Authorization"),
            "Bearer test_key",
        )
        self.assertEqual(self.client.BASE_URL, "https://api.sunoapi.org")
        self.assertEqual(self.client.callback_url, DEFAULT_CALLBACK_URL)

    def test_callback_url_on_client(self):
        client = SunoClient(api_key="k", callback_url="https://example.com/hook")
        self.assertEqual(client.resolve_callback_url(), "https://example.com/hook")
        self.assertEqual(
            client.resolve_callback_url("https://example.com/override"),
            "https://example.com/override",
        )

    def test_apply_callback_default_placeholder(self):
        payload = {"prompt": "test"}
        self.client.apply_callback(payload)
        self.assertEqual(payload["callBackUrl"], DEFAULT_CALLBACK_URL)

    @patch("requests.Session.post")
    def test_post_success_with_envelope(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "task_123"}}
        mock_post.return_value = mock_response

        res = self.client.post("/api/v1/generate", json={"prompt": "test"})
        self.assertEqual(res["data"]["taskId"], "task_123")

    @patch("requests.Session.post")
    def test_post_http_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.text = "Unauthorized access"
        mock_post.return_value = mock_response

        with self.assertRaises(SunoAPIError):
            self.client.post("/api/v1/generate", json={"prompt": "test"})

    @patch("requests.Session.post")
    def test_post_json_error_code(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = '{"code":401,"msg":"Unauthorized"}'
        mock_response.json.return_value = {"code": 401, "msg": "Unauthorized"}
        mock_post.return_value = mock_response

        with self.assertRaises(SunoAPIError) as ctx:
            self.client.post("/api/v1/lyrics", json={"prompt": "test"})

        self.assertEqual(ctx.exception.status_code, 401)


class TestWaitTask(unittest.TestCase):
    def test_task_failed_only_on_explicit_failure(self):
        client = SunoClient(api_key="k")
        self.assertFalse(client._task_failed({"status": "PENDING", "errorMessage": ""}))
        self.assertTrue(client._task_failed({"status": "FAILED"}))
        self.assertTrue(client._task_failed({"successFlag": -1}))

    def test_task_complete_stream_mode(self):
        client = SunoClient(api_key="k")
        res = {
            "response": {
                "sunoData": [{"id": "1", "streamAudioUrl": "https://stream.example.com"}]
            }
        }
        self.assertTrue(client._task_complete(res, "stream"))
        self.assertFalse(client._task_complete({"status": "PENDING"}, "complete"))

    @patch.object(SunoClientClass, "get_task_info")
    def test_wait_task_raises_task_failed(self, mock_get_task_info):
        client = SunoClient(api_key="k")
        mock_get_task_info.return_value = {"status": "FAILED", "errorMessage": "boom"}

        with self.assertRaises(TaskFailed):
            client.wait_task("task-1", poll_interval=0)


if __name__ == "__main__":
    unittest.main()
