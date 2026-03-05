from datetime import datetime, timezone

from pyspark.sql import DataFrame

from load import (
    PIPELINE_NAME,
    WATERMARK_COLUMN,
    get_engine,
    get_watermark,
    save_watermark,
)
from logger import get_logger

log = get_logger(__name__)


def get_jdbc_url(db_host: str, db_port: int, db_name: str) -> str:
    return f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"


def load(
    df: DataFrame,
    jdbc_url: str,
    table_name: str,
    db_user: str,
    db_password: str,
) -> None:
    count = df.count()
    log.info(f"Full load: writing {count} rows to '{table_name}' via JDBC...")

    (
        df.write.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", table_name)
        .option("user", db_user)
        .option("password", db_password)
        .option("driver", "org.postgresql.Driver")
        .mode("overwrite")
        .save()
    )

    log.info(f"Full load complete: {count} rows written to '{table_name}'.")


def load_incremental(
    df: DataFrame,
    jdbc_url: str,
    table_name: str,
    db_user: str,
    db_password: str,
) -> None:
    if df.count() == 0:
        log.info("No new rows to load.")
        return

    count = df.count()
    log.info(f"Incremental load: appending {count} rows to '{table_name}' via JDBC...")

    (
        df.write.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", table_name)
        .option("user", db_user)
        .option("password", db_password)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

    log.info(f"Incremental load complete: {count} rows appended.")
