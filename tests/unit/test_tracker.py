from unittest.mock import MagicMock, patch

import polars as pl

from ci.monitoring.tracker import get_git_sha, hash_dataframe, log_data_info, mlflow_run

def test_get_git_sha_success() -> None:
    with patch("subprocess.check_output", return_value=b"abcdef123456\n"):
        sha = get_git_sha()
        assert sha == "abcdef123456"

def test_get_git_sha_failure() -> None:
    with patch("subprocess.check_output", side_effect=Exception("Git error")):
        sha = get_git_sha()
        assert sha == "unknown"

def test_hash_dataframe() -> None:
    df1 = pl.DataFrame({"a": [1, 2, 3]})
    df2 = pl.DataFrame({"a": [1, 2, 3]})
    df3 = pl.DataFrame({"a": [3, 2, 1]})

    hash1 = hash_dataframe(df1)
    hash2 = hash_dataframe(df2)
    hash3 = hash_dataframe(df3)

    assert hash1 == hash2
    assert hash1 != hash3

def test_hash_empty_dataframe() -> None:
    df = pl.DataFrame()
    h = hash_dataframe(df)
    assert isinstance(h, str)

@patch("ci.monitoring.tracker.mlflow")
@patch("ci.monitoring.tracker.get_config")
def test_mlflow_run_context(mock_get_config: MagicMock, mock_mlflow: MagicMock) -> None:
    mock_get_config.return_value.mlflow_tracking_uri = "sqlite:///test.db"

    with mlflow_run("test_exp", "test_run"):
        pass

    mock_mlflow.set_tracking_uri.assert_called_once_with("sqlite:///test.db")
    mock_mlflow.set_experiment.assert_called_once_with("test_exp")
    mock_mlflow.start_run.assert_called_once_with(run_name="test_run")
    mock_mlflow.set_tag.assert_called()

@patch("ci.monitoring.tracker.mlflow")
def test_log_data_info(mock_mlflow: MagicMock) -> None:
    df = pl.DataFrame({"a": [1]})
    log_data_info(df, "test_data")

    assert mock_mlflow.set_tag.call_count == 2
