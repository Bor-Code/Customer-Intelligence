from pathlib import Path
import polars as pl

from ci.validation.schema import RetailSchema

def standardize_columns(df: pl.DataFrame) -> pl.DataFrame:
    mapping = {
        "InvoiceNo": "Invoice",
        "UnitPrice": "Price",
        "Customer ID": "Customer_ID",
    }
    rename_dict = {k: v for k, v in mapping.items() if k in df.columns}
    return df.rename(rename_dict)

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    df = standardize_columns(df)

    df_pd = df.to_pandas()
    validated_pd = RetailSchema.validate(df_pd)

    df_clean = pl.from_pandas(validated_pd)
    df_clean = df_clean.drop_nulls(subset=["Customer_ID"])
    df_clean = df_clean.with_columns(pl.col("Customer_ID").cast(pl.Int64))

    return df_clean

def separate_returns(df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    returns_mask = df["Invoice"].str.starts_with("C")

    df_returns = df.filter(returns_mask)
    df_sales = df.filter(~returns_mask)

    return df_sales, df_returns

def process_bronze_to_silver(
    bronze_path: Path,
    silver_sales_path: Path,
    silver_returns_path: Path
) -> None:
    if not bronze_path.exists():
        raise FileNotFoundError(f"Bronze data not found at {bronze_path}")

    df = pl.read_parquet(bronze_path)
    if df.is_empty():
        raise ValueError("Bronze dataset is empty.")

    df_clean = clean_data(df)
    df_sales, df_returns = separate_returns(df_clean)

    silver_sales_path.parent.mkdir(parents=True, exist_ok=True)
    silver_returns_path.parent.mkdir(parents=True, exist_ok=True)

    df_sales.write_parquet(silver_sales_path)
    df_returns.write_parquet(silver_returns_path)
