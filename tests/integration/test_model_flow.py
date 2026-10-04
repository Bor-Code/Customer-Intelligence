from unittest.mock import MagicMock, patch

from ci.pipelines.model_flow import run_model_training

@patch("ci.pipelines.model_flow.mlflow_run")
@patch("ci.pipelines.model_flow.register_model")
@patch("ci.pipelines.model_flow.transition_model_stage")
def test_run_model_training(
    mock_trans: MagicMock, mock_reg: MagicMock, mock_run: MagicMock
) -> None:
    run_model_training()
    assert mock_reg.call_count == 2
    assert mock_trans.call_count == 2
