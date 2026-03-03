import sys

from config import Settings
from extract import extract
from load import (
    WATERMARK_COLUMN,
    get_engine,
    get_watermark,
    load,
    load_incremental,
    save_watermark,
    verify_connection,
)
from logger import get_logger
from transform import transform

log = get_logger(__name__)

_SEP = "=" * 60


def run_pipeline(settings: Settings) -> None:
    log.info(_SEP)
    log.info("PIPELINE START  [mode: full]")
    log.info(f"Source : {settings.csv_path}")
    log.info(
        f"Target : {settings.db_host}:{settings.db_port}/{settings.db_name} -> {settings.table_name}"
    )
    log.info(_SEP)

    try:
        raw_df = extract(settings.csv_path)
        clean_df = transform(raw_df)
        engine = get_engine(settings.database_url)
        verify_connection(engine)
        load(clean_df, engine, settings.table_name)
    except FileNotFoundError as e:
        log.error(f"PIPELINE FAILED — file not found: {e}")
        raise
    except ValueError as e:
        log.error(f"PIPELINE FAILED — validation error: {e}")
        raise
    except Exception as e:
        log.error(f"PIPELINE FAILED — {type(e).__name__}: {e}")
        raise

    log.info(_SEP)
    log.info("PIPELINE COMPLETE  [mode: full]")
    log.info(_SEP)


def run_incremental_pipeline(settings: Settings) -> None:
    log.info(_SEP)
    log.info("PIPELINE START  [mode: incremental]")
    log.info(f"Source : {settings.csv_path}")
    log.info(
        f"Target : {settings.db_host}:{settings.db_port}/{settings.db_name} -> {settings.table_name}"
    )
    log.info(_SEP)

    try:
        engine = get_engine(settings.database_url)
        verify_connection(engine)
        watermark = get_watermark(engine)

        if watermark is None:
            log.info("No watermark — bootstrapping with full load.")
            run_pipeline(settings)
            clean_df = transform(extract(settings.csv_path))
            save_watermark(engine, clean_df[WATERMARK_COLUMN].max())
            return

        raw_df = extract(settings.csv_path, since=watermark)

        if raw_df.empty:
            log.info("No new rows since last run.")
            log.info(_SEP)
            log.info("PIPELINE COMPLETE  [mode: incremental — no new data]")
            log.info(_SEP)
            return

        clean_df = transform(raw_df)

        if clean_df.empty:
            log.info("All new rows filtered by transform — nothing to load.")
            log.info(_SEP)
            log.info("PIPELINE COMPLETE  [mode: incremental — all rows invalid]")
            log.info(_SEP)
            return

        load_incremental(clean_df, engine, settings.table_name)
        save_watermark(engine, clean_df[WATERMARK_COLUMN].max())

    except FileNotFoundError as e:
        log.error(f"PIPELINE FAILED — file not found: {e}")
        raise
    except ValueError as e:
        log.error(f"PIPELINE FAILED — validation error: {e}")
        raise
    except Exception as e:
        log.error(f"PIPELINE FAILED — {type(e).__name__}: {e}")
        raise

    log.info(_SEP)
    log.info("PIPELINE COMPLETE  [mode: incremental]")
    log.info(_SEP)


if __name__ == "__main__":
    try:
        settings = Settings()
    except ValueError as e:
        log.error(f"Configuration error: {e}")
        sys.exit(1)

    log.info(f"Configuration loaded: {settings}")

    try:
        if settings.load_mode == "incremental":
            run_incremental_pipeline(settings)
        else:
            run_pipeline(settings)
    except Exception:
        sys.exit(1)
