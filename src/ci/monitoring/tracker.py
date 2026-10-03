import hashlib
import subprocess
from contextlib import contextmanager
from typing import Generator

import mlflow
import polars as pl

from ci.config import get_config

def get_git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "unknown"

import io

def hash_dataframe(df: pl.DataFrame) -> str:
    if df.is_empty():
        return hashlib.sha256(b"empty").hexdigest()

    buf = io.BytesIO()
    df.write_ipc(buf)
    return hashlib.sha256(buf.getvalue()).hexdigest()

@contextmanager
def mlflow_run(experiment_name: str, run_name: str) -> Generator[mlflow.ActiveRun, None, None]:
    config = get_config()
    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.set_tag("git_sha", get_git_sha())
        yield run

def log_data_info(df: pl.DataFrame, dataset_name: str = "training_data") -> None:
    data_hash = hash_dataframe(df)
    mlflow.set_tag(f"{dataset_name}_hash", data_hash)
    mlflow.set_tag(f"{dataset_name}_shape", str(df.shape))
