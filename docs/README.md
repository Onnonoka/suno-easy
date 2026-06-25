# suno-easy documentation

Complete guide for the unofficial Python SDK for [Suno API](https://docs.sunoapi.org/).

## Contents

| Guide | Description |
|---|---|
| [Getting started](getting-started.md) | Installation, first call, environment variables |
| [Client configuration](client.md) | `SunoClient`, API hosts, authentication |
| [Tasks & polling](tasks-and-polling.md) | `Task`, `wait=True/False`, `wait_until="stream"` |
| [Webhooks](webhooks.md) | Callback parsers, `dispatch_webhook`, server integration |
| [API coverage](api-coverage.md) | Full endpoint ↔ SDK mapping (100 %) |
| [Models](models.md) | Dataclasses returned by the SDK |
| [Enums](enums.md) | `ModelVersion`, `VocalGender`, `VoiceLanguage`, … |
| [Errors](errors.md) | `SunoAPIError`, `TaskFailed`, handling patterns |

## Resources (API reference)

| Resource | Methods |
|---|---|
| [`client.music`](resources/music.md) | generate, extend, mashup, replace_section, sounds |
| [`client.lyrics`](resources/lyrics.md) | generate, get, get_timestamped |
| [`client.audio`](resources/audio.md) | cover, extend, stems, MIDI, WAV, style boost, … |
| [`client.persona`](resources/persona.md) | create |
| [`client.account`](resources/account.md) | get_credits |
| [`client.video`](resources/video.md) | create, get |
| [`client.upload`](resources/upload.md) | upload_url, upload_base64, upload_stream |
| [`client.voice`](resources/voice.md) | validate, generate, regenerate, check |

## External links

- [Official Suno API docs](https://docs.sunoapi.org/)
- [API key management](https://sunoapi.org/api-key)
- [Repository README](../README.md)
