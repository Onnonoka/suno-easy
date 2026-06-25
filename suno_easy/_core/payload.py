from __future__ import annotations

from typing import Union

from .types import ModelVersion, PersonaModel, VocalGender


def add_tuning_params(
    payload: dict,
    *,
    negative_tags: str | None = None,
    vocal_gender: Union[VocalGender, str, None] = None,
    style_weight: float | None = None,
    weirdness_constraint: float | None = None,
    audio_weight: float | None = None,
    persona_id: str | None = None,
    persona_model: Union[PersonaModel, str, None] = None,
) -> dict:
    """Append optional generation tuning fields to a request payload."""
    if negative_tags is not None:
        payload["negativeTags"] = negative_tags
    if vocal_gender is not None:
        payload["vocalGender"] = (
            vocal_gender.value if isinstance(vocal_gender, VocalGender) else vocal_gender
        )
    if style_weight is not None:
        payload["styleWeight"] = style_weight
    if weirdness_constraint is not None:
        payload["weirdnessConstraint"] = weirdness_constraint
    if audio_weight is not None:
        payload["audioWeight"] = audio_weight
    if persona_id is not None:
        payload["personaId"] = persona_id
    if persona_model is not None:
        payload["personaModel"] = (
            persona_model.value if isinstance(persona_model, PersonaModel) else persona_model
        )
    return payload


def model_value(model: Union[ModelVersion, str]) -> str:
    return model.value if isinstance(model, ModelVersion) else model
