"""
Entry point for fetching historical weather data from the OpenWeather
One Call API (Time Machine endpoint) and persisting the response locally.

This script:
- Reads configuration from environment variables
- Creates a configured HTTP session
- Fetches weather data for a fixed location and timestamp
- Writes the raw JSON response to disk

Intended for local experimentation and development.
"""

import json
import os

import requests
from rich import print as rprint
from weather_client import fetch_openweather_data

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}
DEFAULT_TIMEOUT = 10.0


def main() -> None:
    """
    Orchestrates retrieval of historical weather data from OpenWeather
    and saves the response to a local JSON file.

    Expects the environment variable OPENWEATHER_API_KEY to be set.
    """
    api_key = os.environ["OPENWEATHER_API_KEY"]

    params: dict[str, str | int | float] = {
        "lat": 54.9069,
        "lon": -1.3838,
        "appid": api_key,
        "dt": 1767830400,
        "units": "metric",
    }

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    weather_data = fetch_openweather_data(session, BASE_URL, params)

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, indent=2)

    rprint("Weather data saved to weather_data.json")
    rprint(weather_data)


if __name__ == "__main__":
    main()
