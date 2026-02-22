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
    ) -> dict[str, float]:
        """Compute mean daily temperatures for a given date range.

        Implementations are expected to aggregate raw weather records for each
        calendar day between ``start_date`` and ``end_date`` (inclusive) and
        return the mean temperature per day.

        Args:
            data: Mapping from a calendar date to a dictionary of raw weather
                data for that day. The exact structure of the inner dictionary
                is implementation-specific but must contain sufficient
                information to derive a mean temperature for the day.
            start_date: The first date (inclusive) of the period for which mean
                daily temperatures should be computed.
            end_date: The last date (inclusive) of the period for which mean
                daily temperatures should be computed. Must be greater than or
                equal to ``start_date``.

        Returns:
            A mapping from ISO-formatted date strings (``YYYY-MM-DD``) to the
            corresponding mean temperature for that day, expressed in the
            temperature unit used by the underlying data source (for example,
            degrees Celsius or Kelvin).

        Raises:
            ValueError: If ``start_date`` is after ``end_date`` or if the
                requested date range cannot be satisfied from ``data``.
        """
        raise NotImplementedError
