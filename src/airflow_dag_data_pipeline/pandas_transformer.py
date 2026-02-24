from datetime import date
from typing import Any

import pandas as pd

from airflow_dag_data_pipeline.weather_transformer import WeatherDataTransformer


class PandasWeatherDataTransformer(WeatherDataTransformer):
    """Concrete implementation of WeatherDataTransformer using pandas.
    Converts raw OpenWeather API response data into a DataFrame,
    calculates the mean daily temperature, and returns the results
    as a dictionary of {date_string: mean_temperature}."""

    def _filter_data(
        self, data: dict[date, dict[str, Any]], start_date: date, end_date: date
    ) -> dict[date, dict[str, Any]]:
        filtered_data = {
            d: response for d, response in data.items() if start_date <= d <= end_date
        }

        return filtered_data

    def _build_records(
        self, filtered_data: dict[date, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        try:
            records = [
                {
                    "date": str(d),
                    "morning": response["temperature"]["morning"],
                    "afternoon": response["temperature"]["afternoon"],
                    "evening": response["temperature"]["evening"],
                    "night": response["temperature"]["night"],
                }
                for d, response in filtered_data.items()
            ]
        except KeyError as e:
            field_name = e.args[0] if e.args else "unknown"
            raise ValueError(
                f"Missing expected temperature field: {field_name}"
            ) from e
        return records

    def get_mean_daily_temperature(
        self, data: dict[date, dict[str, Any]], start_date: date, end_date: date
    ) -> dict[str, float]:
        """Calculate mean daily temperature for a date range.

        Args:
            data: Dictionary of date objects to API response dicts
            start_date: Start of date range (inclusive)
            end_date: End of date range (inclusive)

        Returns:
            Dictionary mapping ISO format date strings (e.g. "2026-02-14")
            to mean daily temperature floats. Note: input keys are date
            objects but output keys are ISO format strings.

        Raises:
            ValueError: If no data exists in the given date range
            ValueError: If temperature fields are missing from the data
        """
        if start_date > end_date:
            raise ValueError(
                "Invalid date range: start_date must be less than or equal to end_date"
            )
        filtered_data = self._filter_data(data, start_date, end_date)

        if not filtered_data:
            raise ValueError(f"No data found between {start_date} and {end_date}")

        records = self._build_records(filtered_data)

        df = pd.DataFrame(records)
        temperature_columns = ["morning", "afternoon", "evening", "night"]
        df["mean_temp"] = df[temperature_columns].mean(axis=1)
        return {
            str(k): float(v)
            for k, v in df.set_index("date")["mean_temp"].to_dict().items()
        }
