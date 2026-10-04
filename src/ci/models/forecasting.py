from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import polars as pl
from numpy.typing import NDArray
from sklearn.metrics import root_mean_squared_error

from ci.models.base import MiningModel

class ForecastingModel(MiningModel):
    def __init__(self, random_state: int = 42, lags: list[int] | None = None) -> None:
        self.model = lgb.LGBMRegressor(random_state=random_state)
        self.lags = lags or [1, 2, 3, 7]
        self.metrics: dict[str, float] = {}

    def _create_lag_features(self, df: pl.DataFrame) -> pl.DataFrame:
        if "Date" not in df.columns or "Target" not in df.columns:
            raise ValueError("Data must contain 'Date' and 'Target' columns.")

        df = df.sort("Date")

        for lag in self.lags:
            df = df.with_columns(pl.col("Target").shift(lag).alias(f"lag_{lag}"))

        return df.drop_nulls()

    def fit(
        self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None
    ) -> "ForecastingModel":
        features_df = self._create_lag_features(X)

        y_train = features_df["Target"].to_numpy()
        X_train = features_df.drop(["Date", "Target"], strict=False).to_numpy()

        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_train)
        self.metrics["rmse"] = float(root_mean_squared_error(y_train, preds))

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        features_df = self._create_lag_features(X)
        X_test = features_df.drop(["Date", "Target"], strict=False).to_numpy()
        return self.model.predict(X_test)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "ForecastingModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
