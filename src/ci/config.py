from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class PathsConfig(BaseSettings):
    data_dir: Path = Field(default=Path("data"))
    bronze_dir: Path = Field(default=Path("data/bronze"))
    silver_dir: Path = Field(default=Path("data/silver"))
    gold_dir: Path = Field(default=Path("data/gold"))
    duckdb_path: Path = Field(default=Path("data/gold/ci.duckdb"))
    model_dir: Path = Field(default=Path("models"))

class AppConfig(BaseSettings):
    paths: PathsConfig = Field(default_factory=PathsConfig)
    mlflow_tracking_uri: str = Field(default="sqlite:///mlruns.db")

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

def get_config() -> AppConfig:
    return AppConfig()
