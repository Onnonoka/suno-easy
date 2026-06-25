import unittest

from suno_easy import UploadedFile


class TestUploadedFileModel(unittest.TestCase):
    def test_from_api_data(self):
        uploaded = UploadedFile.from_api_data(
            {
                "fileName": "track.mp3",
                "filePath": "audio/uploads/track.mp3",
                "downloadUrl": "https://tempfile.example.com/track.mp3",
                "fileSize": 1024,
                "mimeType": "audio/mpeg",
                "uploadedAt": "2025-01-01T12:00:00.000Z",
            }
        )
        self.assertEqual(uploaded.file_name, "track.mp3")
        self.assertEqual(uploaded.download_url, "https://tempfile.example.com/track.mp3")
        self.assertEqual(uploaded.file_size, 1024)


if __name__ == "__main__":
    unittest.main()
