from abc import ABC, abstractmethod
from datetime import date
from typing import Any


class WeatherDataTransformer(ABC):
    """Abstract base class for weather data transformers.
    Defines the interface for transforming raw OpenWeather API response data.
    All concrete implementations must implement get_mean_daily_temperature."""

    @abstractmethod
    def get_mean_daily_temperature(
        self, data: dict[date, dict[str, Any]], start_date: date, end_date: date
    ): ...
