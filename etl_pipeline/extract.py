from datetime import datetime
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


def extract(csv_path: Path, since: datetime | None = None) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found at '{csv_path}'. Check CSV_PATH in your .env file."
        )

    df = pd.read_csv(csv_path)
    log.info(f"Loaded {len(df)} rows x {len(df.columns)} columns from {csv_path}")

    _validate_columns(df, csv_path)

    if since is not None:
        df = _filter_since(df, since)

    return df


def _filter_since(df: pd.DataFrame, since: datetime) -> pd.DataFrame:
    before = len(df)
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    since_naive = since.replace(tzinfo=None) if since.tzinfo else since
    df = df[parsed_dates > since_naive]
    log.info(
        f"Watermark filter (order_date > {since.date()}): {before - len(df)} excluded, {len(df)} remaining."
    )
    return df


def _validate_columns(df: pd.DataFrame, csv_path: Path) -> None:
    missing = EXPECTED_COLUMNS - frozenset(df.columns)
    if missing:
        raise ValueError(
            f"CSV at '{csv_path}' is missing columns: {sorted(missing)}. Found: {sorted(df.columns)}"
        )
