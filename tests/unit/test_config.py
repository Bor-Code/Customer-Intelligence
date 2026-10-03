import os
from pathlib import Path

from ci.config import AppConfig, PathsConfig, get_config

def test_default_config() -> None:
    config = get_config()
    assert isinstance(config, AppConfig)
    assert isinstance(config.paths, PathsConfig)
    assert config.paths.data_dir == Path("data")
    assert config.paths.bronze_dir == Path("data/bronze")
    assert config.mlflow_tracking_uri == "sqlite:///mlruns.db"

def test_env_override() -> None:
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
    os.environ["PATHS__DATA_DIR"] = "custom_data"

    config = get_config()

    assert config.mlflow_tracking_uri == "http://localhost:5000"
    assert config.paths.data_dir == Path("custom_data")

    del os.environ["MLFLOW_TRACKING_URI"]
    del os.environ["PATHS__DATA_DIR"]
