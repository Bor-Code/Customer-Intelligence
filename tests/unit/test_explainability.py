from datetime import datetime, timedelta

import polars as pl

from ci.models.churn import ChurnModel
from ci.models.explainability import explain_churn_predictions

def test_explain_churn_predictions() -> None:
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

    model = ChurnModel(random_state=42)
    model.fit(X, y)

    explanation = explain_churn_predictions(model, X)

    assert "shap_values" in explanation
    assert "base_value" in explanation
    assert "feature_names" in explanation
    assert len(explanation["feature_names"]) == 3
    assert explanation["feature_names"] == ["Recency", "Frequency", "Monetary"]
    assert len(explanation["shap_values"]) == 6
