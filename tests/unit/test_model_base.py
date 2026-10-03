from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
import pytest
from numpy.typing import NDArray

from ci.models.base import MiningModel

class DummyModel(MiningModel):
    def fit(self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None) -> "MiningModel":
        return self

    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        return np.zeros(len(X))

    def save(self, path: Path) -> None:
        pass

    @classmethod
    def load(cls, path: Path) -> "MiningModel":
        return cls()

def test_mining_model_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        MiningModel()  # type: ignore

def test_dummy_model_instantiation() -> None:
    model = DummyModel()
    assert isinstance(model, MiningModel)

def test_dummy_model_methods() -> None:
    model = DummyModel()
    X = pl.DataFrame({"A": [1, 2]})

    assert model.fit(X) is model

    preds = model.predict(X)
    assert len(preds) == 2
