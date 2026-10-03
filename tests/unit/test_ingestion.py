from pathlib import Path
import pytest
import polars as pl

from ci.ingestion.loader import load_raw_data, save_to_bronze

def test_load_raw_data_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("id,name\n1,Test\n")

    df = load_raw_data(csv_file)
    assert not df.is_empty()
    assert df.shape == (1, 2)
    assert df.columns == ["id", "name"]

def test_load_raw_data_empty_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("id,name\n")

    with pytest.raises(RuntimeError, match="The loaded dataset is empty"):
        load_raw_data(csv_file)

def test_load_raw_data_not_found(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        load_raw_data(missing_file)

def test_save_to_bronze(tmp_path: Path) -> None:
    df = pl.DataFrame({"id": [1, 2], "value": [10.0, 20.0]})
    output_path = tmp_path / "bronze" / "data.parquet"

    save_to_bronze(df, output_path)

    assert output_path.exists()
    df_loaded = pl.read_parquet(output_path)
    assert df_loaded.shape == (2, 2)

def test_save_empty_to_bronze(tmp_path: Path) -> None:
    df = pl.DataFrame({"id": [], "value": []})
    output_path = tmp_path / "bronze" / "data.parquet"

    with pytest.raises(ValueError, match="Cannot save an empty dataframe"):
        save_to_bronze(df, output_path)
