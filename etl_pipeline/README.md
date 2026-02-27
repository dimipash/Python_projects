# ETL Pipeline: CSV → Postgres

A Python ETL pipeline I built to practise structuring data engineering projects properly — not just as a single script, but as a set of focused modules the way you'd see it in a real team codebase.

It reads raw sales data from a CSV, cleans it, and loads the result into PostgreSQL. The data intentionally ships messy: duplicates, nulls in critical fields, an `"abc"` where a number should be, and `"not-a-date"` in a date column. Six of the fifteen input rows get dropped by the time the pipeline finishes.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` file. It worked, but everything — config, logging, cleaning logic, database writes — lived in the same place. I refactored it into separate modules because I wanted to practise the Single Responsibility Principle: each file has one job, so I always know where to look when something breaks and I can change one thing without worrying about breaking another.

```
config.py    →  knows about configuration
logger.py    →  knows about log formatting
extract.py   →  knows how to read a CSV
transform.py →  knows how to clean data
load.py      →  knows how to write to Postgres
pipeline.py  →  knows the order of operations
```

---

## Project structure

```
etl-csv-to-postgres/
├── .env                  # ⚠️  secrets — never committed
├── .env.sample           # ✅  safe template — copy this to .env
├── config.py             # loads .env → typed Settings dataclass
├── logger.py             # shared logger factory, one per module
├── extract.py            # step 1: read raw CSV into a DataFrame
├── transform.py          # step 2: clean, validate, derive columns
├── load.py               # step 3: write clean data to Postgres
├── pipeline.py           # orchestrator + entry point
├── data/
│   └── sales_raw.csv     # sample input data (intentionally messy)
├── docker-compose.yml    # spins up local Postgres
├── requirements.txt
└── README.md
```

---

## How the transform step works

This is where most of the interesting decisions live. I broke the cleaning logic into seven private helper functions inside `transform.py`, so the public `transform()` function reads like a plain-English checklist:

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

Each helper logs how many rows it removed. When a pipeline run produces fewer rows than expected, I can trace exactly where data was lost without guessing.

---

## Data flow

```
data/sales_raw.csv  (15 rows, intentionally messy)
        │
        ▼  extract()       reads CSV as-is, validates column structure only
        │
        ▼  transform()
        │  _drop_duplicates            → -1 row
        │  _drop_null_critical_fields  → -2 rows
        │  _validate_numerics          → -2 rows  (bad quantity/price)
        │  _validate_dates             → -1 row   (unparseable date)
        │  _standardize_text           → normalises casing
        │  _derive_columns             → adds total_revenue
        │  _add_metadata               → adds loaded_at (UTC)
        │
        ▼  load()
        Postgres: sales_clean  (9 rows)
```

---

## Stack

| Tool | Role |
|------|------|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation and cleaning |
| **SQLAlchemy** | database engine and connection pooling |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` into environment variables |
| **PostgreSQL 15** | target database |
| **Docker Compose** | local Postgres, no manual install needed |

---

## Getting started

**Prerequisites:** Python 3.11+, Docker Desktop

```bash
# clone and install
git clone https://https://github.com/dimipash/Python_projects.git
pip install -r requirements.txt

# set up environment variables
cp .env.sample .env
# the defaults in .env.sample match docker-compose, so no edits needed locally

# start Postgres
docker-compose up -d

# run the pipeline
python pipeline.py
```

**Check the result:**
```bash
docker exec -it etl_demo_postgres psql -U postgres -d etl_demo \
  -c "SELECT * FROM sales_clean;"
```

**What the logs look like:**
```
2024-01-28 10:00:00 | INFO     | pipeline   | PIPELINE START
2024-01-28 10:00:00 | INFO     | pipeline   | Source : data/sales_raw.csv
2024-01-28 10:00:00 | INFO     | pipeline   | Target : localhost:5432/etl_demo → sales_clean
2024-01-28 10:00:00 | INFO     | extract    | Loaded 15 rows × 7 columns
2024-01-28 10:00:00 | INFO     | transform  | [drop_duplicates] 1 rows removed → 14 remaining.
2024-01-28 10:00:00 | INFO     | transform  | [drop_null_critical_fields] 2 rows removed → 12 remaining.
2024-01-28 10:00:00 | INFO     | transform  | [validate_numerics] 2 rows removed → 10 remaining.
2024-01-28 10:00:00 | INFO     | transform  | [validate_dates] 1 rows removed → 9 remaining.
2024-01-28 10:00:00 | INFO     | transform  | Transformation complete. 9/15 rows passed (6 removed).
2024-01-28 10:00:00 | INFO     | load       | Database connection verified.
2024-01-28 10:00:00 | INFO     | load       | Row count verified: 9 rows in 'sales_clean'.
2024-01-28 10:00:00 | INFO     | pipeline   | PIPELINE COMPLETE ✓
```

Every log line shows which module produced it — that's `logger.py`'s named-logger pattern paying off.

---

## What I'd add next

**Airflow scheduling.** Right now I run `python pipeline.py` manually. The next step is wrapping `extract()`, `transform()`, and `load()` in an Airflow DAG where each becomes its own Task. The functions are already shaped correctly for this — clear inputs, clear outputs, no side effects. Airflow would add scheduling, automatic retries, a web UI, and alerting.

**Spark for scale.** pandas loads the entire file into memory on one machine, which breaks down past a few gigabytes. I'd migrate to PySpark to distribute the work across a cluster. The API is similar enough that the migration isn't as daunting as it sounds — `pd.read_csv()` becomes `spark.read.csv()`, and `dropna()` becomes `df.na.drop()`. The main conceptual shift is learning Spark's lazy evaluation model.

**Great Expectations for data quality.** Instead of ad-hoc cleaning code, I'd define formal expectations (`quantity > 0`, `region` must be one of a known set of values) that generate data quality reports and can halt the pipeline if the source data is too broken to trust.

**Incremental loads.** The pipeline currently does a full replace on every run (`if_exists='replace'`). In production I'd track the last `loaded_at` timestamp and only process new rows since that point, which becomes essential once the dataset grows beyond what fits in memory.

**pytest coverage.** Each private function in `transform.py` was written to be testable in isolation — no database connection needed. I'd add `tests/test_transform.py` to lock in the cleaning behaviour and catch regressions early.

---

## License

MIT
