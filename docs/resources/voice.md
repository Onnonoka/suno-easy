# client.voice

Suno Voice custom voice workflow — create a reusable `voiceId` from user recordings.

## Workflow overview

```text
validate → user records phrase → generate → check
     ↑                                    │
     └── regenerate (optional) ───────────┘
```

## validate

Generate a validation phrase from a segment of source audio.

```python
from suno_easy import VoiceLanguage

info = client.voice.validate(
    voice_url="https://example.com/source-vocal.mp3",
    vocal_start_s=0,
    vocal_end_s=10,
    language=VoiceLanguage.FR,
    wait=True,
)

print(info.validate_info)  # phrase the user must sing
print(info.task_id)        # keep for subsequent steps
```

**Returns:** `VoiceValidationInfo` or `Task[VoiceValidationInfo]`  
**Endpoint:** `POST /api/v1/voice/validate`

## get_validate_info

Poll validation phrase status manually.

```python
info = client.voice.get_validate_info("task-id")
```

**Endpoint:** `GET /api/v1/voice/validate-info`

Statuses: `wait_processing`, `processing_validate`, `wait_validating`, `success`, `fail`, …

## generate

Submit the user's verification recording (singing the phrase is recommended).

```python
from suno_easy import SingerSkillLevel

voice = client.voice.generate(
    task_id=info.task_id,
    verify_url="https://example.com/verification.mp3",
    voice_name="My Custom Voice",
    description="Warm pop vocal",
    style="Pop",
    singer_skill_level=SingerSkillLevel.INTERMEDIATE,
    wait=True,
)

print(voice.voice_id)
```

**Returns:** `CustomVoice` or `Task[CustomVoice]`  
**Endpoint:** `POST /api/v1/voice/generate`

## get_record

```python
voice = client.voice.get_record("task-id")
```

**Endpoint:** `GET /api/v1/voice/record-info`

## regenerate

Request a new validation phrase for an existing task.

```python
task_id = client.voice.regenerate(
    "task-id",
    callback_url="https://yourdomain.com/suno/voice-webhook",
)
```

**Returns:** `str` (task ID)  
**Endpoint:** `POST /api/v1/voice/regenerate`

Note: upstream API field is `calBackUrl` (typo), not `callBackUrl`.

## check

Verify whether the voice is ready for use.

```python
check = client.voice.check("task-id")
print(check.is_available)
```

**Returns:** `VoiceCheck` (synchronous)  
**Endpoint:** `POST /api/v1/voice/check-voice`

## Webhooks

| Step | Parser |
|---|---|
| Validation phrase ready | `parse_voice_validate_webhook` |
| Custom voice created | `parse_voice_generate_webhook` |
| Phrase regenerated | `parse_voice_regenerate_webhook` |

```python
from suno_easy import parse_voice_validate_webhook, parse_voice_generate_webhook

event, info = parse_voice_validate_webhook(body)
event, voice = parse_voice_generate_webhook(body)
```

## See also

- [Webhooks](../webhooks.md)
- [Enums](../enums.md) — `VoiceLanguage`, `SingerSkillLevel`
- [Models](../models.md) — `VoiceValidationInfo`, `CustomVoice`, `VoiceCheck`
- [client.upload](upload.md) — upload verification audio
