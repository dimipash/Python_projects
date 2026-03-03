# ETL Pipeline: CSV → Postgres

A Python ETL pipeline I built to practise structuring data engineering projects properly — modular, tested, scheduled, and now running incrementally so it only processes new data on each run.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` that rewrote the entire table on every run. I refactored it into separate modules, added Airflow scheduling, wrote a test suite for all the cleaning logic, and then implemented incremental loading — the pattern that makes pipelines viable at scale.

```
config.py    →  knows about configuration (including load mode)
logger.py    →  knows about log formatting
extract.py   →  knows how to read a CSV (and filter by watermark)
transform.py →  knows how to clean data
load.py      →  knows how to write to Postgres (full or incremental)
pipeline.py  →  orchestrator — run_pipeline() or run_incremental_pipeline()
dags/
  etl_dag.py →  Airflow DAG, 4 tasks, 06:00 UTC daily
tests/
  conftest.py        →  shared fixtures
  test_extract.py    →  file/column validation tests
  test_transform.py  →  35 tests across all 7 cleaning steps
  test_incremental.py →  watermark logic + filtered extract tests
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
├── config.py             # Settings dataclass — now includes LOAD_MODE
├── logger.py             # get_logger(__name__) factory
├── extract.py            # Step 1: read CSV, optional watermark filter
├── transform.py          # Step 2: clean data (7 private helpers)
├── load.py               # Step 3: full load or incremental append
├── pipeline.py           # run_pipeline() or run_incremental_pipeline()
│
├── dags/
│   └── etl_dag.py        # Airflow DAG, 4 tasks, 06:00 UTC daily
│
├── data/
│   ├── sales_raw.csv     # Day 1: 15 messy rows, 9 survive transform
│   └── sales_day2.csv    # Day 2: 7 new rows to demonstrate incremental load
│
├── tmp/                  # Parquet files between Airflow tasks (gitignored)
│   └── .gitkeep
├── logs/                 # Airflow task logs (gitignored)
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_extract.py
    ├── test_transform.py
    └── test_incremental.py  # watermark + filtered extract tests
```

---

## How incremental loading works

The problem with `if_exists='replace'` is that it rewrites every row on every run. If the table has 10 million rows and 500 new ones arrived today, you're still processing and writing 10 million rows. That's slow, expensive, and pointless.

Incremental loading fixes this with a **watermark**: after each run, we record the highest `order_date` seen in a dedicated `etl_watermarks` table. On the next run, we only extract rows newer than that date.

```
etl_watermarks table:
  pipeline_name | last_order_date          | updated_at
  sales         | 2024-01-27 00:00:00+00   | 2024-01-28 06:01:43+00
```

**Run 1 (no watermark — bootstraps automatically):**
```
get_watermark()     → None (first run)
extract(since=None) → all 15 rows from sales_raw.csv
transform()         → 9 clean rows
load()              → full replace, adds UNIQUE constraint on order_id
save_watermark()    → records 2024-01-27 (max order_date in the data)
```

**Run 2 (incremental):**
```
get_watermark()              → 2024-01-27
extract(since=2024-01-27)    → only rows from sales_day2.csv after that date
transform()                  → cleans the new rows
load_incremental()           → stages rows, merges with ON CONFLICT DO NOTHING
save_watermark()             → updates to 2024-01-30 (new max)
```

**Why `ON CONFLICT DO NOTHING`?**
The watermark filter already prevents most duplicates. But if a row somehow slips through — network glitch, pipeline restart mid-run — the `UNIQUE` constraint on `order_id` means Postgres silently skips it instead of creating a duplicate.

**Why `order_date` and not `loaded_at` as the watermark?**
`loaded_at` is set by *us* during transform — it's always "now", which makes it useless for filtering source data. `order_date` is the actual business date of the record, which is stable and correct for determining what's new.

---

## How the transform step works

Seven private helper functions chain together inside a single public `transform()`:

```python
def transform(df):
    df = _drop_duplicates(df)
    df = _drop_null_critical_fields(df)
    df = _validate_numerics(df)
    df = _validate_dates(df)
    df = _standardize_text(df)
    df = _derive_columns(df)       # → total_revenue = quantity × unit_price
    df = _add_metadata(df)         # → loaded_at (UTC)
    return df
