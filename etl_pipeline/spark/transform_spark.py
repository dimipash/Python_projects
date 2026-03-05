from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    current_timestamp,
    initcap,
    to_date,
    trim,
)
from pyspark.sql.functions import (
    round as spark_round,
)

from logger import get_logger

log = get_logger(__name__)

CRITICAL_FIELDS = ["customer_name", "product", "region"]
NUMERIC_FIELDS = ["quantity", "unit_price"]


def transform(df: DataFrame) -> DataFrame:
    original_count = df.count()

    df = _drop_duplicates(df)
    df = _drop_null_critical_fields(df)
    df = _validate_numerics(df)
    df = _validate_dates(df)
    df = _standardize_text(df)
    df = _derive_columns(df)
    df = _add_metadata(df)

    log.info(f"Transform complete: {df.count()}/{original_count} rows passed.")
    return df


def _drop_duplicates(df: DataFrame) -> DataFrame:
    before = df.count()
    df = df.dropDuplicates()
    _log_removed("drop_duplicates", before, df.count())
    return df


def _drop_null_critical_fields(df: DataFrame) -> DataFrame:
    before = df.count()
    df = df.na.drop(subset=CRITICAL_FIELDS)
    _log_removed("drop_null_critical_fields", before, df.count())
    return df


def _validate_numerics(df: DataFrame) -> DataFrame:
    before = df.count()
    df = df.withColumn("quantity", col("quantity").cast("integer"))
    df = df.withColumn("unit_price", col("unit_price").cast("double"))
    df = df.na.drop(subset=NUMERIC_FIELDS)
    _log_removed("validate_numerics", before, df.count())
    return df


def _validate_dates(df: DataFrame) -> DataFrame:
    before = df.count()
    df = df.withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
    df = df.na.drop(subset=["order_date"])
    _log_removed("validate_dates", before, df.count())
    return df


def _standardize_text(df: DataFrame) -> DataFrame:
    df = df.withColumn("customer_name", initcap(trim(col("customer_name"))))
    df = df.withColumn("region", initcap(trim(col("region"))))
    return df


def _derive_columns(df: DataFrame) -> DataFrame:
    df = df.withColumn(
        "total_revenue", spark_round(col("quantity") * col("unit_price"), 2)
    )
    return df


def _add_metadata(df: DataFrame) -> DataFrame:
    df = df.withColumn("loaded_at", current_timestamp())
    return df


def _log_removed(step: str, before: int, after: int) -> None:
    log.info(f"[{step}] {before - after} rows removed -> {after} remaining.")
