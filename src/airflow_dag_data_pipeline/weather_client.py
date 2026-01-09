from typing import Any

import requests

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}
DEFAULT_TIMEOUT = 10.0


def fetch_openweather_data(
    session: requests.Session,
    url: str,
    params: dict[str, str | int | float] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    Fetch JSON data from the OpenWeather API.

    Args:
        session: Configured requests Session object with headers
        url: The OpenWeather API endpoint URL
        params: Query parameters including lat, lon, appid, and dt
        timeout: Request timeout in seconds (default: 10.0)

    Returns:
        Dictionary containing the JSON response from the API

    Raises:
        requests.HTTPError: If the API request fails with a non-200 status
        requests.Timeout: If the request exceeds the timeout duration
        requests.RequestException: For other request-related errors
    """
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()
