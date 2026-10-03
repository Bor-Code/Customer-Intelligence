from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import polars as pl

def build_rfm(sales_parquet_path: Path, snapshot_date: datetime | None = None) -> pl.DataFrame:
    df = pl.read_parquet(sales_parquet_path)

    if df.is_empty():
        return pl.DataFrame(
            schema={
                "Customer_ID": pl.Int64,
                "Recency": pl.Int64,
                "Frequency": pl.UInt32,
                "Monetary": pl.Float64,
            }
        )

    if snapshot_date is None:
        max_date = df["InvoiceDate"].max()
        snapshot = max_date + timedelta(days=1)
    else:
        snapshot = snapshot_date

    rfm = (
        df.with_columns((pl.col("Price") * pl.col("Quantity")).alias("TotalSum"))
        .group_by("Customer_ID")
        .agg(
            [
                (snapshot - pl.col("InvoiceDate").max()).dt.total_days().alias("Recency"),
                pl.col("Invoice").n_unique().alias("Frequency"),
                pl.col("TotalSum").sum().alias("Monetary"),
            ]
        )
    )

    return rfm

def save_gold_features(df: pl.DataFrame, duckdb_path: Path, table_name: str) -> None:
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(duckdb_path)) as conn:
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
