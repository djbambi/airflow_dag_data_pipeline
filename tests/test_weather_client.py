# tests/test_weather_client.py
from unittest.mock import Mock

from airflow_dag_data_pipeline.weather_client import fetch_openweather_data


def test_fetch_openweather_data_returns_json_on_success() -> None:
    # Arrange: create a fake response
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"ok": True}

    # Arrange: create a fake session that returns the fake response
    fake_session = Mock()
    fake_session.get.return_value = fake_response

    # Act: call the function under test
    result = fetch_openweather_data(
        session=fake_session,
        url="https://example.com",
        params={"a": 1},
        timeout_s=10.0,
    )

    # Assert: we got back the JSON dict
    assert result == {"ok": True}