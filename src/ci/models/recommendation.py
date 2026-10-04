from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import polars as pl
from numpy.typing import NDArray
from sklearn.decomposition import TruncatedSVD

from ci.models.base import MiningModel

class RecommendationModel(MiningModel):
    def __init__(self, n_components: int = 20, random_state: int = 42) -> None:
        self.n_components = n_components
        self.model = TruncatedSVD(n_components=n_components, random_state=random_state)
        self.user_item_matrix: pd.DataFrame | None = None
        self.item_factors: NDArray[Any] | None = None
        self.items: list[str] = []

    def fit(
        self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None
    ) -> "RecommendationModel":
        if "Customer_ID" not in X.columns or "Description" not in X.columns:
            raise ValueError("X must contain 'Customer_ID' and 'Description' columns.")

        df = X.select(["Customer_ID", "Description"]).drop_nulls()

        user_item = (
            df.with_columns(pl.lit(1).alias("purchase"))
            .group_by(["Customer_ID", "Description"])
            .sum()
            .pivot(values="purchase", index="Customer_ID", on="Description")
            .fill_null(0)
        )

        self.user_item_matrix = user_item.to_pandas().set_index("Customer_ID")
        self.items = list(self.user_item_matrix.columns)

        n_comps = min(self.n_components, len(self.items) - 1)
        if n_comps < 1:
            n_comps = 1

        self.model.set_params(n_components=n_comps)
        self.item_factors = self.model.fit_transform(self.user_item_matrix.T)

        return self

    def predict(self, X: pl.DataFrame) -> pl.DataFrame:
        if self.item_factors is None or self.user_item_matrix is None:
            raise ValueError("Model is not fitted yet.")

        if "Customer_ID" not in X.columns:
            raise ValueError("Prediction input must contain 'Customer_ID'.")

        customers = X["Customer_ID"].unique().to_list()
        recommendations = []

        norms = np.linalg.norm(self.item_factors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        item_factors_norm = self.item_factors / norms

        similarity_matrix = np.dot(item_factors_norm, item_factors_norm.T)

        for cust_id in customers:
            if cust_id not in self.user_item_matrix.index:
                continue

            user_history = self.user_item_matrix.loc[cust_id].to_numpy()
            scores = np.dot(user_history, similarity_matrix)
            scores[user_history > 0] = -1

            top_idx = np.argsort(scores)[::-1][:5]

            for idx in top_idx:
                if scores[idx] > 0:
                    recommendations.append(
                        {
                            "Customer_ID": cust_id,
                            "Recommendation": self.items[idx],
                            "Score": float(scores[idx]),
                        }
                    )

        if not recommendations:
            return pl.DataFrame(
                {"Customer_ID": pl.Int64, "Recommendation": pl.Utf8, "Score": pl.Float64}
            )

        return pl.DataFrame(recommendations)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> "RecommendationModel":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not an instance of {cls.__name__}")
        return model
