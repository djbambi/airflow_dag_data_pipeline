"""Tests for the weather client retry logic and API call behavior."""

from unittest.mock import Mock

import pytest
import requests
import requests_mock

from airflow_dag_data_pipeline.weather_client import _should_retry, api_call


@pytest.fixture
def test_url():
    """Provide a consistent test URL."""
    return "http://example.com/weather"


@pytest.fixture
def mock_session():
    """Provide a requests Session for testing."""
    return requests.Session()


@pytest.fixture
def successful_response(test_url):
    """Provide a mocked successful API response."""
    with requests_mock.Mocker() as m:
        expected_data = {"weather": "sunny", "temp": 20}
        m.get(test_url, status_code=200, json=expected_data)
        yield m, expected_data


def test_should_retry_on_timeout():
    """Timeout errors should be retried."""
    # Arrange: Create the exception
    exception = requests.Timeout()

    # Act: Call the function
    result = _should_retry(exception)

    # Assert: Check it returns True
    assert result is True


def test_should_retry_on_connection_error():
    """Connection errors should be retried."""
    # Arrange: Create the exception
    exception = requests.ConnectionError()

    # Act: Call the function
    result = _should_retry(exception)

    # Assert: Check it returns True
    assert result is True


@pytest.mark.parametrize("status_code", [408, 429, 500, 502, 503, 504])
def test_should_retry_on_retryable_http_status(status_code):
    """HTTP errors with retryable status codes should be retried."""
    # Arrange: Create HTTPError with the given status code
    exception = requests.HTTPError()
    exception.response = Mock(status_code=status_code)

    # Act: Call the function
    result = _should_retry(exception)

    # Assert: Check it returns True
    assert result is True


@pytest.mark.parametrize(
    "status_code", [pytest.param(400, id="Bad Request"), 401, 403, 404, 405]
)
def test_should_not_retry_on_client_error_status(status_code):
    """HTTP client errors (4xx) should NOT be retried."""
    # Arrange: Create HTTPError with the given status code
    exception = requests.HTTPError()
    exception.response = Mock(status_code=status_code)

    # Act: Call the function
    result = _should_retry(exception)

    # Assert: Check it returns False
    assert result is False


def test_api_call_returns_200_status(test_url, mock_session, successful_response):
    """Test that successful API call returns 200 status."""
    response = api_call(mock_session, test_url)
    assert response.status_code == 200


def test_api_call_returns_expected_json(test_url, mock_session, successful_response):
    """Test that successful API call returns expected JSON data."""
    m, expected_data = successful_response
    response = api_call(mock_session, test_url)
    assert response.json() == expected_data


def test_api_call_returns_weather_key(test_url, mock_session, successful_response):
    """Test that successful API call returns weather key in JSON."""
    m, expected_data = successful_response
    response = api_call(mock_session, test_url)
    assert "weather" in response.json()


def test_api_call_raises_for_status_with_requests_mock(test_url, mock_session):
    with requests_mock.Mocker() as m:
        m.get(test_url, status_code=503, text="service unavailable")

        with pytest.raises(requests.HTTPError):
            api_call(mock_session, test_url)
