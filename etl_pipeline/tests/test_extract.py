import textwrap
from pathlib import Path

import pandas as pd
import pytest

from extract import EXPECTED_COLUMNS, extract

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_csv(tmp_path: Path, content: str) -> Path:
    """
    Write a CSV string to a temp file and return its Path.

    textwrap.dedent strips leading indentation from the triple-quoted string,
    so tests can indent CSV content for readability without that whitespace
    ending up in the file.
    """
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(textwrap.dedent(content).strip())
    return csv_path


def valid_csv_content() -> str:
    """Return a minimal valid CSV with all expected columns."""
    return """
        order_id,customer_name,product,quantity,unit_price,order_date,region
        1001,Alice,Laptop,2,999.99,2024-01-15,North
    """


# ===========================================================================
# File-level errors
# ===========================================================================


class TestExtractFileErrors:
    def test_raises_file_not_found_for_missing_file(self, tmp_path):
        """
        extract() should raise FileNotFoundError — not KeyError or AttributeError —
        when the file doesn't exist. The error type matters for the pipeline's
        error handling in pipeline.py.
        """
        missing = tmp_path / "does_not_exist.csv"
        with pytest.raises(FileNotFoundError):
            extract(missing)

    def test_error_message_contains_path(self, tmp_path):
        """The FileNotFoundError message should include the path that was attempted."""
        missing = tmp_path / "ghost.csv"
        with pytest.raises(FileNotFoundError, match="ghost.csv"):
            extract(missing)


# ===========================================================================
# Column validation errors
# ===========================================================================


class TestExtractColumnValidation:
    def test_raises_value_error_for_missing_column(self, tmp_path):
        """
        A CSV that's missing one expected column should raise ValueError,
        not a generic KeyError from inside pandas.
        """
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date
            1001,Alice,Laptop,2,999.99,2024-01-15
        """,
        )
        # 'region' column is missing
        with pytest.raises(ValueError):
            extract(csv)

    def test_error_message_names_missing_column(self, tmp_path):
        """The ValueError message should tell the developer which column is missing."""
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date
            1001,Alice,Laptop,2,999.99,2024-01-15
        """,
        )
        with pytest.raises(ValueError, match="region"):
            extract(csv)

    def test_raises_for_multiple_missing_columns(self, tmp_path):
        """A CSV missing multiple columns should still raise ValueError."""
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name
            1001,Alice
        """,
        )
        with pytest.raises(ValueError):
            extract(csv)

    def test_extra_columns_are_allowed(self, tmp_path):
        """
        A CSV with extra columns beyond EXPECTED_COLUMNS should not raise.
        We only enforce that the required columns are present, not that no
        extras exist. Real data sources often add columns over time.
        """
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region,extra_col
            1001,Alice,Laptop,2,999.99,2024-01-15,North,some_value
        """,
        )
        df = extract(csv)  # should not raise
        assert "extra_col" in df.columns

    def test_expected_columns_constant_is_correct(self):
        """Verify EXPECTED_COLUMNS matches our known schema."""
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


# ===========================================================================
# Successful extraction
# ===========================================================================


class TestExtractSuccess:
    def test_returns_dataframe(self, tmp_path):
        """extract() should return a pandas DataFrame."""
        csv = write_csv(tmp_path, valid_csv_content())
        result = extract(csv)
        assert isinstance(result, pd.DataFrame)

    def test_correct_row_count(self, tmp_path):
        """Row count in the DataFrame should match rows in the CSV (excl. header)."""
        csv = write_csv(tmp_path, valid_csv_content())
        result = extract(csv)
        assert len(result) == 1

    def test_all_expected_columns_present(self, tmp_path):
        """The returned DataFrame should contain all expected columns."""
        csv = write_csv(tmp_path, valid_csv_content())
        result = extract(csv)
        for col in EXPECTED_COLUMNS:
            assert col in result.columns, f"Expected column missing: {col}"

    def test_data_is_not_cleaned(self, tmp_path):
        """
        extract() must return raw data as-is. If the CSV contains a null
        or a string in a numeric column, extract() should NOT remove or fix it —
        that's transform()'s job. This test guards against accidentally mixing
        the two responsibilities.
        """
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,,Laptop,abc,999.99,not-a-date,North
        """,
        )
        result = extract(csv)
        # Row should still be there — extract() doesn't clean
        assert len(result) == 1
        assert result.iloc[0]["quantity"] == "abc"
        assert pd.isna(result.iloc[0]["customer_name"])

    def test_multirow_csv(self, tmp_path):
        """A CSV with multiple rows should return all of them."""
        csv = write_csv(
            tmp_path,
            """
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-16,South
            1003,Carol,Keyboard,1,79.99,2024-01-17,East
        """,
        )
        result = extract(csv)
        assert len(result) == 3

    def test_accepts_pathlib_path(self, tmp_path):
        """extract() signature declares Path, not str — confirm it works with Path."""
        csv = write_csv(tmp_path, valid_csv_content())
        assert isinstance(csv, Path)
        result = extract(csv)  # would raise TypeError if str is required
        assert len(result) == 1
