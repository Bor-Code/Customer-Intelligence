from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ci.models.forecasting import ForecastingModel

@pytest.fixture
def dummy_ts_data() -> pl.DataFrame:
    base = datetime(2023, 1, 1)
    dates = [base + timedelta(days=i) for i in range(20)]
    targets = [10.0 + float(i) + float(i % 3) for i in range(20)]
    return pl.DataFrame({"Date": dates, "Target": targets})

def test_forecasting_model_fit(dummy_ts_data: pl.DataFrame) -> None:
    model = ForecastingModel(lags=[1, 2], random_state=42)
    model.fit(dummy_ts_data)

    assert "rmse" in model.metrics

def test_forecasting_model_predict(dummy_ts_data: pl.DataFrame) -> None:
    model = ForecastingModel(lags=[1, 2], random_state=42)
    model.fit(dummy_ts_data)

    preds = model.predict(dummy_ts_data)
    assert len(preds) == len(dummy_ts_data) - 2

def test_forecasting_model_missing_columns() -> None:
    model = ForecastingModel()
    with pytest.raises(ValueError, match="must contain 'Date' and 'Target'"):
        model.fit(pl.DataFrame({"A": [1]}))

def test_forecasting_model_save_load(tmp_path: Path, dummy_ts_data: pl.DataFrame) -> None:
    model_path = tmp_path / "forecasting.joblib"
    model = ForecastingModel(lags=[1])
    model.fit(dummy_ts_data)

    model.save(model_path)
    loaded_model = ForecastingModel.load(model_path)

    assert isinstance(loaded_model, ForecastingModel)
    assert loaded_model.lags == model.lags

    preds_original = model.predict(dummy_ts_data)
    preds_loaded = loaded_model.predict(dummy_ts_data)
    np.testing.assert_array_equal(preds_original, preds_loaded)
