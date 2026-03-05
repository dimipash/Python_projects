from datetime import datetime
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, to_date

from logger import get_logger

log = get_logger(__name__)

EXPECTED_COLUMNS = frozenset(
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


def extract(
    spark: SparkSession, csv_path: Path, since: datetime | None = None
) -> DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found at '{csv_path}'. Check CSV_PATH in your .env file."
        )

    df = (
        spark.read.option("header", True)
        .option("inferSchema", False)
        .csv(str(csv_path))
    )

    log.info(f"Loaded {df.count()} rows x {len(df.columns)} columns from {csv_path}")

    _validate_columns(df, csv_path)

    if since is not None:
        df = _filter_since(df, since)

    return df


def _filter_since(df: DataFrame, since: datetime) -> DataFrame:
    before = df.count()
    since_str = since.date().isoformat()
    df = df.filter(to_date(col("order_date"), "yyyy-MM-dd") > lit(since_str))
    after = df.count()
    log.info(
        f"Watermark filter (order_date > {since_str}): {before - after} excluded, {after} remaining."
    )
    return df


def _validate_columns(df: DataFrame, csv_path: Path) -> None:
    missing = EXPECTED_COLUMNS - frozenset(df.columns)
    if missing:
        raise ValueError(
            f"CSV at '{csv_path}' is missing columns: {sorted(missing)}. Found: {sorted(df.columns)}"
        )
