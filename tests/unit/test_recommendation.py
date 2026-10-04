from pathlib import Path

import polars as pl
import pytest

from ci.models.recommendation import RecommendationModel

@pytest.fixture
def dummy_reco_data() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "Customer_ID": [1, 1, 1, 2, 2, 3, 3, 4],
            "Description": ["A", "B", "C", "A", "B", "C", "D", "D"],
        }
    )

def test_reco_model_fit(dummy_reco_data: pl.DataFrame) -> None:
    model = RecommendationModel(n_components=2, random_state=42)
    model.fit(dummy_reco_data)

    assert model.item_factors is not None
    assert model.user_item_matrix is not None
    assert len(model.items) == 4

def test_reco_model_predict(dummy_reco_data: pl.DataFrame) -> None:
    model = RecommendationModel(n_components=2, random_state=42)
    model.fit(dummy_reco_data)

    test_input = pl.DataFrame({"Customer_ID": [1, 4, 999]})
    preds = model.predict(test_input)

    assert isinstance(preds, pl.DataFrame)
    assert "Customer_ID" in preds.columns
    assert "Recommendation" in preds.columns
    assert "Score" in preds.columns

    assert 999 not in preds["Customer_ID"].to_list()

def test_reco_model_missing_columns() -> None:
    model = RecommendationModel()
    with pytest.raises(ValueError, match="must contain 'Customer_ID' and 'Description'"):
        model.fit(pl.DataFrame({"A": [1]}))

def test_reco_model_save_load(tmp_path: Path, dummy_reco_data: pl.DataFrame) -> None:
    model_path = tmp_path / "reco_model.joblib"
    model = RecommendationModel()
    model.fit(dummy_reco_data)

    model.save(model_path)
    loaded_model = RecommendationModel.load(model_path)

    assert loaded_model.items == model.items
