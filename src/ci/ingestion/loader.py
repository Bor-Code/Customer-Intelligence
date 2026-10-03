from pathlib import Path
import pandas as pd
import polars as pl

def load_raw_data(file_path: Path) -> pl.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    try:
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            df = pl.read_csv(file_path)
        elif suffix in (".xls", ".xlsx"):
            df_pd = pd.read_excel(file_path)
            df = pl.from_pandas(df_pd)
        else:
            raise ValueError(f"Unsupported file extension: {suffix}")

        if df.is_empty():
            raise ValueError(f"The loaded dataset is empty: {file_path}")

        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load raw data from {file_path}: {e}") from e

def save_to_bronze(df: pl.DataFrame, output_path: Path) -> None:
    if df.is_empty():
        raise ValueError("Cannot save an empty dataframe to bronze layer.")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(output_path)
    except Exception as e:
        raise IOError(f"Failed to write bronze data to {output_path}: {e}") from e
