from pathlib import Path
from typing import Any

import joblib
import numpy as np
import polars as pl
from numpy.typing import NDArray
from sklearn.ensemble import IsolationForest

from ci.models.base import MiningModel

class AnomalyDetectionModel(MiningModel):
    def __init__(self, contamination: float | str = "auto", random_state: int = 42) -> None:
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        self.metrics: dict[str, float] = {}

    def fit(
        self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None
    ) -> "AnomalyDetectionModel":
        features = X.drop(["Customer_ID"], strict=False).to_numpy()

        self.model.fit(features)

        preds = self.model.predict(features)
        anomalies_count = int(np.sum(preds == -1))

        self.metrics["train_anomalies"] = float(anomalies_count)
        self.metrics["train_total"] = float(len(features))

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        features = X.drop(["Customer_ID"], strict=False).to_numpy()
        return self.model.predict(features)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "AnomalyDetectionModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
