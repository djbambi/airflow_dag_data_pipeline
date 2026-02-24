from datetime import date
from typing import Any

import pytest

from airflow_dag_data_pipeline import WeatherDataTransformer


class IncompleteTransformer(WeatherDataTransformer):
    pass  # deliberately doesn't implement get_mean_daily_temperature


class CompleteTransformer(WeatherDataTransformer):
    def get_mean_daily_temperature(
        self, data: dict[date, dict[str, Any]], start_date: date, end_date: date
    ) -> dict[str, float]:
        return {"2026-02-14": 7.6}  # dummy return value for testing


def test_cannot_instantiate_abc():
    with pytest.raises(TypeError):
        WeatherDataTransformer()


def test_incomplete_concrete_class_raises_error():
    with pytest.raises(TypeError):
        IncompleteTransformer()


def test_complete_concrete_class_can_be_instantiated():
    transformer = CompleteTransformer()
    assert isinstance(transformer, WeatherDataTransformer)
