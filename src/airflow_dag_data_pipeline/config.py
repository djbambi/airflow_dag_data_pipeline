import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OpenWeatherConfig:
    api_key: str
    timeout_s: float


def load_openweather_config() -> OpenWeatherConfig:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is not set")

    try:
        timeout_s = float(os.getenv("OPENWEATHER_TIMEOUT_S", "10"))
    except ValueError as exc:
        raise RuntimeError("OPENWEATHER_TIMEOUT_S must be a number") from exc

    if timeout_s <= 0:
        raise RuntimeError("OPENWEATHER_TIMEOUT_S must be > 0")

    return OpenWeatherConfig(
        api_key=api_key,
        timeout_s=timeout_s,
    )
