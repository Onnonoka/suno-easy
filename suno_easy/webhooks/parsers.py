"""Parse Suno API webhook (callback) payloads on your server."""

from __future__ import annotations

from typing import Any

from ..exceptions import TaskFailed
from ..models import CoverImage, Lyrics, MIDIData, MusicVideo, SeparatedStems, Song, WavFile
from .events import WebhookEvent


def parse_webhook(payload: dict[str, Any]) -> WebhookEvent:
    """Parse the top-level webhook envelope from any Suno callback."""
    data = payload.get("data") or {}
    task_id = data.get("task_id") or data.get("taskId") or ""
    callback_type = data.get("callbackType") or data.get("callback_type") or ""

    return WebhookEvent(
        code=int(payload.get("code", 0)),
        message=str(payload.get("msg", "")),
        callback_type=str(callback_type),
        task_id=str(task_id),
        raw=payload,
    )


def _callback_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data") or {}
    items = data.get("data")
    if items is None:
        return []
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        return [items]
    return []


def _ensure_not_error(event: WebhookEvent) -> None:
    if event.is_error:
        raise TaskFailed(
            {
                "errorMessage": event.message,
                "taskId": event.task_id,
                "status": "FAILED",
            }
        )


def parse_music_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, list[Song]]:
    """Parse a music generation / extension callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    return event, [Song.from_callback_item(item) for item in _callback_items(payload)]


def parse_lyrics_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, list[Lyrics]]:
    """Parse a lyrics generation callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    return event, [Lyrics.from_callback_item(item) for item in _callback_items(payload)]


def parse_cover_image_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, CoverImage]:
    """Parse a cover image generation callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    items = _callback_items(payload)
    images = [item.get("image_url") or item.get("imageUrl") for item in items if item]
    images = [url for url in images if url]
    if not images:
        data = (payload.get("data") or {}).get("images") or []
        images = list(data)
    return event, CoverImage(images=images)


def parse_vocal_separation_webhook(
    payload: dict[str, Any],
) -> tuple[WebhookEvent, SeparatedStems]:
    """Parse a vocal separation callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    items = _callback_items(payload)
    source = items[0] if items else (payload.get("data") or {})
    return event, SeparatedStems.from_callback_data(source)


def parse_midi_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, MIDIData]:
    """Parse a MIDI generation callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    data = payload.get("data") or {}
    midi_source = data.get("midiData") or data.get("data") or data
    if isinstance(midi_source, list) and midi_source:
        midi_source = midi_source[0]
    return event, MIDIData.from_callback_data(midi_source if isinstance(midi_source, dict) else {})


def parse_wav_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, WavFile]:
    """Parse a WAV conversion callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    data = payload.get("data") or {}
    return event, WavFile.from_task_data(data if isinstance(data, dict) else {})


def parse_video_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, MusicVideo]:
    """Parse a music video generation callback."""
    event = parse_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    data = payload.get("data") or {}
    return event, MusicVideo.from_task_data(data if isinstance(data, dict) else {})


def dispatch_webhook(payload: dict[str, Any]) -> tuple[WebhookEvent, Any]:
    """Best-effort parser based on payload shape."""
    event = parse_webhook(payload)
    items = _callback_items(payload)

    if items and "text" in items[0]:
        return parse_lyrics_webhook(payload)
    if items and ("audio_url" in items[0] or "audioUrl" in items[0]):
        return parse_music_webhook(payload)
    data = payload.get("data") or {}
    if isinstance(data, dict):
        inner = data.get("response") or data
        if isinstance(inner, dict):
            if inner.get("audioWavUrl") or inner.get("audio_wav_url"):
                return parse_wav_webhook(payload)
            if inner.get("videoUrl") or inner.get("video_url"):
                return parse_video_webhook(payload)
    if event.is_error:
        _ensure_not_error(event)
    return event, payload.get("data")
