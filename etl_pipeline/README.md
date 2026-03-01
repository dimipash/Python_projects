# ETL Pipeline: CSV → Postgres

A Python ETL pipeline I built to practise structuring data engineering projects properly — not just as a single script, but as a set of focused modules the way you'd see it in a real team codebase.

It reads raw sales data from a CSV, cleans it, and loads the result into PostgreSQL — scheduled and orchestrated by Apache Airflow, with a full pytest test suite covering all cleaning logic.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` file. It worked, but everything — config, logging, cleaning logic, database writes — lived in the same place. I refactored it into separate modules so each file has one job, added Airflow so the pipeline runs on a schedule instead of manually, and wrote tests for every cleaning step so regressions get caught before they reach the database.

```
config.py    →  knows about configuration
logger.py    →  knows about log formatting
extract.py   →  knows how to read a CSV
transform.py →  knows how to clean data
load.py      →  knows how to write to Postgres
pipeline.py  →  orchestrator, standalone entry point
dags/
  etl_dag.py →  Airflow DAG: 4 tasks, daily schedule
tests/
  conftest.py      →  shared fixtures
  test_extract.py  →  file and column validation tests
  test_transform.py →  35 tests across all 7 cleaning steps
```

---

## Project structure

```
etl-csv-to-postgres/
├── .env                  # ⚠️  secrets — never committed
├── .env.sample           # ✅  safe template — copy this to .env
├── .gitignore
├── LICENSE
├── Makefile              # make test, make cov, make run, make up
├── README.md
├── pyproject.toml        # pytest config + coverage thresholds
├── requirements.txt
├── docker-compose.yml    # etl-postgres + full Airflow stack
│
├── config.py             # Settings dataclass, loads .env
├── logger.py             # get_logger(__name__) factory
├── extract.py            # Step 1: read CSV
├── transform.py          # Step 2: clean data
├── load.py               # Step 3: write to Postgres
├── pipeline.py           # orchestrator + entry point
│
├── dags/
│   └── etl_dag.py        # Airflow DAG, 4 tasks, 06:00 UTC daily
│
├── data/
│   └── sales_raw.csv     # 15 messy rows, 9 survive transform
│
├── tmp/                  # intermediate Parquet files (gitignored)
│   └── .gitkeep
│
├── logs/                 # Airflow task logs (gitignored)
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    ├── conftest.py        # make_row() factory + 7 shared fixtures
    ├── test_extract.py    # file errors, column validation, raw data untouched
    └── test_transform.py  # 35 tests, one class per cleaning helper
```

---

## How the transform step works

This is where most of the interesting decisions live. I broke the cleaning logic into seven private helper functions so the public `transform()` reads like a plain-English checklist:

```python
def transform(df):
    df = _drop_duplicates(df)
    df = _drop_null_critical_fields(df)
    df = _validate_numerics(df)
    df = _validate_dates(df)
    df = _standardize_text(df)
    df = _derive_columns(df)
    df = _add_metadata(df)
    return df
```

Each helper logs how many rows it removed. When a run produces fewer rows than expected, I can trace exactly where data was lost without guessing.

---

## How Airflow orchestrates the pipeline

`pipeline.py` runs all three steps in one process, in memory. The Airflow DAG breaks them into separate Tasks that each run in their own process:

```
[extract_task] → [transform_task] → [load_task] → [cleanup_task]
```

If `load_task` fails, Airflow retries just that task — without re-running extract and transform from scratch.

Each task writes its output to a date-stamped Parquet file in `tmp/` and passes only the file path (a string) through XCom — not the DataFrame itself, which can be hundreds of MBs. In production I'd replace the local `tmp/` path with S3 or GCS; the pattern is identical.

The DAG runs every day at 06:00 UTC (`schedule="0 6 * * *"`). `catchup=False` means Airflow won't backfill runs for every day since `start_date`.

---

## Data flow

```
data/sales_raw.csv  (15 rows, intentionally messy)
        │
        ▼  extract_task      reads CSV, writes raw_{date}.parquet
        │
        ▼  transform_task    reads raw Parquet, cleans data
        │    _drop_duplicates            → -1 row
        │    _drop_null_critical_fields  → -2 rows
        │    _validate_numerics          → -2 rows
        │    _validate_dates             → -1 row
        │    _standardize_text           → normalises casing
        │    _derive_columns             → adds total_revenue
        │    _add_metadata               → adds loaded_at (UTC)
        │  writes clean_{date}.parquet
        │
        ▼  load_task         reads clean Parquet, writes to Postgres
        ▼  cleanup_task      deletes both Parquet files

        Postgres: sales_clean  (9 rows)
```

---

## Tests

The test suite covers `extract.py` and `transform.py` — the two modules that contain pure Python logic with no database dependency. `load.py` is tested at runtime via the row-count verification built into `_verify_row_count()`.

```bash
make test   # run all 35 tests
make cov    # run with coverage report (fail_under=80)
```

Tests are organised into one class per function, so failures are immediately traceable:

```
PASSED tests/test_transform.py::TestDropDuplicates::test_removes_exact_duplicates
PASSED tests/test_transform.py::TestValidateNumerics::test_drops_string_quantity
PASSED tests/test_extract.py::TestExtractSuccess::test_data_is_not_cleaned
```

All fixtures live in `tests/conftest.py` and are built with a `make_row(**overrides)` factory — a valid baseline row with targeted overrides, so each test communicates exactly which field it's exercising.

---

## Stack

| Tool | Role |
|------|------|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation and cleaning |
| **pyarrow** | Parquet read/write between Airflow tasks |
| **SQLAlchemy** | database engine and connection pooling |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` into environment variables |
| **Apache Airflow 2.9** | scheduling, orchestration, retries, web UI |
| **PostgreSQL 15** | target database + Airflow metadata DB (separate instances) |
| **Docker Compose** | runs the full stack locally |
| **pytest + pytest-cov** | test runner and coverage reporting |

---

## Getting started

**Prerequisites:** Python 3.11+, Docker Desktop

```bash
git clone https://https://github.com/dimipash
pip install -r requirements.txt

# configure
cp .env.sample .env
# defaults match docker-compose — no edits needed locally

# run the tests first to verify everything works
make test

# start the full stack
make up
```

**Airflow UI:** http://localhost:8080 — login `admin` / `admin`

The DAG `etl_csv_to_postgres` runs automatically at 06:00 UTC. To trigger manually: click the DAG → **Trigger DAG** (▶ top right).

**Check the result:**
```bash
make check
```

**Run standalone without Airflow:**
```bash
make run
```

---

## What I'd add next

**Incremental loads.** The pipeline does a full replace on every run (`if_exists='replace'`). In production I'd track the last `loaded_at` timestamp and only process new rows since that point — essential once the dataset grows past what fits in memory.

**Great Expectations for data quality.** Instead of ad-hoc cleaning code, I'd define formal expectations (`quantity > 0`, `region` must be one of a fixed set) that generate HTML data quality reports and can halt the pipeline if the source data is too broken to trust.

**Spark for scale.** pandas loads the entire file into memory on one machine, which breaks down past a few gigabytes. I'd migrate to PySpark to distribute the work across a cluster. The API is close enough that migration isn't as daunting as it sounds — `pd.read_csv()` becomes `spark.read.csv()`, `dropna()` becomes `df.na.drop()`. The main shift is learning Spark's lazy evaluation model.

---

## License

MIT
