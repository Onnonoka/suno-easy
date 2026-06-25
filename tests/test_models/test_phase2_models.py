import unittest

from suno_easy import (
    Credits,
    TimestampedLyrics,
    AlignedWord,
    StyleBoost,
    WavFile,
    MusicVideo,
)


class TestCreditsModel(unittest.TestCase):
    def test_from_api_data_int(self):
        credits = Credits.from_api_data(42)
        self.assertEqual(credits.remaining, 42)

    def test_from_api_data_dict(self):
        credits = Credits.from_api_data({"creditsRemaining": 100})
        self.assertEqual(credits.remaining, 100)


class TestTimestampedLyricsModel(unittest.TestCase):
    def test_from_api_data(self):
        result = TimestampedLyrics.from_api_data(
            {
                "alignedWords": [
                    {"word": "Hello", "startS": 0.1, "endS": 0.5, "success": True, "palign": 1}
                ],
                "waveformData": [0.0, 0.5, 1.0],
                "hootCer": 0.42,
                "isStreamed": True,
            }
        )
        self.assertEqual(len(result.aligned_words), 1)
        word = result.aligned_words[0]
        self.assertIsInstance(word, AlignedWord)
        self.assertEqual(word.word, "Hello")
        self.assertEqual(word.start_s, 0.1)
        self.assertEqual(word.palign, 1)
        self.assertEqual(result.waveform_data, [0.0, 0.5, 1.0])
        self.assertEqual(result.hoot_cer, 0.42)
        self.assertTrue(result.is_streamed)


class TestStyleBoostModel(unittest.TestCase):
    def test_from_api_data(self):
        boost = StyleBoost.from_api_data(
            {
                "taskId": "style-1",
                "result": "Enhanced pop",
                "creditsConsumed": 1.5,
                "creditsRemaining": 98.5,
                "successFlag": 1,
            }
        )
        self.assertEqual(boost.task_id, "style-1")
        self.assertEqual(boost.result, "Enhanced pop")
        self.assertEqual(boost.credits_consumed, 1.5)
        self.assertEqual(boost.success_flag, "1")


class TestWavFileModel(unittest.TestCase):
    def test_from_task_data_nested_response(self):
        wav = WavFile.from_task_data(
            {"taskId": "wav-1", "response": {"audioWavUrl": "https://example.com/a.wav"}}
        )
        self.assertEqual(wav.wav_url, "https://example.com/a.wav")
        self.assertEqual(wav.task_id, "wav-1")

    def test_from_task_data_flat_webhook(self):
        wav = WavFile.from_task_data({"taskId": "wav-2", "audioWavUrl": "https://example.com/b.wav"})
        self.assertEqual(wav.wav_url, "https://example.com/b.wav")


class TestMusicVideoModel(unittest.TestCase):
    def test_from_task_data_nested_response(self):
        video = MusicVideo.from_task_data(
            {"taskId": "vid-1", "response": {"videoUrl": "https://example.com/a.mp4"}}
        )
        self.assertEqual(video.video_url, "https://example.com/a.mp4")

    def test_from_task_data_flat_webhook(self):
        video = MusicVideo.from_task_data({"taskId": "vid-2", "videoUrl": "https://example.com/b.mp4"})
        self.assertEqual(video.video_url, "https://example.com/b.mp4")


if __name__ == "__main__":
    unittest.main()
