import unittest

from suno_easy import VoiceValidationInfo, CustomVoice, VoiceCheck


class TestVoiceModels(unittest.TestCase):
    def test_voice_validation_info_from_api_data(self):
        info = VoiceValidationInfo.from_api_data(
            {
                "taskId": "task-1",
                "validateInfo": "Sing this phrase tonight",
                "status": "wait_validating",
                "errorCode": 0,
                "errorMessage": "",
            }
        )
        self.assertEqual(info.task_id, "task-1")
        self.assertEqual(info.validate_info, "Sing this phrase tonight")
        self.assertEqual(info.status, "wait_validating")

    def test_custom_voice_from_api_data(self):
        voice = CustomVoice.from_api_data(
            {
                "taskId": "task-2",
                "voiceId": "voice-abc",
                "status": "success",
            }
        )
        self.assertEqual(voice.voice_id, "voice-abc")
        self.assertEqual(voice.status, "success")

    def test_voice_check_from_api_data(self):
        check = VoiceCheck.from_api_data({"isAvailable": True})
        self.assertTrue(check.is_available)


if __name__ == "__main__":
    unittest.main()
