import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    db_host: str = field(default_factory=lambda: _require_env("DB_HOST"))
    db_port: int = field(
        default_factory=lambda: int(_require_env("DB_PORT", default="5432"))
    )
    db_name: str = field(default_factory=lambda: _require_env("DB_NAME"))
    db_user: str = field(default_factory=lambda: _require_env("DB_USER"))
    db_password: str = field(default_factory=lambda: _require_env("DB_PASSWORD"))

    csv_path: Path = field(
        default_factory=lambda: Path(
            _require_env("CSV_PATH", default="data/sales_raw.csv")
        )
    )
    table_name: str = field(
        default_factory=lambda: _require_env("TABLE_NAME", default="sales_clean")
    )

    @property
    def database_url(self) -> str:

        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def __repr__(self) -> str:

        return (
            f"Settings(db_host={self.db_host!r}, db_port={self.db_port}, "
            f"db_name={self.db_name!r}, db_user={self.db_user!r}, "
            f"db_password='***', csv_path={self.csv_path!r}, "
            f"table_name={self.table_name!r})"
        )


def _require_env(key: str, default: str | None = None) -> str:

    value = os.environ.get(key, default)
    if value is None:
        raise ValueError(
            f"Required environment variable '{key}' is not set. "
            f"Did you copy .env.sample to .env and fill it in?"
        )
    return value
