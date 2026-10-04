from unittest.mock import MagicMock, patch

import pandas as pd
import polars as pl

from ci.monitoring.registry import (
    MiningPyfuncWrapper,
    load_registered_model,
    register_model,
    transition_model_stage,
)

def test_mining_pyfunc_wrapper_standard() -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = ["test_pred"]

    wrapper = MiningPyfuncWrapper(mock_model)
    df_pd = pd.DataFrame({"A": [1]})

    preds = wrapper.predict(None, df_pd)
    assert preds == ["test_pred"]
    mock_model.predict.assert_called_once()

def test_mining_pyfunc_wrapper_basket() -> None:
    mock_model = MagicMock()
    mock_model.predict.side_effect = NotImplementedError()
    mock_model.get_rules.return_value = pl.DataFrame({"rule": ["A -> B"]})

    wrapper = MiningPyfuncWrapper(mock_model)
    df_pd = pd.DataFrame({"A": [1]})

    preds = wrapper.predict(None, df_pd)
    assert isinstance(preds, pd.DataFrame)
    assert "rule" in preds.columns
    mock_model.get_rules.assert_called_once()

@patch("ci.monitoring.registry.mlflow")
def test_register_model(mock_mlflow: MagicMock) -> None:
    mock_model = MagicMock()
    mock_mlflow.pyfunc.log_model.return_value.model_uri = "models:/test/1"

    uri = register_model(mock_model, "artifacts", "TestModel")
    assert uri == "models:/test/1"
    mock_mlflow.pyfunc.log_model.assert_called_once()

@patch("ci.monitoring.registry.mlflow")
def test_transition_model_stage(mock_mlflow: MagicMock) -> None:
    mock_client = MagicMock()
    mock_mlflow.tracking.MlflowClient.return_value = mock_client

    transition_model_stage("TestModel", 1, "Production")
    mock_client.transition_model_version_stage.assert_called_once_with(
        name="TestModel",
        version="1",
        stage="Production",
        archive_existing_versions=True,
    )

@patch("ci.monitoring.registry.mlflow")
def test_load_registered_model(mock_mlflow: MagicMock) -> None:
    mock_mlflow.pyfunc.load_model.return_value = MagicMock()
    model = load_registered_model("TestModel", "Staging")

    assert model is not None
    mock_mlflow.pyfunc.load_model.assert_called_once_with("models:/TestModel/Staging")
