import json
from pathlib import Path

import great_expectations as gx
import great_expectations.expectations as gxe
import pandas as pd

from logger import get_logger

log = get_logger(__name__)

VALID_REGIONS = {"North", "South", "East", "West"}
REPORTS_DIR = Path(__file__).parent / "reports"


class DataQualityError(Exception):
    pass


def validate_raw(df: pd.DataFrame, action: str = "halt") -> bool:
    expectations = [
        gxe.ExpectColumnToExist(column="order_id"),
        gxe.ExpectColumnToExist(column="customer_name"),
        gxe.ExpectColumnToExist(column="product"),
        gxe.ExpectColumnToExist(column="quantity"),
        gxe.ExpectColumnToExist(column="unit_price"),
        gxe.ExpectColumnToExist(column="order_date"),
        gxe.ExpectColumnToExist(column="region"),
        gxe.ExpectTableRowCountToBeGreaterThan(value=0),
        gxe.ExpectColumnValuesToNotBeNull(column="order_id"),
    ]
    return _run(df, suite_name="raw_suite", expectations=expectations, action=action)


def validate_clean(df: pd.DataFrame, action: str = "halt") -> bool:
    expectations = [
        gxe.ExpectColumnValuesToNotBeNull(column="customer_name"),
        gxe.ExpectColumnValuesToNotBeNull(column="product"),
        gxe.ExpectColumnValuesToNotBeNull(column="region"),
        gxe.ExpectColumnValuesToNotBeNull(column="order_date"),
        gxe.ExpectColumnValuesToNotBeNull(column="total_revenue"),
        gxe.ExpectColumnValuesToNotBeNull(column="loaded_at"),
        gxe.ExpectColumnValuesToBeInSet(column="region", value_set=VALID_REGIONS),
        gxe.ExpectColumnValuesToBeBetween(column="quantity", min_value=1),
        gxe.ExpectColumnValuesToBeBetween(
            column="unit_price", min_value=0, strict_min=True
        ),
        gxe.ExpectColumnValuesToBeBetween(
            column="total_revenue", min_value=0, strict_min=True
        ),
        gxe.ExpectColumnValuesToBeUnique(column="order_id"),
    ]
    return _run(df, suite_name="clean_suite", expectations=expectations, action=action)


def _run(
    df: pd.DataFrame,
    suite_name: str,
    expectations: list,
    action: str,
) -> bool:
    context = gx.get_context(mode="ephemeral")

    datasource = context.data_sources.add_pandas("pandas_source")
    asset = datasource.add_dataframe_asset("dataframe_asset")
    batch_definition = asset.add_batch_definition_whole_dataframe("batch_definition")

    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
    for expectation in expectations:
        suite.add_expectation(expectation)

    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(name=suite_name, data=batch_definition, suite=suite)
    )

    result = validation_definition.run(batch_parameters={"dataframe": df})

    failures = [r for r in result.results if not r.success]
    _write_report(suite_name, result)

    if result.success:
        log.info(f"[{suite_name}] All {len(result.results)} expectations passed.")
        return True

    failure_summary = ", ".join(
        f"{r.expectation_config.type}({_expectation_column(r)})" for r in failures
    )
    log.warning(
        f"[{suite_name}] {len(failures)}/{len(result.results)} expectations failed: {failure_summary}"
    )

    if action == "halt":
        raise DataQualityError(
            f"Data quality check failed for '{suite_name}': {failure_summary}"
        )

    return False


def _expectation_column(result) -> str:
    kwargs = result.expectation_config.kwargs
    return kwargs.get("column", "table")


def _write_report(suite_name: str, result) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / f"{suite_name}.json"

    summary = {
        "suite": suite_name,
        "success": result.success,
        "evaluated": len(result.results),
        "passed": sum(1 for r in result.results if r.success),
        "failed": sum(1 for r in result.results if not r.success),
        "failures": [
            {
                "expectation": r.expectation_config.type,
                "column": _expectation_column(r),
                "details": str(r.result),
            }
            for r in result.results
            if not r.success
        ],
    }

    report_path.write_text(json.dumps(summary, indent=2, default=str))
    log.info(f"[{suite_name}] Report written to {report_path}")
