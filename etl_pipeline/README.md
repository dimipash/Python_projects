# ETL Pipeline: CSV → Postgres

A Python ETL pipeline built to practise structuring data engineering projects properly — modular, tested, scheduled, incremental, and now with formal data quality checks at every stage.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` that rewrote the entire table on every run. I refactored it into separate modules, added Airflow scheduling, wrote a test suite for all the cleaning logic, implemented incremental loading, and then added Great Expectations — the step that turns ad-hoc cleaning code into a formal, auditable data contract.

```
config.py    →  configuration (load mode, GE action)
logger.py    →  logging factory
extract.py   →  read CSV, optional watermark filter
transform.py →  7 cleaning steps
validate.py  →  GE validation: raw suite + clean suite
load.py      →  full load or incremental append + watermark
pipeline.py  →  orchestrator
dags/
  etl_dag.py →  Airflow DAG, 4 tasks, 06:00 UTC daily
tests/
  test_extract.py     →  13 tests
  test_transform.py   →  35 tests
  test_incremental.py →  17 tests
  test_validate.py    →  25 tests
```

---

## Project structure

```
etl-csv-to-postgres/
├── .env                  # secrets — never committed
├── .env.sample           # safe template — copy to .env
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
├── requirements.txt
├── docker-compose.yml
│
├── config.py             # Settings dataclass — LOAD_MODE + GE_ACTION
├── logger.py
├── extract.py
├── transform.py
├── validate.py           # Great Expectations: validate_raw() + validate_clean()
├── load.py
├── pipeline.py
│
├── dags/
│   └── etl_dag.py
│
├── data/
│   ├── sales_raw.csv     # day 1: 15 rows, 9 survive
│   └── sales_day2.csv    # day 2: incremental demo
│
├── reports/              # GE JSON reports (gitignored, generated at runtime)
│   └── .gitkeep
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
    ├── test_incremental.py
    └── test_validate.py
```

---

## How data quality validation works

The pipeline validates data at two points using Great Expectations, with an ephemeral GE context — no `.gx/` directory, no GE Cloud, no migration scripts.

```
extract()
    ↓
validate_raw()     ← structural checks on source data
    ↓
transform()
    ↓
validate_clean()   ← contract checks on output data
    ↓
load()
```

**Raw suite** — catches source-level problems before transform wastes time on them:

| Expectation | Reason |
|---|---|
| All 7 columns exist | schema change in the source CSV |
| Row count > 0 | empty file delivered |
| `order_id` not null | every row must be identifiable |

**Clean suite** — verifies the output matches the contract before it reaches Postgres:

| Expectation | Reason |
|---|---|
| No nulls in `customer_name`, `product`, `region`, `order_date`, `total_revenue`, `loaded_at` | critical fields must survive transform |
| `region` in `{North, South, East, West}` | unknown regions corrupt GROUP BY reports |
| `quantity` >= 1 | zero or negative quantity is a bad order |
| `unit_price` > 0 | free items should be explicit, not silent |
| `total_revenue` > 0 | derived column must be positive |
| `order_id` unique | no duplicates allowed in the output |

**Failure modes** — controlled by `GE_ACTION` in `.env`:

- `halt` (default) — raises `DataQualityError`, stops the pipeline. Use in production.
- `warn` — logs failures and continues. Use when first rolling out GE against unfamiliar data.

After every run, a JSON report is written to `reports/{suite_name}.json`:

```json
{
  "suite": "clean_suite",
  "success": false,
  "evaluated": 11,
  "passed": 10,
  "failed": 1,
  "failures": [
    {
      "expectation": "ExpectColumnValuesToBeInSet",
      "column": "region",
      "details": "..."
    }
  ]
}
```

---

## How incremental loading works

After each run, we record the highest `order_date` in a `etl_watermarks` table. The next run only extracts rows newer than that date.

```
Run 1 — full bootstrap:
  get_watermark() → None
  extract(all rows) → transform → load (replace) → save_watermark(2024-01-27)

Run 2 — incremental:
  get_watermark() → 2024-01-27
  extract(since=2024-01-27) → validate_raw → transform → validate_clean
  → load_incremental (ON CONFLICT DO NOTHING) → save_watermark(2024-01-30)
```

---

## How the transform step works

```python
def transform(df):
    df = _drop_duplicates(df)
    df = _drop_null_critical_fields(df)
    df = _validate_numerics(df)
    df = _validate_dates(df)
    df = _standardize_text(df)
    df = _derive_columns(df)       # total_revenue = quantity * unit_price
    df = _add_metadata(df)         # loaded_at (UTC)
    return df
```

---

## How Airflow orchestrates the pipeline

```
[extract_task] → [transform_task] → [load_task] → [cleanup_task]
```

Each task passes its output to the next as a Parquet file path via XCom. In production, `tmp/` would be replaced with S3. The DAG runs daily at 06:00 UTC; `catchup=False` prevents backfilling.

---

## Tests

```bash
make test   # run all tests (no database required)
make cov    # run with coverage report
```

| File | Tests | What it covers |
|---|---|---|
| `test_transform.py` | 35 | one class per cleaning helper |
| `test_extract.py` | 13 | file errors, column validation, raw data untouched |
| `test_incremental.py` | 17 | watermark filter, extract with `since=`, mocked DB |
| `test_validate.py` | 25 | raw suite, clean suite, halt vs warn, each expectation |

`test_validate.py` uses `pytest.importorskip("great_expectations")` — if GE isn't installed the tests are skipped cleanly rather than erroring.

---

## Stack

| Tool | Role |
|---|---|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation and cleaning |
| **Great Expectations 1.x** | data quality validation, JSON reports |
| **pyarrow** | Parquet read/write between Airflow tasks |
| **SQLAlchemy** | database engine, upsert SQL |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` |
| **Apache Airflow 2.9** | scheduling, orchestration, retries |
| **PostgreSQL 15** | target DB + Airflow metadata DB |
| **Docker Compose** | full local stack |
| **pytest + pytest-cov** | test runner and coverage |

---

## Getting started

**Prerequisites:** Python 3.11+, Docker Desktop

```bash
git clone https://github.com/dimipash/Python_projects/tree/main/etl_pipeline
pip install -r requirements.txt
cp .env.sample .env

make test

make up
make run
make check
```

**To demo incremental loading:**
```bash
CSV_PATH=data/sales_raw.csv LOAD_MODE=full python pipeline.py
CSV_PATH=data/sales_day2.csv LOAD_MODE=incremental python pipeline.py
make check
```

**Airflow UI:** http://localhost:8080 — `admin` / `admin`

---

## What I'd add next

**Spark for scale.** pandas loads the entire file into memory on one machine. I'd migrate to PySpark — `pd.read_csv()` becomes `spark.read.csv()`, `dropna()` becomes `df.na.drop()`. The main shift is Spark's lazy evaluation model.

---

## License

MIT
