from datetime import date

import pytest

from airflow_dag_data_pipeline.pandas_transformer import PandasWeatherDataTransformer


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
