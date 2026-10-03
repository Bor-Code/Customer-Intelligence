from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import polars as pl
from numpy.typing import NDArray

class MiningModel(ABC):
    @abstractmethod
    def fit(self, X: pl.DataFrame, y: pl.Series | NDArray[Any] | None = None) -> "MiningModel":
        pass

    @abstractmethod
    def predict(self, X: pl.DataFrame) -> NDArray[Any]:
        pass

    @abstractmethod
    def save(self, path: Path) -> None:
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> "MiningModel":
        pass
