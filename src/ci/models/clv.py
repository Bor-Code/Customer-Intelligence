from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import polars as pl
from numpy.typing import NDArray
from sklearn.metrics import root_mean_squared_error

from ci.models.base import MiningModel

class CLVModel(MiningModel):
    def __init__(self, random_state: int = 42) -> None:
        self.model = lgb.LGBMRegressor(random_state=random_state)
        self.metrics: dict[str, float] = {}

    def fit(self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None) -> "CLVModel":
        if y is None:
            raise ValueError("CLV model requires target variable 'y'.")

        features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)
        features = features_df.to_numpy()

        if isinstance(y, pl.Series):
            y_arr = y.to_numpy()
        else:
            y_arr = y

        self.model.fit(features, y_arr)

        preds = self.model.predict(features)
        self.metrics["rmse"] = float(root_mean_squared_error(y_arr, preds))

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)
        return self.model.predict(features_df.to_numpy())

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "CLVModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
