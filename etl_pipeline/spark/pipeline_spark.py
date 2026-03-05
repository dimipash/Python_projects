import sys

from pyspark.sql import SparkSession

from config import Settings
from load import (
    WATERMARK_COLUMN,
    get_engine,
    get_watermark,
    save_watermark,
    verify_connection,
)
from logger import get_logger
from spark.extract_spark import extract
from spark.load_spark import get_jdbc_url, load, load_incremental
from spark.transform_spark import transform

log = get_logger(__name__)

_SEP = "=" * 60


def get_spark(app_name: str = "etl-csv-to-postgres") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def run_pipeline(settings: Settings, spark: SparkSession) -> None:
    log.info(_SEP)
    log.info("SPARK PIPELINE START  [mode: full]")
    log.info(f"Source : {settings.csv_path}")
    log.info(
        f"Target : {settings.db_host}:{settings.db_port}/{settings.db_name} -> {settings.table_name}"
    )
    log.info(_SEP)

    try:
        raw_df = extract(spark, settings.csv_path)
        clean_df = transform(raw_df)

        jdbc_url = get_jdbc_url(settings.db_host, settings.db_port, settings.db_name)
        load(
            clean_df,
            jdbc_url,
            settings.table_name,
            settings.db_user,
            settings.db_password,
        )

    except FileNotFoundError as e:
        log.error(f"SPARK PIPELINE FAILED — file not found: {e}")
        raise
    except Exception as e:
        log.error(f"SPARK PIPELINE FAILED — {type(e).__name__}: {e}")
        raise

    log.info(_SEP)
    log.info("SPARK PIPELINE COMPLETE  [mode: full]")
    log.info(_SEP)


def run_incremental_pipeline(settings: Settings, spark: SparkSession) -> None:
    log.info(_SEP)
    log.info("SPARK PIPELINE START  [mode: incremental]")
    log.info(f"Source : {settings.csv_path}")
    log.info(
        f"Target : {settings.db_host}:{settings.db_port}/{settings.db_name} -> {settings.table_name}"
    )
    log.info(_SEP)

    try:
        engine = get_engine(settings.database_url)
        verify_connection(engine)
        watermark = get_watermark(engine)

        jdbc_url = get_jdbc_url(settings.db_host, settings.db_port, settings.db_name)

        if watermark is None:
            log.info("No watermark — bootstrapping with full load.")
            run_pipeline(settings, spark)
            clean_df = transform(extract(spark, settings.csv_path))
            max_date = clean_df.agg({WATERMARK_COLUMN: "max"}).collect()[0][0]
            save_watermark(engine, max_date)
            return

        raw_df = extract(spark, settings.csv_path, since=watermark)

        if raw_df.count() == 0:
            log.info("No new rows since last run.")
            log.info(_SEP)
            log.info("SPARK PIPELINE COMPLETE  [mode: incremental — no new data]")
            log.info(_SEP)
            return

        clean_df = transform(raw_df)

        if clean_df.count() == 0:
            log.info("All new rows filtered by transform — nothing to load.")
            log.info(_SEP)
            log.info("SPARK PIPELINE COMPLETE  [mode: incremental — all rows invalid]")
            log.info(_SEP)
            return

        load_incremental(
            clean_df,
            jdbc_url,
            settings.table_name,
            settings.db_user,
            settings.db_password,
        )

        max_date = clean_df.agg({WATERMARK_COLUMN: "max"}).collect()[0][0]
        save_watermark(engine, max_date)

    except FileNotFoundError as e:
        log.error(f"SPARK PIPELINE FAILED — file not found: {e}")
        raise
    except Exception as e:
        log.error(f"SPARK PIPELINE FAILED — {type(e).__name__}: {e}")
        raise

    log.info(_SEP)
    log.info("SPARK PIPELINE COMPLETE  [mode: incremental]")
    log.info(_SEP)


if __name__ == "__main__":
    try:
        settings = Settings()
    except ValueError as e:
        log.error(f"Configuration error: {e}")
        sys.exit(1)

    log.info(f"Configuration loaded: {settings}")
    spark = get_spark()

    try:
        if settings.load_mode == "incremental":
            run_incremental_pipeline(settings, spark)
        else:
            run_pipeline(settings, spark)
    except Exception:
        sys.exit(1)
    finally:
        spark.stop()
