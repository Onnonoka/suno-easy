import unittest

from suno_easy import (
    parse_webhook,
    parse_music_webhook,
    parse_lyrics_webhook,
    parse_wav_webhook,
    parse_video_webhook,
    parse_voice_validate_webhook,
    parse_voice_generate_webhook,
    parse_voice_regenerate_webhook,
    dispatch_webhook,
    Song,
    WavFile,
    MusicVideo,
    VoiceValidationInfo,
    CustomVoice,
    TaskFailed,
)


class TestWebhookParsers(unittest.TestCase):
    MUSIC_PAYLOAD = {
        "code": 200,
        "msg": "All generated successfully.",
        "data": {
            "callbackType": "complete",
            "task_id": "task-1",
            "data": [
                {
                    "id": "song-1",
                    "title": "Test Song",
                    "audio_url": "https://example.com/song.mp3",
                    "stream_audio_url": "https://example.com/stream",
                    "source_stream_audio_url": "https://example.com/source-stream",
                    "image_url": "https://example.com/cover.jpg",
                    "prompt": "[Verse] Hello",
                    "model_name": "chirp-v4",
                    "tags": "pop",
                    "createTime": "2025-01-01 00:00:00",
                    "duration": 120.0,
                }
            ],
        },
    }

    LYRICS_PAYLOAD = {
        "code": 200,
        "msg": "All generated successfully.",
        "data": {
            "callbackType": "complete",
            "taskId": "task-2",
            "data": [{"text": "[Verse]\nLine one", "title": "Lyric Title", "status": "complete"}],
        },
    }

    ERROR_PAYLOAD = {
        "code": 400,
        "msg": "Lyrics generation failed",
        "data": {"callbackType": "error", "taskId": "task-3", "data": None},
    }

    def test_parse_webhook_music_task_id(self):
        event = parse_webhook(self.MUSIC_PAYLOAD)
        self.assertEqual(event.task_id, "task-1")
        self.assertTrue(event.is_final)

    def test_parse_webhook_lyrics_task_id(self):
        event = parse_webhook(self.LYRICS_PAYLOAD)
        self.assertEqual(event.task_id, "task-2")

    def test_parse_music_webhook(self):
        event, songs = parse_music_webhook(self.MUSIC_PAYLOAD)
        self.assertEqual(len(songs), 1)
        self.assertIsInstance(songs[0], Song)
        self.assertEqual(songs[0].source_stream_url, "https://example.com/source-stream")

    def test_parse_lyrics_webhook(self):
        _, lyrics = parse_lyrics_webhook(self.LYRICS_PAYLOAD)
        self.assertEqual(lyrics[0].title, "Lyric Title")

    def test_parse_lyrics_webhook_error_raises(self):
        with self.assertRaises(TaskFailed):
            parse_lyrics_webhook(self.ERROR_PAYLOAD)

    def test_parse_wav_webhook(self):
        payload = {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "wav-1",
                "audioWavUrl": "https://example.com/track.wav",
            },
        }
        event, wav = parse_wav_webhook(payload)
        self.assertEqual(event.task_id, "wav-1")
        self.assertIsInstance(wav, WavFile)
        self.assertEqual(wav.wav_url, "https://example.com/track.wav")

    def test_parse_video_webhook(self):
        payload = {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "vid-1",
                "videoUrl": "https://example.com/track.mp4",
            },
        }
        event, video = parse_video_webhook(payload)
        self.assertEqual(event.task_id, "vid-1")
        self.assertIsInstance(video, MusicVideo)
        self.assertEqual(video.video_url, "https://example.com/track.mp4")

    def test_parse_wav_webhook_error_raises(self):
        payload = {
            "code": 400,
            "msg": "WAV conversion failed",
            "data": {"callbackType": "error", "taskId": "wav-err", "data": None},
        }
        with self.assertRaises(TaskFailed):
            parse_wav_webhook(payload)

    def test_dispatch_webhook_wav(self):
        payload = {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "wav-1",
                "audioWavUrl": "https://example.com/track.wav",
            },
        }
        _, result = dispatch_webhook(payload)
        self.assertIsInstance(result, WavFile)
        self.assertEqual(result.wav_url, "https://example.com/track.wav")

    def test_dispatch_webhook_video(self):
        payload = {
            "code": 200,
            "msg": "ok",
            "data": {
                "callbackType": "complete",
                "taskId": "vid-1",
                "videoUrl": "https://example.com/track.mp4",
            },
        }
        _, result = dispatch_webhook(payload)
        self.assertIsInstance(result, MusicVideo)
        self.assertEqual(result.video_url, "https://example.com/track.mp4")

    def test_parse_voice_validate_webhook(self):
        payload = {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v-task-1",
                "validateInfo": "Please record this validation phrase clearly.",
                "status": "wait_validating",
                "errorCode": 0,
                "errorMessage": "",
            },
        }
        event, info = parse_voice_validate_webhook(payload)
        self.assertEqual(event.task_id, "v-task-1")
        self.assertIsInstance(info, VoiceValidationInfo)
        self.assertEqual(info.validate_info, "Please record this validation phrase clearly.")

    def test_parse_voice_validate_webhook_error_raises(self):
        payload = {
            "code": 400,
            "msg": "Validation phrase generation failed",
            "data": {
                "taskId": "v-task-err",
                "validateInfo": "",
                "status": "processing_validate_fail",
                "errorCode": 500,
                "errorMessage": "Failed to generate validation phrase",
            },
        }
        with self.assertRaises(TaskFailed):
            parse_voice_validate_webhook(payload)

    def test_parse_voice_generate_webhook(self):
        payload = {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v-gen-1",
                "voiceId": "voice_abc",
                "status": "success",
                "errorCode": 0,
                "errorMessage": "",
            },
        }
        event, voice = parse_voice_generate_webhook(payload)
        self.assertEqual(event.task_id, "v-gen-1")
        self.assertIsInstance(voice, CustomVoice)
        self.assertEqual(voice.voice_id, "voice_abc")

    def test_parse_voice_regenerate_webhook(self):
        payload = {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v-task-1",
                "validateInfo": "Please record this new validation phrase clearly.",
                "status": "wait_validating",
            },
        }
        _, info = parse_voice_regenerate_webhook(payload)
        self.assertIsInstance(info, VoiceValidationInfo)

    def test_dispatch_webhook_voice_validate(self):
        payload = {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v-task-1",
                "validateInfo": "Sing this phrase",
                "status": "wait_validating",
            },
        }
        _, result = dispatch_webhook(payload)
        self.assertIsInstance(result, VoiceValidationInfo)

    def test_dispatch_webhook_voice_generate(self):
        payload = {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": "v-gen-1",
                "voiceId": "voice_abc",
                "status": "success",
            },
        }
        _, result = dispatch_webhook(payload)
        self.assertIsInstance(result, CustomVoice)


if __name__ == "__main__":
    unittest.main()
