import json

import requests

from airflow_dag_data_pipeline.config import Settings
from airflow_dag_data_pipeline.weather_client import (
    DEFAULT_HEADERS,
    fetch_openweather_data,
)


def main() -> None:
    settings = Settings()

    params: dict[str, str | int | float] = {
        "lat": 54.9069,
        "lon": -1.3838,
        "dt": 1767830400,
        "appid": settings.openweather_api_key,
        "units": "metric",
    }

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    data = fetch_openweather_data(
        session=session,
        url=str(settings.openweather_base_url),
        params=params,
        timeout_s=settings.openweather_timeout_s,
    )

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
