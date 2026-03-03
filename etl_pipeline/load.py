from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from logger import get_logger

log = get_logger(__name__)

PIPELINE_NAME = "sales"
WATERMARK_COLUMN = "order_date"


def get_engine(database_url: str) -> Engine:
    log.info("Creating database engine...")
    return create_engine(database_url)


def verify_connection(engine: Engine) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log.info("Database connection verified.")
    except OperationalError as e:
        raise OperationalError(
            f"Could not connect to the database. Check DB credentials in .env. Error: {e}",
            params=None,
            orig=e,
        ) from e


def load(df: pd.DataFrame, engine: Engine, table_name: str) -> None:
    log.info(f"Full load: writing {len(df)} rows to '{table_name}'...")
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            method="multi",
        )
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Full load failed for '{table_name}': {e}") from e

    _ensure_unique_constraint(engine, table_name, column="order_id")
    _verify_row_count(engine, table_name, expected=len(df))
    log.info(f"Full load complete.")


def get_watermark(
    engine: Engine, pipeline_name: str = PIPELINE_NAME
) -> datetime | None:
    _ensure_watermarks_table(engine)

    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT last_order_date FROM etl_watermarks WHERE pipeline_name = :name"
            ),
            {"name": pipeline_name},
        ).fetchone()

    if row is None:
        log.info(f"No watermark found for '{pipeline_name}' — first run.")
        return None

    watermark = row[0]
    if watermark.tzinfo is None:
        watermark = watermark.replace(tzinfo=timezone.utc)

    log.info(f"Watermark: {watermark.date()}")
    return watermark


def save_watermark(
    engine: Engine, watermark: datetime, pipeline_name: str = PIPELINE_NAME
) -> None:
    _ensure_watermarks_table(engine)

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO etl_watermarks (pipeline_name, last_order_date, updated_at)
                VALUES (:name, :watermark, NOW())
                ON CONFLICT (pipeline_name)
                DO UPDATE SET last_order_date = EXCLUDED.last_order_date, updated_at = EXCLUDED.updated_at
            """),
            {"name": pipeline_name, "watermark": watermark},
        )
    log.info(f"Watermark saved: '{pipeline_name}' -> {watermark.date()}")


def load_incremental(df: pd.DataFrame, engine: Engine, table_name: str) -> int:
    if df.empty:
        log.info("No new rows to load.")
        return 0

    staging = f"{table_name}_staging"
    log.info(f"Incremental load: staging {len(df)} rows...")

    try:
        df.to_sql(
            name=staging, con=engine, if_exists="replace", index=False, method="multi"
        )

        columns = ", ".join(f'"{c}"' for c in df.columns)
        with engine.begin() as conn:
            result = conn.execute(
                text(f"""
                INSERT INTO {table_name} ({columns})
                SELECT {columns} FROM {staging}
                ON CONFLICT (order_id) DO NOTHING
            """)
            )
            inserted = result.rowcount

        with engine.begin() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {staging}"))

    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Incremental load failed for '{table_name}': {e}") from e

    log.info(
        f"Incremental load complete: {inserted} inserted, {len(df) - inserted} skipped."
    )
    return inserted


def _ensure_watermarks_table(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS etl_watermarks (
                pipeline_name   VARCHAR(255) PRIMARY KEY,
                last_order_date TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            )
        """)
        )


def _ensure_unique_constraint(engine: Engine, table_name: str, column: str) -> None:
    constraint_name = f"uq_{table_name}_{column}"
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_constraint WHERE conname = :name"),
            {"name": constraint_name},
        ).fetchone()

        if not exists:
            conn.execute(
                text(
                    f'ALTER TABLE "{table_name}" ADD CONSTRAINT {constraint_name} UNIQUE ("{column}")'
                )
            )
            log.info(f"Unique constraint added on '{table_name}'.'{column}'.")


def _verify_row_count(engine: Engine, table_name: str, expected: int) -> None:
    with engine.connect() as conn:
        actual = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

    if actual != expected:
        raise ValueError(
            f"Row count mismatch: wrote {expected} but '{table_name}' has {actual}."
        )
    log.info(f"Row count verified: {actual} rows in '{table_name}'.")
