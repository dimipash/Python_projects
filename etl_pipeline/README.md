# ETL Pipeline: CSV → Postgres

A Python ETL pipeline I built to practise structuring data engineering projects properly — not just as a single script, but as a set of focused modules the way you'd see it in a real team codebase.

It reads raw sales data from a CSV, cleans it, and loads the result into PostgreSQL — now scheduled and orchestrated by Apache Airflow.

---

## Why I built it this way

My first version was a single `etl_pipeline.py` file. I refactored it into separate modules so each file has one job, then added Airflow so the pipeline runs on a schedule instead of manually. Each ETL step is its own Airflow Task, which means they can fail and retry independently.

```
config.py    →  knows about configuration
logger.py    →  knows about log formatting
extract.py   →  knows how to read a CSV
transform.py →  knows how to clean data
load.py      →  knows how to write to Postgres
pipeline.py  →  original entry point (still works standalone)
dags/
  etl_dag.py →  Airflow DAG: schedules and orchestrates the three tasks
```

---

## Project structure

```
etl-csv-to-postgres/
├── .env                  # ⚠️  secrets — never committed
├── .env.sample           # ✅  safe template — copy this to .env
├── config.py
├── logger.py
├── extract.py
├── transform.py
├── load.py
├── pipeline.py           # standalone entry point: python pipeline.py
├── dags/
│   └── etl_dag.py        # Airflow DAG definition
├── data/
│   └── sales_raw.csv
├── tmp/                  # intermediate Parquet files (generated at runtime)
├── logs/                 # Airflow task logs (generated at runtime)
├── docker-compose.yml    # etl-postgres + full Airflow stack
├── requirements.txt
└── README.md
```

---

## How Airflow orchestrates the pipeline

`pipeline.py` runs all three steps in one process, in memory. The Airflow DAG breaks them into separate Tasks that each run in their own process:

```
[extract_task] → [transform_task] → [load_task] → [cleanup_task]
```

If `load_task` fails, Airflow retries just that task — it doesn't re-run extract and transform from scratch.

**The XCom / intermediate storage pattern**

Airflow Tasks share small values (strings, numbers) via XCom. A pandas DataFrame can be hundreds of MBs — too large for XCom. So each task writes its output to a Parquet file in `tmp/` and pushes only the *file path* (a string) through XCom. The next task pulls the path and reads the file.

```
extract_task   →  writes tmp/raw_2024-01-28.parquet    →  pushes path via XCom
transform_task →  reads  tmp/raw_2024-01-28.parquet    →  writes tmp/clean_2024-01-28.parquet  →  pushes path
load_task      →  reads  tmp/clean_2024-01-28.parquet  →  writes to Postgres
cleanup_task   →  deletes both tmp files
```

In production I'd replace the local `tmp/` path with an S3 or GCS URI — the pattern is identical, only the read/write calls change.

**Schedule**

The DAG runs every day at 06:00 UTC (`schedule="0 6 * * *"`). `catchup=False` means Airflow won't try to backfill runs for every day since `start_date`.

---

## Data flow

```
data/sales_raw.csv  (15 rows, intentionally messy)
        │
        ▼  extract_task      reads CSV, writes raw Parquet
        ▼  transform_task    cleans data, writes clean Parquet
        │    _drop_duplicates            → -1 row
        │    _drop_null_critical_fields  → -2 rows
        │    _validate_numerics          → -2 rows
        │    _validate_dates             → -1 row
        │    _standardize_text, _derive_columns, _add_metadata
        ▼  load_task          reads clean Parquet, writes to Postgres
        ▼  cleanup_task       deletes tmp Parquet files

        Postgres: sales_clean  (9 rows)
```

---

## Stack

| Tool | Role |
|------|------|
| **Python 3.11+** | pipeline language |
| **pandas** | data transformation and cleaning |
| **pyarrow** | Parquet read/write (intermediate storage between tasks) |
| **SQLAlchemy** | database engine and connection pooling |
| **psycopg2-binary** | PostgreSQL driver |
| **python-dotenv** | loads `.env` into environment variables |
| **Apache Airflow 2.9** | scheduling, orchestration, retries, web UI |
| **PostgreSQL 15** | target database (etl-postgres) + Airflow metadata DB (airflow-db) |
| **Docker Compose** | runs the full stack locally |

---

## Getting started

**Prerequisites:** Python 3.11+, Docker Desktop

```bash

git clone https://https://github.com/dimipash
pip install -r requirements.txt

# set up environment variables
cp .env.sample .env
# defaults match docker-compose — no edits needed for local dev

# start everything: etl-postgres + Airflow
docker-compose up airflow-init   # run once to set up Airflow schema + admin user
docker-compose up -d             # start all services in the background
```

**Open the Airflow UI:** http://localhost:8080
Login: `admin` / `admin`

The DAG `etl_csv_to_postgres` will appear. It runs automatically at 06:00 UTC daily. To trigger it manually: click the DAG → **Trigger DAG** (▶ button, top right).

**Check the result in Postgres:**
```bash
docker exec -it etl_demo_postgres psql -U postgres -d etl_demo \
  -c "SELECT * FROM sales_clean;"
```

**Run standalone (without Airflow):**
```bash
python pipeline.py
```

---

## What I'd add next

**Spark for scale.** pandas loads the entire file into memory on one machine, which breaks down past a few gigabytes. I'd migrate to PySpark to distribute the work across a cluster. `pd.read_csv()` becomes `spark.read.csv()`, `dropna()` becomes `df.na.drop()`. The main conceptual shift is learning Spark's lazy evaluation model.

**Great Expectations for data quality.** Instead of ad-hoc cleaning code, I'd define formal expectations (`quantity > 0`, `region` must be one of a known set of values) that generate data quality reports and can halt the pipeline if the source data is too broken to trust.

**Incremental loads.** The pipeline currently does a full replace on every run (`if_exists='replace'`). In production I'd track the last `loaded_at` timestamp and only process new rows since that point.

**pytest coverage.** Each private function in `transform.py` was written to be testable in isolation. I'd add `tests/test_transform.py` to lock in the cleaning behaviour and catch regressions early.

---

## License

MIT
