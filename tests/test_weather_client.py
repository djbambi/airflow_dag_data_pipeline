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
        yield expected_data


@pytest.mark.parametrize(
    "exception_type,exception_args",
    [
        pytest.param(requests.Timeout, {}, id="timeout"),
        pytest.param(requests.ConnectionError, {}, id="connection_error"),
    ],
)
def test_should_retry_on_network_errors(exception_type, exception_args):
    """Network errors (timeout, connection) should be retried."""
    # Arrange: Create the exception
    exception = exception_type(**exception_args)

    # Act: Call the function
    result = _should_retry(exception)

    # Assert: Check it returns True
    assert result is True


@pytest.mark.parametrize("status_code", [
    pytest.param(408, id="request_timeout"),
    pytest.param(429, id="too_many_requests"),
    pytest.param(500, id="internal_server_error"),
    pytest.param(502, id="bad_gateway"),
    pytest.param(503, id="service_unavailable"),
    pytest.param(504, id="gateway_timeout"),
])
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
    "status_code",
    [
        pytest.param(400, id="bad_request"),
        pytest.param(401, id="unauthorized"),
        pytest.param(403, id="forbidden"),
        pytest.param(404, id="not_found"),
        pytest.param(405, id="method_not_allowed"),
    ],
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
    expected_data = successful_response
    response = api_call(mock_session, test_url)
    assert response.status_code == 200


def test_api_call_returns_expected_json(test_url, mock_session, successful_response):
    """Test that successful API call returns expected JSON data."""
    expected_data = successful_response
    response = api_call(mock_session, test_url)
    assert response.json() == expected_data


def test_api_call_returns_weather_key(test_url, mock_session, successful_response):
    """Test that successful API call returns weather key in JSON."""
    _ = successful_response
    response = api_call(mock_session, test_url)
    assert "weather" in response.json()


def test_api_call_raises_for_status_with_requests_mock(test_url, mock_session):
    with requests_mock.Mocker() as m:
        m.get(test_url, status_code=503, text="service unavailable")

        with pytest.raises(requests.HTTPError):
            api_call(mock_session, test_url)
