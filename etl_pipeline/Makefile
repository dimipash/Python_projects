# Makefile
# --------
# Shortcuts for the commands you run every day.
# Usage: make <target>   e.g.  make up,  make test,  make cov

.PHONY: help install up down run check test cov lint format clean

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install   Install Python dependencies"
	@echo "  up        Start the full Docker stack (Postgres + Airflow)"
	@echo "  down      Stop and remove all containers"
	@echo "  run       Run the pipeline standalone (no Airflow)"
	@echo "  check     Query Postgres to verify the loaded data"
	@echo "  test      Run all tests"
	@echo "  cov       Run tests with coverage report"
	@echo "  lint      Run ruff linter"
	@echo "  format    Auto-format with ruff"
	@echo "  clean     Remove __pycache__, .coverage, tmp Parquet files"
	@echo ""

install:
	pip install -r requirements.txt

up:
	docker-compose up airflow-init
	docker-compose up -d
	@echo ""
	@echo "Airflow UI: http://localhost:8080  (admin / admin)"

down:
	docker-compose down

run:
	python pipeline.py

check:
	docker exec etl_demo_postgres psql -U postgres -d etl_demo \
		-c "SELECT order_id, customer_name, product, quantity, total_revenue, loaded_at FROM sales_clean ORDER BY order_id;"

# Run all tests — no database required
test:
	pytest

# Run tests + print coverage report in the terminal
# Open htmlcov/index.html in a browser for the full line-by-line report
cov:
	pytest --cov --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Full report: open htmlcov/index.html"

lint:
	ruff check .

format:
	ruff check --fix .
	ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f .coverage coverage.xml
	rm -rf htmlcov/ .pytest_cache/ .mypy_cache/
	rm -f tmp/*.parquet
	@echo "Clean."
