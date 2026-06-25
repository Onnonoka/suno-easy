# API coverage

The SDK covers **100 % of documented Suno REST endpoints** across three API hosts, plus **all documented webhook callback types**.

Official reference: [docs.sunoapi.org](https://docs.sunoapi.org/)

---

## File Upload API — 3/3

Host: `https://sunoapiorg.redpandaai.co` (`DEFAULT_UPLOAD_BASE_URL`)

| HTTP | Endpoint | SDK method |
|---|---|---|
| POST | `/api/file-url-upload` | `client.upload.upload_url()` |
| POST | `/api/file-base64-upload` | `client.upload.upload_base64()` |
| POST | `/api/file-stream-upload` | `client.upload.upload_stream()` |

No webhooks — uploads are synchronous. Files expire after **3 days**.

---

## Suno API — 25/25

Host: `https://api.sunoapi.org`

| HTTP | Endpoint | SDK method | Async |
|---|---|---|---|
| POST | `/api/v1/generate` | `client.music.generate()` | yes |
| POST | `/api/v1/generate/extend` | `client.music.extend()` | yes |
| POST | `/api/v1/generate/mashup` | `client.music.mashup()` | yes |
| POST | `/api/v1/generate/replace-section` | `client.music.replace_section()` | yes |
| POST | `/api/v1/generate/sounds` | `client.music.generate_sounds()` | yes |
| POST | `/api/v1/generate/upload-cover` | `client.audio.cover()` | yes |
| POST | `/api/v1/generate/upload-extend` | `client.audio.extend()` | yes |
| POST | `/api/v1/generate/add-vocals` | `client.audio.add_vocals()` | yes |
| POST | `/api/v1/generate/add-instrumental` | `client.audio.add_instrumental()` | yes |
| POST | `/api/v1/generate/generate-persona` | `client.persona.create()` | no |
| POST | `/api/v1/generate/get-timestamped-lyrics` | `client.lyrics.get_timestamped()` | no |
| GET | `/api/v1/generate/credit` | `client.account.get_credits()` | no |
| GET | `/api/v1/generate/record-info` | `client.music.get_task()` | — |
| POST | `/api/v1/lyrics` | `client.lyrics.generate()` | yes |
| GET | `/api/v1/lyrics/record-info` | `client.lyrics.get_task()` / `get()` | — |
| POST | `/api/v1/vocal-removal/generate` | `client.audio.separate_vocals()` | yes |
| GET | `/api/v1/vocal-removal/record-info` | `client.audio.get_vocal_separation_task()` | — |
| POST | `/api/v1/midi/generate` | `client.audio.generate_midi()` | yes |
| GET | `/api/v1/midi/record-info` | `client.audio.get_midi_task()` | — |
| POST | `/api/v1/wav/generate` | `client.audio.convert_wav()` | yes |
| GET | `/api/v1/wav/record-info` | `client.audio.get_wav_task()` | — |
| POST | `/api/v1/style/generate` | `client.audio.boost_style()` | no |
| POST | `/api/v1/suno/cover/generate` | `client.audio.generate_cover_image()` | yes |
| GET | `/api/v1/suno/cover/record-info` | `client.audio.get_cover_task()` | — |
| POST | `/api/v1/mp4/generate` | `client.video.create()` | yes |
| GET | `/api/v1/mp4/record-info` | `client.video.get_task()` | — |

Convenience parsers on completed tasks:

| SDK helper | Parses to |
|---|---|
| `client.audio.get_wav()` | `WavFile` |
| `client.audio.get_separated_stems()` | `SeparatedStems` |
| `client.audio.get_midi()` | `MIDIData` |
| `client.audio.get_cover_image()` | `CoverImage` |
| `client.video.get()` | `MusicVideo` |
| `client.lyrics.get()` | `list[Lyrics]` |

---

## Suno Voice API — 6/6

Host: `https://api.sunoapi.org`

| HTTP | Endpoint | SDK method | Async |
|---|---|---|---|
| POST | `/api/v1/voice/validate` | `client.voice.validate()` | yes |
| GET | `/api/v1/voice/validate-info` | `client.voice.get_validate_info()` | — |
| POST | `/api/v1/voice/generate` | `client.voice.generate()` | yes |
| GET | `/api/v1/voice/record-info` | `client.voice.get_record()` | — |
| POST | `/api/v1/voice/regenerate` | `client.voice.regenerate()` | callback |
| POST | `/api/v1/voice/check-voice` | `client.voice.check()` | no |

Note: `regenerate()` sends `calBackUrl` (typo in upstream API schema).

---

## Webhook parsers — all documented callbacks

| Callback type | Parser |
|---|---|
| Music generation / extension / mashup / sounds / replace / add vocals / add instrumental / upload cover / upload extend | `parse_music_webhook` |
| Lyrics generation | `parse_lyrics_webhook` |
| Cover image generation | `parse_cover_image_webhook` |
| Vocal separation | `parse_vocal_separation_webhook` |
| MIDI generation | `parse_midi_webhook` |
| WAV conversion | `parse_wav_webhook` |
| Music video | `parse_video_webhook` |
| Voice validation phrase | `parse_voice_validate_webhook` |
| Voice custom generation | `parse_voice_generate_webhook` |
| Voice phrase regeneration | `parse_voice_regenerate_webhook` |
| Auto-detect | `dispatch_webhook` |

Synchronous endpoints (`boost_style`, `get_credits`, `get_timestamped`, `check_voice`, file upload) have **no webhook** by design.

See [Webhooks](webhooks.md) for server integration examples.
