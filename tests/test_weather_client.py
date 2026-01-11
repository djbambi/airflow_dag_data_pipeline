# tests/test_weather_client.py
from unittest.mock import Mock

import pytest

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


def test_fetch_openweather_data_calls_session_get_with_expected_args() -> None:
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {}

    fake_session = Mock()
    fake_session.get.return_value = fake_response

    url = "https://example.com/weather"
    params = {"lat": 54.9, "lon": -1.3}
    timeout_s = 7.5

    fetch_openweather_data(
        session=fake_session,
        url=url,
        params=params,
        timeout_s=timeout_s,
    )

    fake_session.get.assert_called_once_with(url, params=params, timeout=timeout_s)


def test_fetch_openweather_data_raises_when_status_is_error() -> None:
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = Exception("HTTP error")

    fake_session = Mock()
    fake_session.get.return_value = fake_response

    with pytest.raises(Exception, match="HTTP error"):
        fetch_openweather_data(
            session=fake_session,
            url="https://example.com",
            params={},
            timeout_s=10.0,
        )

    fake_response.json.assert_not_called()
