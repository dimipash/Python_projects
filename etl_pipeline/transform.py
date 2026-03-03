from datetime import datetime, timezone

import pandas as pd

from logger import get_logger

log = get_logger(__name__)

CRITICAL_FIELDS: list[str] = ["customer_name", "product", "region"]
NUMERIC_FIELDS: list[str] = ["quantity", "unit_price"]


def transform(df: pd.DataFrame) -> pd.DataFrame:
    original_count = len(df)

    df = _drop_duplicates(df)
    df = _drop_null_critical_fields(df)
    df = _validate_numerics(df)
    df = _validate_dates(df)
    df = _standardize_text(df)
    df = _derive_columns(df)
    df = _add_metadata(df)

    log.info(f"Transform complete: {len(df)}/{original_count} rows passed.")
    return df


def _drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    _log_removed("drop_duplicates", before, len(df))
    return df


def _drop_null_critical_fields(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.dropna(subset=CRITICAL_FIELDS)
    _log_removed("drop_null_critical_fields", before, len(df))
    return df


def _validate_numerics(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    for field in NUMERIC_FIELDS:
        df[field] = pd.to_numeric(df[field], errors="coerce")
    df = df.dropna(subset=NUMERIC_FIELDS)
    _log_removed("validate_numerics", before, len(df))

    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    return df


def _validate_dates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    _log_removed("validate_dates", before, len(df))
    return df


def _standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    for field in ["customer_name", "region"]:
        df[field] = df[field].str.strip().str.title()
    return df


def _derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["total_revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    return df


def _add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df["loaded_at"] = datetime.now(tz=timezone.utc)
    return df


def _log_removed(step: str, before: int, after: int) -> None:
    log.info(f"[{step}] {before - after} rows removed -> {after} remaining.")
