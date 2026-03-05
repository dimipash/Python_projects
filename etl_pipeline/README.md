# ETL Pipeline: CSV → Postgres

A Python ETL pipeline built to practise structuring data engineering projects properly — modular, tested, scheduled, incremental, with formal data quality checks, and now available in both pandas and PySpark.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` that rewrote the entire table on every run. I refactored it into separate modules, added Airflow scheduling, wrote a test suite, implemented incremental loading, added Great Expectations for data quality, and finally migrated the core logic to PySpark so it can run on a cluster at any scale.

```
config.py           →  configuration
logger.py           →  logging factory
extract.py          →  pandas: read CSV, watermark filter
transform.py        →  pandas: 7 cleaning steps
validate.py         →  Great Expectations: raw + clean suites
load.py             →  pandas: full load, incremental, watermarks
pipeline.py         →  pandas orchestrator

spark/
  extract_spark.py  →  PySpark: read CSV, watermark filter
  transform_spark.py →  PySpark: same 7 steps, Spark API
  load_spark.py     →  PySpark: JDBC write, full + incremental
  pipeline_spark.py →  Spark orchestrator

dags/etl_dag.py     →  Airflow DAG, 06:00 UTC daily
tests/              →  90 tests total, no DB required
```

---

## Project structure

```
etl_pipeline/
├── .env
├── .env.sample
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── config.py
├── docker-compose.yml
├── extract.py
├── load.py
├── logger.py
├── pipeline.py
├── pyproject.toml
├── requirements.txt
├── transform.py
├── validate.py
│
├── spark/
│   ├── __init__.py
│   ├── extract_spark.py
│   ├── transform_spark.py
│   ├── load_spark.py
│   └── pipeline_spark.py
│
├── dags/
│   └── etl_dag.py
│
├── data/
│   ├── sales_raw.csv
│   └── sales_day2.csv
│
├── reports/
│   └── .gitkeep
├── tmp/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_extract.py
    ├── test_transform.py
    ├── test_incremental.py
    ├── test_validate.py
    └── test_spark.py
```

---

## pandas vs PySpark — the API translation

Both pipelines do exactly the same work. The logic is identical; only the API changes.

| Step | pandas | PySpark |
|---|---|---|
| Read CSV | `pd.read_csv()` | `spark.read.option("header", True).csv()` |
| Drop duplicates | `df.drop_duplicates()` | `df.dropDuplicates()` |
| Drop null rows | `df.dropna(subset=...)` | `df.na.drop(subset=...)` |
| Cast to numeric | `pd.to_numeric(errors="coerce")` | `.cast("integer")` — nulls on bad values |
| Parse dates | `pd.to_datetime(errors="coerce")` | `to_date()` — nulls on bad values |
| String cleanup | `str.strip().str.title()` | `trim()` + `initcap()` |
| Add column | `df["col"] = expr` | `df.withColumn("col", expr)` |
| Write to DB | `df.to_sql()` | `df.write.format("jdbc").save()` |

The key conceptual difference is **lazy evaluation**: in PySpark, operations like `withColumn()` and `filter()` don't execute immediately — they build an execution plan. The plan runs when you call an action like `.count()` or `.collect()`. pandas executes eagerly, line by line.

---

## How to run

**Prerequisites:** Python 3.11+, Java 11+ (required by Spark), Docker Desktop

```bash
git clone https://github.com/dimipash/Python_projects/tree/main/etl_pipeline
pip install -r requirements.txt
cp .env.sample .env
```

**Run the pandas pipeline:**
```bash
make run
```

**Run the Spark pipeline:**
```bash
make spark-run
```

**Run all tests:**
```bash
make test         # pandas tests (no DB)
make spark-test   # Spark tests (local mode, no cluster)
make cov          # coverage report
```

**Full stack with Airflow:**
```bash
make up
```
Airflow UI: http://localhost:8080 — `admin` / `admin`

**Demo incremental loading:**
```bash
CSV_PATH=data/sales_raw.csv  LOAD_MODE=full        python pipeline.py
CSV_PATH=data/sales_day2.csv LOAD_MODE=incremental python pipeline.py
make check
```

---

## How data quality validation works

Two GE suites run on every pipeline execution — both pandas and Spark.

```
extract → validate_raw → transform → validate_clean → load
```

`GE_ACTION=halt` stops the pipeline on failure. `GE_ACTION=warn` logs and continues. Reports written to `reports/{suite_name}.json` after every run.

---

## How incremental loading works

After each successful run, the max `order_date` is recorded in `etl_watermarks`. The next run only processes rows newer than that date.

```
Run 1: extract all → transform → load (replace) → save watermark
Run 2: extract since watermark → transform → load (append, ON CONFLICT DO NOTHING) → save watermark
```

The watermark logic uses SQLAlchemy in both the pandas and Spark pipelines — it's a few small DB queries, not data processing, so there's no reason to run it through Spark.

---

## Stack

| Tool | Role |
|---|---|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation — single-machine |
| **PySpark 3.5+** | data transformation — distributed |
| **Great Expectations 1.x** | data quality validation |
| **pyarrow** | Parquet between Airflow tasks |
| **SQLAlchemy** | DB engine, watermarks, upserts |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` |
| **Apache Airflow 2.9** | scheduling and orchestration |
| **PostgreSQL 15** | target DB + Airflow metadata DB |
| **Docker Compose** | full local stack |
| **pytest + pytest-cov** | test runner and coverage |

---

## License

MIT
