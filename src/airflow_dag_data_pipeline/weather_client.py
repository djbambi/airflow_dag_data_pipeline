"""Client to fetch weather data from OpenWeather API"""

import platform
from typing import Any

import requests

from airflow_dag_data_pipeline import logger

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}

log = logger.get_logger(f"{platform.node()} - Some System")


def fetch_openweather_data(
    *,
    session: requests.Session,
    url: str,
    params: dict[str, str | int | float],
    timeout_s: float,
) -> dict[str, Any]:
    log.info("Fetching data from OpenWeather API.")
    response = session.get(url, params=params, timeout=timeout_s)
    response.raise_for_status()
    return response.json()  # type: ignore[no-any-return]
