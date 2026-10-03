from datetime import datetime
from pathlib import Path
import pytest
import polars as pl

from ci.validation.cleaner import clean_data, process_bronze_to_silver, separate_returns

def test_clean_data() -> None:
    raw_data = {
        "InvoiceNo": ["536365", "C536366", "536367"],
        "StockCode": ["85123A", "71053", "84406B"],
        "Description": ["TEST 1", "TEST 2", "TEST 3"],
        "Quantity": [6, -1, 8],
        "InvoiceDate": [datetime(2010, 12, 1, 8, 26), datetime(2010, 12, 1, 8, 28), datetime(2010, 12, 1, 8, 34)],
        "UnitPrice": [2.55, 3.39, 2.75],
        "Customer ID": [17850.0, 17850.0, None],
        "Country": ["United Kingdom", "United Kingdom", "United Kingdom"]
    }
    df = pl.DataFrame(raw_data)

    cleaned = clean_data(df)

    assert "Invoice" in cleaned.columns
    assert "Price" in cleaned.columns
    assert "Customer_ID" in cleaned.columns
    assert cleaned.shape[0] == 2
    assert cleaned["Customer_ID"].dtype == pl.Int64

def test_separate_returns() -> None:
    data = {
        "Invoice": ["536365", "C536366", "536367", "C536368"],
        "Value": [1, 2, 3, 4]
    }
    df = pl.DataFrame(data)

    sales, returns = separate_returns(df)

    assert sales.shape[0] == 2
    assert returns.shape[0] == 2
    assert all(not inv.startswith("C") for inv in sales["Invoice"])
    assert all(inv.startswith("C") for inv in returns["Invoice"])

def test_process_bronze_to_silver(tmp_path: Path) -> None:
    bronze_path = tmp_path / "bronze.parquet"
    sales_path = tmp_path / "sales.parquet"
    returns_path = tmp_path / "returns.parquet"

    raw_data = {
        "InvoiceNo": ["536365", "C536366"],
        "StockCode": ["85123A", "71053"],
        "Description": ["TEST", "TEST 2"],
        "Quantity": [6, -1],
        "InvoiceDate": [datetime(2010, 12, 1, 8, 26), datetime(2010, 12, 1, 8, 28)],
        "UnitPrice": [2.55, 3.39],
        "Customer ID": [17850.0, 17850.0],
        "Country": ["UK", "UK"]
    }
    pl.DataFrame(raw_data).write_parquet(bronze_path)

    process_bronze_to_silver(bronze_path, sales_path, returns_path)

    assert sales_path.exists()
    assert returns_path.exists()

    sales_df = pl.read_parquet(sales_path)
    returns_df = pl.read_parquet(returns_path)

    assert sales_df.shape[0] == 1
    assert returns_df.shape[0] == 1
