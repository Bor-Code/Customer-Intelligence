from pathlib import Path

import polars as pl
import pytest

from ci.models.basket import BasketAnalysisModel

@pytest.fixture
def dummy_basket_data() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "Invoice": [1, 1, 1, 2, 2, 3, 3, 3, 4],
            "Description": ["A", "B", "C", "A", "C", "B", "C", "D", "A"],
        }
    )

def test_basket_model_fit(dummy_basket_data: pl.DataFrame) -> None:
    model = BasketAnalysisModel(min_support=0.2, min_confidence=0.5)
    model.fit(dummy_basket_data)

    assert model.frequent_itemsets is not None
    assert not model.frequent_itemsets.empty

    rules = model.get_rules()
    assert isinstance(rules, pl.DataFrame)

    assert not rules.is_empty()

def test_basket_model_missing_columns() -> None:
    model = BasketAnalysisModel()
    df = pl.DataFrame({"A": [1, 2]})
    with pytest.raises(ValueError, match="must contain 'Invoice' and 'Description'"):
        model.fit(df)

def test_basket_model_predict_raises(dummy_basket_data: pl.DataFrame) -> None:
    model = BasketAnalysisModel()
    model.fit(dummy_basket_data)
    with pytest.raises(NotImplementedError):
        model.predict(dummy_basket_data)

def test_basket_model_save_load(tmp_path: Path, dummy_basket_data: pl.DataFrame) -> None:
    model_path = tmp_path / "model.joblib"
    model = BasketAnalysisModel(min_support=0.2)
    model.fit(dummy_basket_data)

    model.save(model_path)
    loaded_model = BasketAnalysisModel.load(model_path)

    assert isinstance(loaded_model, BasketAnalysisModel)
    assert loaded_model.frequent_itemsets is not None
