from enum import Enum


class ModelVersion(str, Enum):
    V4 = "V4"
    V4_5 = "V4_5"
    V4_5PLUS = "V4_5PLUS"
    V4_5ALL = "V4_5ALL"
    V5 = "V5"
    V5_5 = "V5_5"


class PersonaModel(str, Enum):
    STYLE = "style_persona"
    VOICE = "voice_persona"


class VocalGender(str, Enum):
    MALE = "m"
    FEMALE = "f"


class SeparationMode(str, Enum):
    SEPARATE_VOCAL = "separate_vocal"
    SPLIT_STEM = "split_stem"
