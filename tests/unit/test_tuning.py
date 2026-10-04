from datetime import datetime, timedelta

import polars as pl

from ci.models.tuning import optimize_churn_model

def test_optimize_churn_model() -> None:
    now = datetime(2023, 1, 10)
    X = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5, 6, 7, 8],
            "InvoiceDate": [
                now - timedelta(days=60),
                now - timedelta(days=45),
                now - timedelta(days=40),
                now - timedelta(days=35),
                now - timedelta(days=25),
                now - timedelta(days=10),
                now - timedelta(days=5),
                now - timedelta(days=2),
            ],
            "Recency": [10, 20, 15, 5, 2, 30, 10, 20],
            "Frequency": [5, 1, 2, 10, 8, 1, 5, 1],
            "Monetary": [100.0, 10.0, 30.0, 500.0, 400.0, 20.0, 100.0, 10.0],
        }
    )
    y = pl.Series("churn", [0, 1, 0, 0, 1, 1, 0, 1])

    best_params = optimize_churn_model(X, y, n_trials=2)
    assert "learning_rate" in best_params
    assert "num_leaves" in best_params
    assert "max_depth" in best_params
