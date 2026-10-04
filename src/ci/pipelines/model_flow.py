import polars as pl
from prefect import flow, task

from ci.models.anomaly import AnomalyDetectionModel
from ci.models.segmentation import RFMSegmentationModel
from ci.monitoring.registry import register_model, transition_model_stage
from ci.monitoring.tracker import mlflow_run

@task
def train_segmentation(df: pl.DataFrame) -> None:
    if df.is_empty():
        return
    with mlflow_run("segmentation_training"):
        model = RFMSegmentationModel(n_clusters=3)
        model.fit(df)
        register_model(model, "segmentation_model", "RFMSegmentationModel")
        transition_model_stage("RFMSegmentationModel", 1, "Production")

@task
def train_anomaly(df: pl.DataFrame) -> None:
    if df.is_empty():
        return
    with mlflow_run("anomaly_training"):
        model = AnomalyDetectionModel(contamination=0.1)
        model.fit(df)
        register_model(model, "anomaly_model", "AnomalyDetectionModel")
        transition_model_stage("AnomalyDetectionModel", 1, "Production")

@flow(name="Model Training Flow")
def run_model_training() -> None:
    df = pl.DataFrame(
        {
            "Customer_ID": [1, 2, 3],
            "Recency": [10, 20, 30],
            "Frequency": [1, 2, 3],
            "Monetary": [100.0, 200.0, 300.0],
            "Return_Ratio": [0.0, 0.1, 0.0],
            "Refund_Ratio": [0.0, 0.05, 0.0],
        }
    )

    train_segmentation(df)
    train_anomaly(df)

if __name__ == "__main__":
    run_model_training()
