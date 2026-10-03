from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import polars as pl

from ci.features.rfm import build_rfm, save_gold_features

def test_build_rfm(tmp_path: Path) -> None:
    sales_path = tmp_path / "sales.parquet"
    now = datetime(2023, 1, 10)
    data = {
        "Customer_ID": [1, 1, 2],
        "Invoice": ["A", "B", "C"],
        "InvoiceDate": [now - timedelta(days=5), now - timedelta(days=2), now - timedelta(days=10)],
        "Quantity": [2, 1, 5],
        "Price": [10.0, 20.0, 5.0],
    }
    pl.DataFrame(data).write_parquet(sales_path)

    snapshot = now + timedelta(days=1)
    rfm = build_rfm(sales_path, snapshot_date=snapshot)

    assert rfm.shape[0] == 2

    rfm_1 = rfm.filter(pl.col("Customer_ID") == 1).to_dicts()[0]
    assert rfm_1["Recency"] == 3
    assert rfm_1["Frequency"] == 2
    assert rfm_1["Monetary"] == 40.0

    rfm_2 = rfm.filter(pl.col("Customer_ID") == 2).to_dicts()[0]
    assert rfm_2["Recency"] == 11
    assert rfm_2["Frequency"] == 1
    assert rfm_2["Monetary"] == 25.0

def test_build_rfm_empty(tmp_path: Path) -> None:
    sales_path = tmp_path / "sales.parquet"
    pl.DataFrame(
        schema={
            "Customer_ID": pl.Int64,
            "Invoice": pl.Utf8,
            "InvoiceDate": pl.Datetime,
            "Quantity": pl.Int64,
            "Price": pl.Float64,
        }
    ).write_parquet(sales_path)

    rfm = build_rfm(sales_path)
    assert rfm.is_empty()
    assert "Recency" in rfm.columns

def test_save_gold_features(tmp_path: Path) -> None:
    db_path = tmp_path / "gold" / "ci.duckdb"
    df = pl.DataFrame({"Customer_ID": [1, 2], "Recency": [10, 20]})

    save_gold_features(df, db_path, "rfm")

    assert db_path.exists()

    with duckdb.connect(str(db_path)) as conn:
        result = conn.execute("SELECT * FROM rfm ORDER BY Customer_ID").pl()
        assert result.shape == (2, 2)
        assert result["Recency"].to_list() == [10, 20]
