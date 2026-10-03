from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import polars as pl
from mlxtend.frequent_patterns import association_rules, fpgrowth
from numpy.typing import NDArray

from ci.models.base import MiningModel

class BasketAnalysisModel(MiningModel):
    def __init__(self, min_support: float = 0.01, min_confidence: float = 0.1) -> None:
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets: pd.DataFrame | None = None
        self.rules: pd.DataFrame | None = None

    def fit(
        self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None
    ) -> "BasketAnalysisModel":
        if "Invoice" not in X.columns or "Description" not in X.columns:
            raise ValueError("X must contain 'Invoice' and 'Description' columns.")

        df = X.select(["Invoice", "Description"]).drop_nulls()
        if df.is_empty():
            raise ValueError("Dataframe is empty after dropping nulls.")

        basket = (
            df.with_columns(pl.lit(1).alias("count"))
            .unique(subset=["Invoice", "Description"])
            .pivot(on="Description", index="Invoice", values="count")
            .fill_null(0)
            .drop("Invoice")
        )

        basket_pd = basket.to_pandas().astype(bool)

        self.frequent_itemsets = fpgrowth(
            basket_pd, min_support=self.min_support, use_colnames=True
        )

        if not self.frequent_itemsets.empty:
            self.rules = association_rules(
                self.frequent_itemsets,
                metric="confidence",
                min_threshold=self.min_confidence,
            )
        else:
            self.rules = pd.DataFrame()

        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        raise NotImplementedError(
            "Basket analysis does not support standard predict(). Use get_rules()."
        )

    def get_rules(self) -> pl.DataFrame:
        if self.rules is None:
            raise ValueError("Model is not fitted yet.")
        return pl.from_pandas(self.rules)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "BasketAnalysisModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
