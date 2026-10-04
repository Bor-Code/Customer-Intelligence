from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ci.models.clv import CLVModel

@pytest.fixture
def dummy_clv_data() -> tuple[pl.DataFrame, pl.Series]:
    X = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5],
            "Recency": [10, 20, 15, 5, 2],
            "Frequency": [5, 1, 2, 10, 8],
            "Monetary": [100.0, 10.0, 30.0, 500.0, 400.0],
        }
    )
    y = pl.Series("future_value", [150.0, 0.0, 20.0, 600.0, 450.0])
    return X, y

def test_clv_model_fit_predict(dummy_clv_data: tuple[pl.DataFrame, pl.Series]) -> None:
    X, y = dummy_clv_data
    model = CLVModel(random_state=42)
    model.fit(X, y)

    assert "rmse" in model.metrics

    preds = model.predict(X)
    assert len(preds) == 5

def test_clv_model_missing_y(dummy_clv_data: tuple[pl.DataFrame, pl.Series]) -> None:
    X, _ = dummy_clv_data
    model = CLVModel()
    with pytest.raises(ValueError, match="requires target variable 'y'"):
        model.fit(X)

def test_clv_model_save_load(
    tmp_path: Path, dummy_clv_data: tuple[pl.DataFrame, pl.Series]
) -> None:
    model_path = tmp_path / "clv_model.joblib"
    X, y = dummy_clv_data
    model = CLVModel(random_state=42)
    model.fit(X, y)

    model.save(model_path)
    loaded_model = CLVModel.load(model_path)

    preds_original = model.predict(X)
    preds_loaded = loaded_model.predict(X)

    np.testing.assert_array_equal(preds_original, preds_loaded)
