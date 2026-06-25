from dataclasses import dataclass


@dataclass
class Persona:
    persona_id: str
    name: str
    description: str | None = None
    style: str | None = None

    @classmethod
    def from_api_data(cls, data: dict) -> "Persona":
        return cls(
            persona_id=data.get("personaId") or data.get("persona_id") or "",
            name=data.get("name", ""),
            description=data.get("description"),
            style=data.get("style"),
        )
