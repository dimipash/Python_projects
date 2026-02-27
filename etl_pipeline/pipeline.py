import sys

from extract import extract
from load import get_engine, load, verify_connection

from config import Settings
from logger import get_logger
from transform import transform

log = get_logger(__name__)

_SEPARATOR = "=" * 60


def run_pipeline(settings: Settings) -> None:
    log.info(_SEPARATOR)
    log.info("PIPELINE START")
    log.info(f"Source : {settings.csv_path}")
    log.info(
        f"Target : {settings.db_host}:{settings.db_port}/{settings.db_name} → {settings.table_name}"
    )
    log.info(_SEPARATOR)

    try:
        raw_df = extract(settings.csv_path)

        clean_df = transform(raw_df)

        engine = get_engine(settings.database_url)
        verify_connection(engine)
        load(clean_df, engine, settings.table_name)

    except FileNotFoundError as e:
        log.error(f"PIPELINE FAILED — Source file not found: {e}")
        raise
    except ValueError as e:
        log.error(f"PIPELINE FAILED — Configuration or validation error: {e}")
        raise
    except Exception as e:
        log.error(f"PIPELINE FAILED — Unexpected error: {type(e).__name__}: {e}")
        raise

    log.info(_SEPARATOR)
    log.info("PIPELINE COMPLETE ✓")
    log.info(_SEPARATOR)


if __name__ == "__main__":
    try:
        settings = Settings()
    except ValueError as e:
        log.error(f"Configuration error: {e}")
        sys.exit(1)

    log.info(f"Configuration loaded: {settings}")  # password is masked in repr

    try:
        run_pipeline(settings)
    except Exception:
        sys.exit(1)  # Exit with error code so shell scripts / CI can detect failure