```

Each helper logs how many rows it removed. When a run produces fewer rows than expected, I can trace exactly where data was lost.

---

## How Airflow orchestrates the pipeline

```
[extract_task] → [transform_task] → [load_task] → [cleanup_task]
```

Each task runs in its own process and passes output to the next via a Parquet file in `tmp/` — only the file path travels through XCom. In production I'd replace `tmp/` with S3. The DAG runs daily at 06:00 UTC; `catchup=False` prevents backfilling.

---

## Data flow

```
data/sales_raw.csv   (15 rows — day 1)
data/sales_day2.csv  (7 rows  — day 2, demonstrates incremental)

Run 1 — full bootstrap:
  extract (all)  →  transform (9 clean)  →  load (replace)  →  watermark = 2024-01-27

Run 2 — incremental:
  extract (filtered: order_date > 2024-01-27)
  →  transform (new clean rows)
  →  load_incremental (append + ON CONFLICT DO NOTHING)
  →  watermark = 2024-01-30
```

---

## Tests

```bash
make test   # run all tests (no database required)
make cov    # run with coverage report
```

| File | What it covers |
|------|----------------|
| `test_transform.py` | 35 tests, one class per cleaning helper |
| `test_extract.py` | file errors, column validation, raw data untouched |
| `test_incremental.py` | watermark filter logic, extract with `since=`, mocked DB calls |

The watermark tests use `unittest.mock.MagicMock` to replace the SQLAlchemy engine — no real DB needed. The `_filter_since()` function is pure Python so it needs no mocking at all.

---

## Stack

| Tool | Role |
|------|------|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation and cleaning |
| **pyarrow** | Parquet read/write between Airflow tasks |
| **SQLAlchemy** | database engine, connection pooling, upsert SQL |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` into environment variables |
| **Apache Airflow 2.9** | scheduling, orchestration, retries, web UI |
| **PostgreSQL 15** | target DB + Airflow metadata DB (separate instances) |
| **Docker Compose** | runs the full stack locally |
| **pytest + pytest-cov** | test runner and coverage reporting |

---

## Getting started

**Prerequisites:** Python 3.11+, Docker Desktop

```bash
git clone https://github.com/dimipash/Python_projects/tree/main/etl_pipeline
pip install -r requirements.txt
cp .env.sample .env

make test      # verify everything works before touching the DB

make up        # start Postgres + Airflow
make run       # run the pipeline (reads LOAD_MODE from .env)
make check     # query Postgres to see the result
```

**To demo incremental loading manually:**
```bash
# Run 1 — bootstraps the table from sales_raw.csv
CSV_PATH=data/sales_raw.csv LOAD_MODE=full python pipeline.py

# Run 2 — appends only new rows from sales_day2.csv
CSV_PATH=data/sales_day2.csv LOAD_MODE=incremental python pipeline.py

# Verify both runs landed in the table
make check
```

**Airflow UI:** http://localhost:8080 — `admin` / `admin`

---

## What I'd add next

**Great Expectations for data quality.** Instead of ad-hoc cleaning code, I'd define formal expectations (`quantity > 0`, `region` must be one of a fixed set) that generate HTML data quality reports and can halt the pipeline if the source data is too broken to trust.

**Spark for scale.** pandas loads the entire file into memory on one machine, which breaks down past a few gigabytes. I'd migrate to PySpark to distribute the work across a cluster. `pd.read_csv()` becomes `spark.read.csv()`, `dropna()` becomes `df.na.drop()`. The main shift is learning Spark's lazy evaluation model.

---

## License

MIT
