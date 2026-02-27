from pathlib import Path

import pandas as pd

from logger import get_logger

log = get_logger(__name__)


EXPECTED_COLUMNS: frozenset[str] = frozenset(
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


def extract(csv_path: Path) -> pd.DataFrame:

    log.info(f"Reading CSV from: {csv_path}")

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found at '{csv_path}'. "
            f"Check the CSV_PATH value in your .env file."
        )

    df = pd.read_csv(csv_path)
    log.info(f"Loaded {len(df)} rows × {len(df.columns)} columns")

    _validate_columns(df, csv_path)

    return df


def _validate_columns(df: pd.DataFrame, csv_path: Path) -> None:

    actual_columns = frozenset(df.columns)
    missing = EXPECTED_COLUMNS - actual_columns

    if missing:
        raise ValueError(
            f"CSV at '{csv_path}' is missing required columns: {sorted(missing)}. "
            f"Found columns: {sorted(actual_columns)}"
        )

    log.info(f"Column validation passed. Columns: {list(df.columns)}")
