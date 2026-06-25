# client.persona

Create a reusable music Persona from an existing generated track.

## create

```python
persona = client.persona.create(
    task_id="music-generation-task-id",
    audio_id="song-audio-id",
    name="Bright Pop Voice",
    description="Upbeat pop vocals with clear articulation",
)

print(persona.persona_id)
```

**Returns:** `Persona` (synchronous)  
**Endpoint:** `POST /api/v1/generate/generate-persona`

Use the returned `persona_id` in `client.music.generate(..., persona_id=...)`.

## Breaking change (v0.2)

| v0.1 | v0.2 |
|---|---|
| `create(music_id, name)` | `create(task_id, audio_id, name, description, …)` |

## See also

- [client.music](music.md) — `persona_id` tuning parameter
- [Models](../models.md) — `Persona`
