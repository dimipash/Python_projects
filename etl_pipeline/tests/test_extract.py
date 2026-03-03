import textwrap
from pathlib import Path

import pandas as pd
import pytest

from extract import EXPECTED_COLUMNS, extract


def write_csv(tmp_path, content):
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(textwrap.dedent(content).strip())
    return csv_path


def valid_csv():
    return """
        order_id,customer_name,product,quantity,unit_price,order_date,region
        1001,Alice,Laptop,2,999.99,2024-01-15,North
    """


class TestExtractFileErrors:
    def test_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            extract(tmp_path / "ghost.csv")

    def test_error_message_contains_path(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="ghost.csv"):
            extract(tmp_path / "ghost.csv")


class TestExtractColumnValidation:
    def test_raises_for_missing_column(self, tmp_path):
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date
            1001,Alice,Laptop,2,999.99,2024-01-15
        """,
        )
        with pytest.raises(ValueError):
            extract(csv)

    def test_error_names_missing_column(self, tmp_path):
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date
            1001,Alice,Laptop,2,999.99,2024-01-15
        """,
        )
        with pytest.raises(ValueError, match="region"):
            extract(csv)

    def test_extra_columns_allowed(self, tmp_path):
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region,extra
            1001,Alice,Laptop,2,999.99,2024-01-15,North,foo
        """,
        )
        df = extract(csv)
        assert "extra" in df.columns

    def test_expected_columns_constant(self):
        assert EXPECTED_COLUMNS == frozenset(
            {
                "order_id",
                "customer_name",
                "product",
                "quantity",
                "unit_price",
                "order_date",
                "region",
            }
        )


class TestExtractSuccess:
    def test_returns_dataframe(self, tmp_path):
        df = extract(write_csv(tmp_path, valid_csv()))
        assert isinstance(df, pd.DataFrame)

    def test_correct_row_count(self, tmp_path):
        df = extract(write_csv(tmp_path, valid_csv()))
        assert len(df) == 1

    def test_all_columns_present(self, tmp_path):
        df = extract(write_csv(tmp_path, valid_csv()))
        for col in EXPECTED_COLUMNS:
            assert col in df.columns

    def test_data_not_cleaned(self, tmp_path):
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,,Laptop,abc,999.99,not-a-date,North
        """,
        )
        df = extract(csv)
        assert len(df) == 1
        assert df.iloc[0]["quantity"] == "abc"
        assert pd.isna(df.iloc[0]["customer_name"])

    def test_multirow_csv(self, tmp_path):
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-16,South
            1003,Carol,Keyboard,1,79.99,2024-01-17,East
        """,
        )
        assert len(extract(csv)) == 3

    def test_accepts_pathlib_path(self, tmp_path):
        csv = write_csv(tmp_path, valid_csv())
        assert isinstance(csv, Path)
        assert len(extract(csv)) == 1
