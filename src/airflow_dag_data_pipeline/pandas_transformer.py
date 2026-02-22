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

    def _build_records(self, filtered_data: dict) -> list[dict[str, Any]]:
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
        return records

    def get_mean_daily_temperature(
        self, data: dict[date, dict[str, Any]], start_date: date, end_date: date
    ) -> dict[str, float]:
        filtered_data = self._filter_data(data, start_date, end_date)

        records = self._build_records(filtered_data)

        df = pd.DataFrame(records)
        temperature_columns = ["morning", "afternoon", "evening", "night"]
        df["mean_temp"] = df[temperature_columns].mean(axis=1)
        return {str(k): float(v) for k, v in df.set_index("date")["mean_temp"].items()}
