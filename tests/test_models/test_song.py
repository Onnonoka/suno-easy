import unittest

from suno_easy import Song


class TestSongModel(unittest.TestCase):
    def test_from_callback_item_camel_case(self):
        song = Song.from_callback_item(
            {
                "id": "1",
                "title": "Track",
                "audioUrl": "https://example.com/a.mp3",
                "streamAudioUrl": "https://example.com/s",
                "imageUrl": "https://example.com/i.jpg",
            }
        )
        self.assertEqual(song.audio_url, "https://example.com/a.mp3")
        self.assertEqual(song.stream_url, "https://example.com/s")

    def test_from_callback_item_snake_case(self):
        song = Song.from_callback_item(
            {
                "id": "1",
                "title": "Track",
                "audio_url": "https://example.com/a.mp3",
                "stream_audio_url": "https://example.com/s",
                "source_audio_url": "https://example.com/src.mp3",
            }
        )
        self.assertEqual(song.audio_url, "https://example.com/a.mp3")
        self.assertEqual(song.source_audio_url, "https://example.com/src.mp3")

    def test_from_task_data(self):
        songs = Song.from_task_data(
            {
                "response": {
                    "sunoData": [
                        {"id": "1", "title": "A", "audioUrl": "https://example.com/a.mp3"}
                    ]
                }
            }
        )
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, "A")


if __name__ == "__main__":
    unittest.main()
