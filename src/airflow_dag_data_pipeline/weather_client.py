"""Client to fetch weather data from OpenWeather API"""

from typing import Any

import requests

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}


def fetch_openweather_data(
    *,
    session: requests.Session,
    url: str,
    params: dict[str, str | int | float],
    timeout_s: float,
) -> dict[str, Any]:
    response = session.get(url, params=params, timeout=timeout_s)
    response.raise_for_status()
    return response.json() # type: ignore[no-any-return]
