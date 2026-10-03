from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ci.models.segmentation import RFMSegmentationModel, assign_segments

@pytest.fixture
def dummy_rfm_data() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5],
            "Recency": [10, 20, 1, 2, 30],
            "Frequency": [5, 1, 10, 8, 1],
            "Monetary": [100.0, 10.0, 500.0, 400.0, 20.0],
        }
    )

def test_rfm_segmentation_fit_predict(dummy_rfm_data: pl.DataFrame) -> None:
    model = RFMSegmentationModel(n_clusters=2, random_state=42)
    model.fit(dummy_rfm_data)

    assert "silhouette_score" in model.metrics

    preds = model.predict(dummy_rfm_data)

    assert len(preds) == 5
    assert preds[1] == -1
    assert preds[4] == -1
    assert preds[0] != -1
    assert preds[2] != -1
    assert preds[3] != -1

def test_assign_segments(dummy_rfm_data: pl.DataFrame) -> None:
    preds = np.array([0, -1, 1, 1, -1])
    df_with_seg = assign_segments(dummy_rfm_data, preds)

    assert "Segment" in df_with_seg.columns
    segs = df_with_seg["Segment"].to_list()
    assert segs[1] == "New Customer"
    assert segs[4] == "New Customer"
    assert segs[0] == "Cluster 0"
    assert segs[2] == "Cluster 1"

def test_model_save_load(tmp_path: Path, dummy_rfm_data: pl.DataFrame) -> None:
    model_path = tmp_path / "model.joblib"
    model = RFMSegmentationModel(n_clusters=2)
    model.fit(dummy_rfm_data)

    model.save(model_path)
    assert model_path.exists()

    loaded_model = RFMSegmentationModel.load(model_path)
    assert isinstance(loaded_model, RFMSegmentationModel)

    preds_original = model.predict(dummy_rfm_data)
    preds_loaded = loaded_model.predict(dummy_rfm_data)

    np.testing.assert_array_equal(preds_original, preds_loaded)
