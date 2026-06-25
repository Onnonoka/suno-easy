# Enums

Import from `suno_easy`:

```python
from suno_easy import (
    ModelVersion,
    PersonaModel,
    VocalGender,
    SeparationMode,
    SingerSkillLevel,
    VoiceLanguage,
)
```

## ModelVersion

AI model for music generation.

| Member | API value |
|---|---|
| `V4` | `V4` |
| `V4_5` | `V4_5` |
| `V4_5PLUS` | `V4_5PLUS` |
| `V4_5ALL` | `V4_5ALL` |
| `V5` | `V5` |
| `V5_5` | `V5_5` |

Default on most generation methods: `ModelVersion.V4_5ALL`.  
`generate_sounds` defaults to `ModelVersion.V5`.

## PersonaModel

| Member | API value |
|---|---|
| `STYLE` | `style_persona` |
| `VOICE` | `voice_persona` |

## VocalGender

| Member | API value |
|---|---|
| `MALE` | `m` |
| `FEMALE` | `f` |

## SeparationMode

| Member | API value |
|---|---|
| `SEPARATE_VOCAL` | `separate_vocal` |
| `SPLIT_STEM` | `split_stem` |

## SingerSkillLevel

Used by `client.voice.generate()`.

| Member | API value |
|---|---|
| `BEGINNER` | `beginner` |
| `INTERMEDIATE` | `intermediate` |
| `ADVANCED` | `advanced` |
| `PROFESSIONAL` | `professional` |

## VoiceLanguage

Used by `client.voice.validate()`.

| Member | Code |
|---|---|
| `EN` | `en` |
| `ZH` | `zh` |
| `ES` | `es` |
| `FR` | `fr` |
| `PT` | `pt` |
| `DE` | `de` |
| `JA` | `ja` |
| `KO` | `ko` |
| `HI` | `hi` |
| `RU` | `ru` |

String values are also accepted wherever enums are supported.
