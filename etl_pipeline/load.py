import pandas as pd
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from logger import get_logger

log = get_logger(__name__)


def get_engine(database_url: str) -> Engine:
    log.info("Creating database engine...")
    engine = create_engine(database_url)
    return engine


def verify_connection(engine: Engine) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log.info("Database connection verified.")
    except OperationalError as e:
        raise OperationalError(
            f"Could not connect to the database. "
            f"Check your DB_HOST, DB_PORT, DB_USER, and DB_PASSWORD in .env. "
            f"Original error: {e}",
            params=None,
            orig=e,
        ) from e


def load(df: pd.DataFrame, engine: Engine, table_name: str) -> None:

    log.info(f"Writing {len(df)} rows to table '{table_name}'...")

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",  # Drops and recreates the table each run.
            index=False,  # Don't write the pandas index as a column.
            method="multi",  # Batch inserts: much faster than row-by-row.
        )
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Failed to write to table '{table_name}': {e}") from e

    _verify_row_count(engine, table_name, expected=len(df))
    log.info(f"Load complete. Table '{table_name}' is ready.")


def _verify_row_count(engine: Engine, table_name: str, expected: int) -> None:

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        actual = result.scalar()

    if actual != expected:
        raise ValueError(
            f"Row count mismatch after load: wrote {expected} rows "
            f"but database contains {actual}. This may indicate a partial write."
        )

    log.info(f"Row count verified: {actual} rows in '{table_name}'.")
