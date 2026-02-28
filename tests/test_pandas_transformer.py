from datetime import date

import pytest

from airflow_dag_data_pipeline.pandas_transformer import PandasWeatherDataTransformer

SAMPLE_DATES_EXPECTED = [
    # Single date - first entry
    (
        date(2026, 2, 14),
        date(2026, 2, 14),
        {"2026-02-14": 5.0},  # (4.0 + 8.0 + 6.0 + 2.0) / 4
    ),
    # Single date - middle entry
    (
        date(2026, 2, 15),
        date(2026, 2, 15),
        {"2026-02-15": 5.75},  # (5.0 + 9.0 + 6.0 + 3.0) / 4
    ),
    # Single date - last entry
    (
        date(2026, 2, 16),
        date(2026, 2, 16),
        {"2026-02-16": 4.0},  # (3.0 + 7.0 + 5.0 + 1.0) / 4
    ),
    # Two consecutive dates
    (
        date(2026, 2, 14),
        date(2026, 2, 15),
        {"2026-02-14": 5.0, "2026-02-15": 5.75},
    ),
    # Full range
    (
        date(2026, 2, 14),
        date(2026, 2, 16),
        {"2026-02-14": 5.0, "2026-02-15": 5.75, "2026-02-16": 4.0},
    ),
    # Range wider than available data - should return all available dates
    (
        date(2026, 2, 1),
        date(2026, 2, 28),
        {"2026-02-14": 5.0, "2026-02-15": 5.75, "2026-02-16": 4.0},
    ),
]


@pytest.fixture
def transformer():
    return PandasWeatherDataTransformer()


@pytest.fixture
def sample_data():
    return {
        date(2026, 2, 14): {
            "temperature": {
                "morning": 4.0,
                "afternoon": 8.0,
                "evening": 6.0,
                "night": 2.0,
            }
        },
    }


@pytest.fixture
def sample_date_range_data():
    return {
        date(2026, 2, 14): {
            "temperature": {
                "morning": 4.0,
                "afternoon": 8.0,
                "evening": 6.0,
                "night": 2.0,
            }
        },
        date(2026, 2, 15): {
            "temperature": {
                "morning": 5.0,
                "afternoon": 9.0,
                "evening": 6.0,
                "night": 3.0,
            }
        },
        date(2026, 2, 16): {
            "temperature": {
                "morning": 3.0,
                "afternoon": 7.0,
                "evening": 5.0,
                "night": 1.0,
            }
        },
    }


# mean = (4.0 + 8.0 + 6.0 + 2.0) / 4 = 5.0


# --- Parametrized tests for get_mean_daily_temperature ---
# Each test case is: (start_date, end_date, expected_result)
# Using sample_date_range_data which has dates 2026-02-14, 2026-02-15, 2026-02-16
@pytest.mark.parametrize("start_date, end_date, expected", SAMPLE_DATES_EXPECTED)
def test_get_mean_daily_temperature_parametrized(
    sample_date_range_data, transformer, start_date, end_date, expected
):
    result = transformer.get_mean_daily_temperature(
        sample_date_range_data, start_date, end_date
    )
    assert result == expected


def test_returns_dict(sample_data, transformer):
    t = transformer.get_mean_daily_temperature(
        sample_data, date(2026, 2, 1), date(2026, 2, 28)
    )
    assert isinstance(t, dict)


def test_get_mean_daily_temperature_returns_correct_mean(sample_data, transformer):
    t = transformer.get_mean_daily_temperature(
        sample_data, date(2026, 2, 14), date(2026, 2, 14)
    )
    assert t == {"2026-02-14": 5.0}


def test_filter_data_excludes_dates_outside_range(sample_date_range_data, transformer):
    t = transformer._filter_data(
        sample_date_range_data, date(2026, 2, 15), date(2026, 2, 15)
    )
    assert t == {
        date(2026, 2, 15): {
            "temperature": {
                "morning": 5.0,
                "afternoon": 9.0,
                "evening": 6.0,
                "night": 3.0,
            }
        }
    }


def test_get_mean_daily_temperature_raises_value_error_for_empty_range(
    sample_data, transformer
):
    """Test that a ValueError is raised when no data exists in the date range."""
    with pytest.raises(ValueError):
        transformer.get_mean_daily_temperature(
            sample_data, date(2026, 3, 1), date(2026, 3, 7)
        )


def test_build_records_raises_value_error_for_missing_temperature_field(transformer):
    """Test that a ValueError is raised when temperature fields are missing."""
    invalid_data = {
        date(2026, 2, 14): {
            "temperature": {
                "morning": 4.0,
                # missing afternoon, evening, night
            }
        }
    }
    with pytest.raises(ValueError):
        transformer._build_records(invalid_data)


def test_get_mean_daily_temperature_returns_correct_means_for_date_range(
    sample_date_range_data, transformer
):
    t = transformer.get_mean_daily_temperature(
        sample_date_range_data, date(2026, 2, 14), date(2026, 2, 16)
    )
    assert t == {
        "2026-02-14": 5.0,  # (4.0 + 8.0 + 6.0 + 2.0) / 4
        "2026-02-15": 5.75,  # (5.0 + 9.0 + 6.0 + 3.0) / 4
        "2026-02-16": 4.0,  # (3.0 + 7.0 + 5.0 + 1.0) / 4
    }
