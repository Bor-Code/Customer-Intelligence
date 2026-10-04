from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ci.features.anomaly import build_anomaly_features
from ci.models.anomaly import AnomalyDetectionModel

@pytest.fixture
def dummy_sales_returns() -> tuple[pl.DataFrame, pl.DataFrame]:
    sales = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3],
            "Invoice": ["A", "B", "C"],
            "Quantity": [10, 5, 2],
            "Price": [10.0, 20.0, 50.0],
        }
    )
    returns = pl.DataFrame(
        {
            "Customer_ID": [1, 3],
            "Invoice": ["C1", "C2"],
            "Quantity": [-2, -1],
            "Price": [10.0, 50.0],
        }
    )
    return sales, returns

def test_build_anomaly_features(dummy_sales_returns: tuple[pl.DataFrame, pl.DataFrame]) -> None:
    sales, returns = dummy_sales_returns
    features = build_anomaly_features(sales, returns)

    assert "Return_Ratio" in features.columns
    assert "Refund_Ratio" in features.columns

    f1 = features.filter(pl.col("Customer_ID") == 1).to_dicts()[0]
    assert f1["Return_Ratio"] == 0.5
    assert np.isclose(f1["Refund_Ratio"], 20 / 120)

    f2 = features.filter(pl.col("Customer_ID") == 2).to_dicts()[0]
    assert f2["Return_Ratio"] == 0.0
    assert f2["Refund_Ratio"] == 0.0

def test_anomaly_model_fit_predict() -> None:
    features = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5],
            "Return_Ratio": [0.0, 0.0, 0.1, 0.9, 0.0],
            "Refund_Ratio": [0.0, 0.0, 0.05, 0.95, 0.0],
        }
    )

    model = AnomalyDetectionModel(contamination=0.2, random_state=42)
    model.fit(features)

    assert "train_anomalies" in model.metrics

    preds = model.predict(features)
    assert len(preds) == 5
    assert preds[3] == -1

def test_anomaly_model_save_load(tmp_path: Path) -> None:
    features = pl.DataFrame(
        {
            "Customer_ID": [1, 2],
            "Return_Ratio": [0.0, 0.5],
            "Refund_Ratio": [0.0, 0.5],
        }
    )
    model = AnomalyDetectionModel()
    model.fit(features)

    model_path = tmp_path / "model.joblib"
    model.save(model_path)

    loaded = AnomalyDetectionModel.load(model_path)
    assert isinstance(loaded, AnomalyDetectionModel)
