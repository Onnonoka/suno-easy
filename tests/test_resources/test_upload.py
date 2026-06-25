import io
import unittest
from unittest.mock import MagicMock, patch

from suno_easy import SunoClient, UploadedFile, DEFAULT_UPLOAD_BASE_URL


UPLOAD_RESPONSE = {
    "success": True,
    "code": 200,
    "msg": "File uploaded successfully",
    "data": {
        "fileName": "track.mp3",
        "filePath": "audio/uploads/track.mp3",
        "downloadUrl": "https://tempfile.example.com/track.mp3",
        "fileSize": 2048,
        "mimeType": "audio/mpeg",
        "uploadedAt": "2025-01-01T12:00:00.000Z",
    },
}


class TestUploadResource(unittest.TestCase):
    def setUp(self):
        self.client = SunoClient(api_key="k")

    def test_default_upload_base_url(self):
        self.assertEqual(self.client.upload_base_url, DEFAULT_UPLOAD_BASE_URL)

    @patch("requests.Session.post")
    def test_upload_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = UPLOAD_RESPONSE
        mock_post.return_value = mock_response

        uploaded = self.client.upload.upload_url(
            "https://example.com/track.mp3",
            upload_path="audio/uploads",
            file_name="track.mp3",
        )
        self.assertIsInstance(uploaded, UploadedFile)
        self.assertEqual(uploaded.download_url, "https://tempfile.example.com/track.mp3")
        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["fileUrl"], "https://example.com/track.mp3")
        self.assertIn("/api/file-url-upload", mock_post.call_args.args[0])
        self.assertTrue(mock_post.call_args.args[0].startswith(DEFAULT_UPLOAD_BASE_URL))

    @patch("requests.Session.post")
    def test_upload_base64(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = UPLOAD_RESPONSE
        mock_post.return_value = mock_response

        uploaded = self.client.upload.upload_base64("aGVsbG8=", upload_path="audio/base64")
        self.assertIsInstance(uploaded, UploadedFile)
        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["base64Data"], "aGVsbG8=")
        self.assertIn("/api/file-base64-upload", mock_post.call_args.args[0])

    @patch("requests.Session.post")
    def test_upload_stream(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = UPLOAD_RESPONSE
        mock_post.return_value = mock_response

        uploaded = self.client.upload.upload_stream(
            io.BytesIO(b"audio-bytes"),
            upload_path="audio/stream",
            file_name="clip.mp3",
        )
        self.assertIsInstance(uploaded, UploadedFile)
        self.assertIn("/api/file-stream-upload", mock_post.call_args.args[0])
        self.assertIn("files", mock_post.call_args.kwargs)
        headers = mock_post.call_args.kwargs["headers"]
        self.assertNotIn("Content-Type", headers)


if __name__ == "__main__":
    unittest.main()
