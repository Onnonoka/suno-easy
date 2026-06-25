import unittest
from unittest.mock import MagicMock, patch
from suno_easy import SunoClient, SunoAPIError


class TestSunoClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.client = SunoClient(api_key=self.api_key)

    def test_client_initialization(self):
        """Test that the client is initialized with proper headers."""
        self.assertEqual(
            self.client.session.headers.get("Authorization"),
            f"Bearer {self.api_key}"
        )
        self.assertEqual(
            self.client.session.headers.get("Content-Type"),
            "application/json"
        )
        self.assertEqual(self.client.BASE_URL, "https://api.sunoapi.org")

    @patch("requests.Session.post")
    def test_post_success(self, mock_post):
        """Test successful POST request."""
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"status": "success", "data": {"id": "task_123"}}
        mock_post.return_value = mock_response

        res = self.client.post("/api/v1/generate", json={"prompt": "test"})
        
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["data"]["id"], "task_123")
        mock_post.assert_called_once_with(
            "https://api.sunoapi.org/api/v1/generate",
            json={"prompt": "test"}
        )

    @patch("requests.Session.post")
    def test_post_failure(self, mock_post):
        """Test failed POST request raising SunoAPIError."""
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.text = "Unauthorized access"
        mock_post.return_value = mock_response

        with self.assertRaises(SunoAPIError) as context:
            self.client.post("/api/v1/generate", json={"prompt": "test"})
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("Unauthorized access", str(context.exception))

    @patch("requests.Session.get")
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"status": "success", "data": "info"}
        mock_get.return_value = mock_response

        res = self.client.get("/api/v1/generate/record-info", params={"taskId": "task_123"})
        
        self.assertEqual(res["data"], "info")
        mock_get.assert_called_once_with(
            "https://api.sunoapi.org/api/v1/generate/record-info",
            params={"taskId": "task_123"}
        )


if __name__ == "__main__":
    unittest.main()
