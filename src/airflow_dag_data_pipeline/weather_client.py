"""Client to fetch weather data from OpenWeather API"""

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}


def fetch_openweather_data(
    *,
    session,
    url: str,
    params: dict,
    timeout_s: float,
) -> dict:
    response = session.get(url, params=params, timeout=timeout_s)
    response.raise_for_status()
    return response.json()
