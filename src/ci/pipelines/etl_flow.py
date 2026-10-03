from pathlib import Path
from prefect import flow, task

from ci.config import get_config
from ci.ingestion.loader import load_raw_data, save_to_bronze
from ci.validation.cleaner import process_bronze_to_silver

@task(retries=2)
def extract_and_load_bronze(raw_file: Path, bronze_path: Path) -> None:
    df = load_raw_data(raw_file)
    save_to_bronze(df, bronze_path)

@task
def transform_and_load_silver(bronze_path: Path, sales_path: Path, returns_path: Path) -> None:
    process_bronze_to_silver(bronze_path, sales_path, returns_path)

@flow(name="Raw to Silver ETL")
def run_etl_flow(raw_file_name: str = "online_retail_II.xlsx") -> None:
    config = get_config()

    raw_file_path = config.paths.data_dir / raw_file_name
    bronze_path = config.paths.bronze_dir / "raw_data.parquet"
    silver_sales_path = config.paths.silver_dir / "sales.parquet"
    silver_returns_path = config.paths.silver_dir / "returns.parquet"

    extract_and_load_bronze(raw_file_path, bronze_path)
    transform_and_load_silver(bronze_path, silver_sales_path, silver_returns_path)

if __name__ == "__main__":
    run_etl_flow()
