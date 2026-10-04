from typing import Any

import mlflow
import pandas as pd
import polars as pl
from mlflow.pyfunc import PythonModel

from ci.models.base import MiningModel

class MiningPyfuncWrapper(PythonModel):
    def __init__(self, model: MiningModel) -> None:
        self.model = model

    def predict(self, context: Any, model_input: pd.DataFrame | pl.DataFrame) -> Any:
        if isinstance(model_input, pd.DataFrame):
            model_input = pl.from_pandas(model_input)

        if hasattr(self.model, "get_rules") and callable(getattr(self.model, "get_rules")):
            try:
                return self.model.predict(model_input)
            except NotImplementedError:
                return getattr(self.model, "get_rules")().to_pandas()

        preds = self.model.predict(model_input)
        if isinstance(preds, pl.DataFrame):
            return preds.to_pandas()
        return preds

def register_model(
    model: MiningModel, artifact_path: str, registered_model_name: str
) -> str:
    wrapper = MiningPyfuncWrapper(model)
    model_info = mlflow.pyfunc.log_model(
        artifact_path=artifact_path,
        python_model=wrapper,
        registered_model_name=registered_model_name,
    )
    return model_info.model_uri

def transition_model_stage(model_name: str, version: int, stage: str) -> None:
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=str(version),
        stage=stage,
        archive_existing_versions=True,
    )

def load_registered_model(model_name: str, stage: str = "Production") -> Any:
    model_uri = f"models:/{model_name}/{stage}"
    return mlflow.pyfunc.load_model(model_uri)
