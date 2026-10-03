from pathlib import Path
from unittest.mock import patch
import polars as pl

from ci.config import AppConfig, PathsConfig
from ci.pipelines.etl_flow import run_etl_flow

def test_run_etl_flow_end_to_end(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    bronze_dir = tmp_path / "bronze"
    silver_dir = tmp_path / "silver"

    data_dir.mkdir()

    raw_csv = data_dir / "test_data.csv"
    raw_csv.write_text("InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,Customer ID,Country\n536365,85123A,TEST,6,2010-12-01 08:26:00,2.55,17850,UK\nC536366,71053,TEST2,-1,2010-12-01 08:28:00,3.39,17850,UK\n")

    test_paths = PathsConfig(
        data_dir=data_dir,
        bronze_dir=bronze_dir,
        silver_dir=silver_dir,
        gold_dir=tmp_path / "gold",
        duckdb_path=tmp_path / "gold" / "ci.duckdb",
        model_dir=tmp_path / "models"
    )
    test_config = AppConfig(paths=test_paths)

    with patch("ci.pipelines.etl_flow.get_config", return_value=test_config):
        run_etl_flow(raw_file_name="test_data.csv")

    assert (bronze_dir / "raw_data.parquet").exists()
    assert (silver_dir / "sales.parquet").exists()
    assert (silver_dir / "returns.parquet").exists()

    sales_df = pl.read_parquet(silver_dir / "sales.parquet")
    returns_df = pl.read_parquet(silver_dir / "returns.parquet")

    assert sales_df.shape[0] == 1
    assert returns_df.shape[0] == 1
