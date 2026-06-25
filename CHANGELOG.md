# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] — 2026-06-25

### Added

- **Phase 2:** `client.account`, `client.video`, timestamped lyrics, WAV conversion, style boost, mashup, replace section, sound generation.
- **Phase 3:** `client.upload.*` (URL, Base64, stream), `client.voice.*` (full custom voice workflow).
- Voice webhook parsers: `parse_voice_validate_webhook`, `parse_voice_generate_webhook`, `parse_voice_regenerate_webhook`.
- PEP 561 `py.typed` marker for static type checkers.
- GitHub Actions CI (Python 3.10, 3.12).
- Full documentation in `docs/` and smoke-test examples in `examples/`.

### Changed

- `wait=False` returns a `Task` handle instead of a bare string.
- `persona.create()` signature aligned with official API (`task_id`, `audio_id`, `description`).
- Default `callBackUrl` injected automatically via `DEFAULT_CALLBACK_URL`.

### Removed

- `music.remaster()` (endpoint not in official API).

## [0.1.0] — initial release

- Resource-oriented SDK for Suno API: music, lyrics, audio, persona.
- Polling, webhooks, typed models.

[0.2.0]: https://github.com/Onnonoka/suno-easy/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Onnonoka/suno-easy/releases/tag/v0.1.0
