from pathlib import Path
from typing import Any

import joblib
import numpy as np
import polars as pl
from numpy.typing import NDArray
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ci.models.base import MiningModel

class RFMSegmentationModel(MiningModel):
    def __init__(self, n_clusters: int = 4, random_state: int = 42) -> None:
        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "kmeans",
                    KMeans(
                        n_clusters=n_clusters,
                        random_state=random_state,
                        n_init="auto",
                    ),
                ),
            ]
        )
        self.metrics: dict[str, float] = {}

    def fit(self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None) -> "RFMSegmentationModel":
        X_train = X.filter(pl.col("Frequency") > 1)
        if X_train.is_empty():
            raise ValueError("No customers with Frequency > 1 available for training.")

        features = X_train.select(["Recency", "Frequency", "Monetary"]).to_numpy()
        self.pipeline.fit(features)

        preds = self.pipeline.predict(features)
        if len(set(preds)) > 1:
            self.metrics["silhouette_score"] = float(silhouette_score(features, preds))
        else:
            self.metrics["silhouette_score"] = -1.0

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        is_new = X["Frequency"] <= 1
        features = X.select(["Recency", "Frequency", "Monetary"]).to_numpy()

        kmeans_preds = np.full(len(X), -1, dtype=int)

        if not is_new.all():
            mask_existing = ~is_new.to_numpy()
            features_existing = features[mask_existing]
            kmeans_preds[mask_existing] = self.pipeline.predict(features_existing)

        return kmeans_preds

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "RFMSegmentationModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model

def assign_segments(df: pl.DataFrame, preds: NDArray[Any]) -> pl.DataFrame:
    segments = np.where(
        preds == -1, "New Customer", np.char.add("Cluster ", preds.astype(str))
    )
    return df.with_columns(pl.Series("Segment", segments))
