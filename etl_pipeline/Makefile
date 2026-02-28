# Makefile
# --------
# Shortcuts for the commands you run every day.
# Usage: make <target>   e.g.  make up,  make run,  make lint
#
# Why a Makefile?
#   Instead of remembering "docker-compose up airflow-init && docker-compose up -d"
#   or the exact psql command to check results, you just type "make up" or
#   "make check". It also documents the intended workflow for anyone else
#   picking up the project.

.PHONY: help install up down run check lint format clean

# Default target — show available commands
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install   Install Python dependencies"
	@echo "  up        Start the full Docker stack (Postgres + Airflow)"
	@echo "  down      Stop and remove all containers"
	@echo "  run       Run the pipeline standalone (no Airflow)"
	@echo "  check     Query Postgres to verify the loaded data"
	@echo "  lint      Run ruff linter across all Python files"
	@echo "  format    Auto-format all Python files with ruff"
	@echo "  clean     Remove __pycache__, tmp files, and .coverage"
	@echo ""

# ---------------------------------------------------------------------------

install:
	pip install -r requirements.txt

# Start Postgres + full Airflow stack.
# airflow-init runs once to create the DB schema and admin user.
up:
	docker-compose up airflow-init
	docker-compose up -d
	@echo ""
	@echo "Airflow UI: http://localhost:8080  (admin / admin)"

# Stop everything and remove containers (volumes are preserved).
down:
	docker-compose down

# Run the pipeline directly — no Airflow needed, useful during development.
run:
	python pipeline.py

# Quick sanity check: show the rows currently in the database.
check:
	docker exec etl_demo_postgres psql -U postgres -d etl_demo \
		-c "SELECT order_id, customer_name, product, quantity, total_revenue, loaded_at FROM sales_clean ORDER BY order_id;"

# Lint all Python files with ruff (fast, replaces flake8 + isort + pyupgrade).
# Install with: pip install ruff
lint:
	ruff check .

# Auto-fix and format all Python files.
format:
	ruff check --fix .
	ruff format .

# Remove generated files that shouldn't be committed.
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	find . -name "coverage.xml" -delete 2>/dev/null || true
	rm -rf htmlcov/ .pytest_cache/ .mypy_cache/
	rm -f tmp/*.parquet
	@echo "Clean."
