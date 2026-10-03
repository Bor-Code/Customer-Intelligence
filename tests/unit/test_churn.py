from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ci.models.churn import ChurnModel

@pytest.fixture
def dummy_churn_data() -> tuple[pl.DataFrame, pl.Series]:
    now = datetime(2023, 1, 10)
    X = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5, 6],
            "InvoiceDate": [
                now - timedelta(days=60),
                now - timedelta(days=45),
                now - timedelta(days=40),
                now - timedelta(days=25),
                now - timedelta(days=10),
                now - timedelta(days=5),
            ],
            "Recency": [10, 20, 15, 5, 2, 30],
            "Frequency": [5, 1, 2, 10, 8, 1],
            "Monetary": [100.0, 10.0, 30.0, 500.0, 400.0, 20.0],
        }
    )
    y = pl.Series("churn", [0, 1, 0, 0, 1, 1])
    return X, y

def test_churn_model_fit_predict(dummy_churn_data: tuple[pl.DataFrame, pl.Series]) -> None:
    X, y = dummy_churn_data
    model = ChurnModel(random_state=42)
    model.fit(X, y)

    assert "roc_auc" in model.metrics

    preds = model.predict(X)
    assert len(preds) == 6
    assert set(preds).issubset({0, 1})

def test_churn_model_missing_y(dummy_churn_data: tuple[pl.DataFrame, pl.Series]) -> None:
    X, _ = dummy_churn_data
    model = ChurnModel()
    with pytest.raises(ValueError, match="requires target variable 'y'"):
        model.fit(X)

def test_churn_model_missing_date(dummy_churn_data: tuple[pl.DataFrame, pl.Series]) -> None:
    X, y = dummy_churn_data
    X_no_date = X.drop("InvoiceDate")
    model = ChurnModel()
    with pytest.raises(ValueError, match="must contain 'InvoiceDate'"):
        model.fit(X_no_date, y)

def test_churn_model_save_load(tmp_path: Path, dummy_churn_data: tuple[pl.DataFrame, pl.Series]) -> None:
    model_path = tmp_path / "model.joblib"
    X, y = dummy_churn_data
    model = ChurnModel(random_state=42)
    model.fit(X, y)

    model.save(model_path)
    assert model_path.exists()

    loaded_model = ChurnModel.load(model_path)
    assert isinstance(loaded_model, ChurnModel)

    preds_original = model.predict(X)
    preds_loaded = loaded_model.predict(X)

    np.testing.assert_array_equal(preds_original, preds_loaded)
