from dataclasses import dataclass


@dataclass
class Credits:
    remaining: int

    @classmethod
    def from_api_data(cls, data: int | dict) -> "Credits":
        if isinstance(data, dict):
            value = data.get("creditsRemaining") or data.get("remaining") or data.get("data") or 0
            return cls(remaining=int(value))
        return cls(remaining=int(data))
