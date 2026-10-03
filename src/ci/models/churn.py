from datetime import timedelta
from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import numpy as np
import polars as pl
from numpy.typing import NDArray
from sklearn.metrics import roc_auc_score

from ci.models.base import MiningModel

class ChurnModel(MiningModel):
    def __init__(self, random_state: int = 42) -> None:
        self.model = lgb.LGBMClassifier(random_state=random_state)
        self.metrics: dict[str, float] = {}

    def fit(self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None) -> "ChurnModel":
        if y is None:
            raise ValueError("Churn model requires target variable 'y'.")

        if "InvoiceDate" not in X.columns:
            raise ValueError("X must contain 'InvoiceDate' for temporal split.")

        max_date = X["InvoiceDate"].max()
        split_date = max_date - timedelta(days=30)

        is_train = X["InvoiceDate"] <= split_date

        features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)
        features = features_df.to_numpy()

        if isinstance(y, pl.Series):
            y_arr = y.to_numpy()
        else:
            y_arr = y

        mask = is_train.to_numpy()

        X_train, y_train = features[mask], y_arr[mask]
        X_test, y_test = features[~mask], y_arr[~mask]

        if len(set(y_test)) < 2:
            self.model.fit(X_train, y_train)
            self.metrics["roc_auc"] = 0.0
        else:
            self.model.fit(
                X_train,
                y_train,
                eval_set=[(X_test, y_test)],
            )
            preds = self.model.predict_proba(X_test)[:, 1]
            self.metrics["roc_auc"] = float(roc_auc_score(y_test, preds))

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)
        return self.model.predict(features_df.to_numpy())

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "ChurnModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
