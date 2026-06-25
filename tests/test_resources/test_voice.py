import unittest
from unittest.mock import MagicMock, patch

from suno_easy import (
    SunoClient,
    Task,
    TaskKind,
    VoiceValidationInfo,
    CustomVoice,
    VoiceCheck,
    VoiceLanguage,
    SingerSkillLevel,
    DEFAULT_CALLBACK_URL,
)


class TestVoiceResource(unittest.TestCase):
    @patch("requests.Session.post")
    def test_validate_payload_and_wait(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v-task-1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(
            client,
            "get",
            return_value={
                "code": 200,
                "data": {
                    "taskId": "v-task-1",
                    "validateInfo": "Harmonies fill the air",
                    "status": "wait_validating",
                },
            },
        ):
            info = client.voice.validate(
                "https://example.com/voice.mp3",
                vocal_start_s=0,
                vocal_end_s=10,
                language=VoiceLanguage.EN,
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["voiceUrl"], "https://example.com/voice.mp3")
        self.assertEqual(payload["language"], "en")
        self.assertEqual(payload["callBackUrl"], DEFAULT_CALLBACK_URL)
        self.assertIsInstance(info, VoiceValidationInfo)
        self.assertEqual(info.validate_info, "Harmonies fill the air")

    @patch("requests.Session.post")
    def test_validate_wait_false_returns_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v-task-2"}}
        mock_post.return_value = mock_response

        task = SunoClient(api_key="k").voice.validate(
            "https://example.com/voice.mp3",
            vocal_start_s=0,
            vocal_end_s=5,
            wait=False,
        )
        self.assertIsInstance(task, Task)
        self.assertEqual(task.kind, TaskKind.VOICE_VALIDATE)

    @patch("requests.Session.get")
    def test_get_validate_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {
            "code": 200,
            "data": {"taskId": "v-task-1", "validateInfo": "Phrase", "status": "wait_validating"},
        }
        mock_get.return_value = mock_response

        info = SunoClient(api_key="k").voice.get_validate_info("v-task-1")
        self.assertEqual(info.validate_info, "Phrase")
        self.assertEqual(mock_get.call_args.kwargs["params"]["taskId"], "v-task-1")

    @patch("requests.Session.post")
    def test_generate_payload_and_wait(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "voice-gen-1"}}
        mock_post.return_value = mock_response

        client = SunoClient(api_key="k")
        with patch.object(
            client,
            "get",
            return_value={
                "code": 200,
                "data": {"taskId": "voice-gen-1", "voiceId": "voice-123", "status": "success"},
            },
        ):
            voice = client.voice.generate(
                "v-task-1",
                "https://example.com/verify.mp3",
                voice_name="My Voice",
                singer_skill_level=SingerSkillLevel.ADVANCED,
                wait=True,
            )

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["verifyUrl"], "https://example.com/verify.mp3")
        self.assertEqual(payload["voiceName"], "My Voice")
        self.assertEqual(payload["singerSkillLevel"], "advanced")
        self.assertIsInstance(voice, CustomVoice)
        self.assertEqual(voice.voice_id, "voice-123")

    @patch("requests.Session.post")
    def test_regenerate_uses_cal_back_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"taskId": "v-task-3"}}
        mock_post.return_value = mock_response

        task_id = SunoClient(api_key="k", callback_url="https://hooks.example.com/voice").voice.regenerate(
            "v-task-1"
        )
        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["calBackUrl"], "https://hooks.example.com/voice")
        self.assertEqual(task_id, "v-task-3")

    @patch("requests.Session.post")
    def test_check_voice(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "{}"
        mock_response.json.return_value = {"code": 200, "data": {"isAvailable": True}}
        mock_post.return_value = mock_response

        check = SunoClient(api_key="k").voice.check("v-task-1")
        self.assertIsInstance(check, VoiceCheck)
        self.assertTrue(check.is_available)
        self.assertEqual(mock_post.call_args.kwargs["json"]["task_id"], "v-task-1")


if __name__ == "__main__":
    unittest.main()
