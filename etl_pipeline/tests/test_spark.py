import textwrap
from datetime import datetime, timezone
from pathlib import Path

import pytest

pyspark = pytest.importorskip("pyspark")

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from spark.extract_spark import EXPECTED_COLUMNS, _filter_since, extract
from spark.transform_spark import (
    CRITICAL_FIELDS,
    NUMERIC_FIELDS,
    _add_metadata,
    _derive_columns,
    _drop_duplicates,
    _drop_null_critical_fields,
    _standardize_text,
    _validate_dates,
    _validate_numerics,
    transform,
)


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("etl-test")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()


def make_row(**overrides) -> dict:
    defaults = {
        "order_id": "1001",
        "customer_name": "Alice Johnson",
        "product": "Laptop",
        "quantity": "2",
        "unit_price": "999.99",
        "order_date": "2024-01-15",
        "region": "North",
    }
    return {**defaults, **overrides}


class TestDropDuplicates:
    def test_removes_exact_duplicates(self, spark):
        row = make_row()
        df = spark.createDataFrame([row, row])
        assert _drop_duplicates(df).count() == 1

    def test_keeps_unique_rows(self, spark):
        df = spark.createDataFrame([make_row()])
        assert _drop_duplicates(df).count() == 1

    def test_near_duplicates_kept(self, spark):
        df = spark.createDataFrame(
            [
                make_row(quantity="1"),
                make_row(quantity="2"),
            ]
        )
        assert _drop_duplicates(df).count() == 2

    def test_empty_dataframe(self, spark):
        schema = StructType(
            [
                StructField("order_id", StringType()),
                StructField("customer_name", StringType()),
            ]
        )
        df = spark.createDataFrame([], schema)
        assert _drop_duplicates(df).count() == 0


class TestDropNullCriticalFields:
    def test_drops_null_customer_name(self, spark):
        df = spark.createDataFrame(
            [
                make_row(customer_name=None),
                make_row(customer_name="Alice"),
            ]
        )
        assert _drop_null_critical_fields(df).count() == 1

    def test_drops_null_product(self, spark):
        df = spark.createDataFrame([make_row(product=None), make_row()])
        assert _drop_null_critical_fields(df).count() == 1

    def test_drops_null_region(self, spark):
        df = spark.createDataFrame([make_row(region=None), make_row()])
        assert _drop_null_critical_fields(df).count() == 1

    def test_keeps_null_non_critical_field(self, spark):
        df = spark.createDataFrame([make_row(order_id=None)])
        assert _drop_null_critical_fields(df).count() == 1

    def test_critical_fields_constant(self):
        assert set(CRITICAL_FIELDS) == {"customer_name", "product", "region"}


class TestValidateNumerics:
    def test_drops_string_quantity(self, spark):
        df = spark.createDataFrame([make_row(quantity="abc"), make_row(quantity="2")])
        assert _validate_numerics(df).count() == 1

    def test_drops_null_quantity(self, spark):
        df = spark.createDataFrame([make_row(quantity=None), make_row(quantity="2")])
        assert _validate_numerics(df).count() == 1

    def test_quantity_cast_to_int(self, spark):
        df = spark.createDataFrame([make_row(quantity="2")])
        result = _validate_numerics(df)
        assert result.schema["quantity"].dataType == IntegerType()

    def test_unit_price_cast_to_double(self, spark):
        df = spark.createDataFrame([make_row(unit_price="9.99")])
        result = _validate_numerics(df)
        assert result.schema["unit_price"].dataType == DoubleType()

    def test_numeric_fields_constant(self):
        assert set(NUMERIC_FIELDS) == {"quantity", "unit_price"}


class TestValidateDates:
    def test_drops_unparseable_date(self, spark):
        df = spark.createDataFrame([make_row(order_date="not-a-date"), make_row()])
        assert _validate_dates(df).count() == 1

    def test_valid_date_parsed(self, spark):
        df = spark.createDataFrame([make_row(order_date="2024-01-15")])
        result = _validate_dates(df)
        assert result.count() == 1
        from pyspark.sql.types import DateType

        assert result.schema["order_date"].dataType == DateType()

    def test_empty_string_dropped(self, spark):
        df = spark.createDataFrame([make_row(order_date=""), make_row()])
        assert _validate_dates(df).count() == 1


class TestStandardizeText:
    def test_lowercase_region_title_cased(self, spark):
        df = spark.createDataFrame([make_row(region="north")])
        result = _standardize_text(df).collect()
        assert result[0]["region"] == "North"

    def test_uppercase_region_title_cased(self, spark):
        df = spark.createDataFrame([make_row(region="SOUTH")])
        result = _standardize_text(df).collect()
        assert result[0]["region"] == "South"

    def test_whitespace_stripped_from_name(self, spark):
        df = spark.createDataFrame([make_row(customer_name="  alice  ")])
        result = _standardize_text(df).collect()
        assert result[0]["customer_name"] == "Alice"

    def test_correct_casing_unchanged(self, spark):
        df = spark.createDataFrame(
            [make_row(customer_name="Alice Johnson", region="North")]
        )
        result = _standardize_text(df).collect()
        assert result[0]["customer_name"] == "Alice Johnson"
        assert result[0]["region"] == "North"


class TestDeriveColumns:
    def test_total_revenue_calculated(self, spark):
        df = spark.createDataFrame([make_row()])
        df = _validate_numerics(df)
        result = _derive_columns(df).collect()
        assert result[0]["total_revenue"] == pytest.approx(1999.98)

    def test_total_revenue_column_added(self, spark):
        df = spark.createDataFrame([make_row()])
        df = _validate_numerics(df)
        assert "total_revenue" not in df.columns
        assert "total_revenue" in _derive_columns(df).columns

    def test_zero_quantity_produces_zero_revenue(self, spark):
        df = spark.createDataFrame([make_row(quantity="0", unit_price="99.99")])
        df = _validate_numerics(df)
        result = _derive_columns(df).collect()
        assert result[0]["total_revenue"] == 0.0


class TestAddMetadata:
    def test_loaded_at_column_added(self, spark):
        df = spark.createDataFrame([make_row()])
        assert "loaded_at" not in df.columns
        assert "loaded_at" in _add_metadata(df).columns

    def test_loaded_at_is_not_null(self, spark):
        df = spark.createDataFrame([make_row()])
        result = _add_metadata(df).collect()
        assert result[0]["loaded_at"] is not None


class TestTransformIntegration:
    def _full_raw(self, spark):
        return spark.createDataFrame(
            [
                make_row(
                    order_id="1001",
                    customer_name="Alice Johnson",
                    product="Laptop",
                    quantity="2",
                    unit_price="999.99",
                    order_date="2024-01-15",
                    region="North",
                ),
                make_row(
                    order_id="1002",
                    customer_name="Bob Smith",
                    product="Mouse",
                    quantity="5",
                    unit_price="29.99",
                    order_date="2024-01-16",
                    region="South",
                ),
                make_row(
                    order_id="1003",
                    customer_name=None,
                    product="Keyboard",
                    quantity="1",
                    unit_price="79.99",
                    order_date="2024-01-17",
                    region="East",
                ),
                make_row(
                    order_id="1004",
                    customer_name="Carol White",
                    product="Monitor",
                    quantity="abc",
                    unit_price="349.99",
                    order_date="2024-01-18",
                    region="West",
                ),
                make_row(
                    order_id="1005",
                    customer_name="Dave Brown",
                    product="Laptop",
                    quantity="1",
                    unit_price="999.99",
                    order_date="not-a-date",
                    region="North",
                ),
                make_row(
                    order_id="1006",
                    customer_name="Eve Davis",
                    product="Headset",
                    quantity="3",
                    unit_price="149.99",
                    order_date="2024-01-20",
                    region="South",
                ),
                make_row(
                    order_id="1007",
                    customer_name="Frank Miller",
                    product="Mouse",
                    quantity="2",
                    unit_price="29.99",
                    order_date="2024-01-21",
                    region=None,
                ),
                make_row(
                    order_id="1008",
                    customer_name="Grace Lee",
                    product="Webcam",
                    quantity="1",
                    unit_price="89.99",
                    order_date="2024-01-22",
                    region="East",
                ),
                make_row(
                    order_id="1009",
                    customer_name="Alice Johnson",
                    product="Mouse",
                    quantity="5",
                    unit_price="29.99",
                    order_date="2024-01-16",
                    region="South",
                ),
                make_row(
                    order_id="1002",
                    customer_name="Bob Smith",
                    product="Mouse",
                    quantity="5",
                    unit_price="29.99",
                    order_date="2024-01-16",
                    region="South",
                ),
                make_row(
                    order_id="1010",
                    customer_name="Hank Wilson",
                    product="Keyboard",
                    quantity=None,
                    unit_price="79.99",
                    order_date="2024-01-23",
                    region="West",
                ),
                make_row(
                    order_id="1011",
                    customer_name="Ivy Moore",
                    product="Laptop",
                    quantity="1",
                    unit_price="999.99",
                    order_date="2024-01-24",
                    region="North",
                ),
                make_row(
                    order_id="1012",
                    customer_name=None,
                    product="Headset",
                    quantity=None,
                    unit_price="149.99",
                    order_date="2024-01-25",
                    region="South",
                ),
                make_row(
                    order_id="1013",
                    customer_name="Jack Taylor",
                    product="Monitor",
                    quantity="2",
                    unit_price="349.99",
                    order_date="2024-01-26",
                    region="East",
                ),
                make_row(
                    order_id="1014",
                    customer_name="Karen Anderson",
                    product="Webcam",
                    quantity="3",
                    unit_price="89.99",
                    order_date="2024-01-27",
                    region="West",
                ),
            ]
        )

    def test_correct_row_count(self, spark):
        assert transform(self._full_raw(spark)).count() == 9

    def test_has_total_revenue(self, spark):
        assert "total_revenue" in transform(self._full_raw(spark)).columns

    def test_has_loaded_at(self, spark):
        assert "loaded_at" in transform(self._full_raw(spark)).columns

    def test_no_nulls_in_critical_fields(self, spark):
        result = transform(self._full_raw(spark))
        for field in CRITICAL_FIELDS:
            assert result.filter(result[field].isNull()).count() == 0

    def test_quantity_is_integer(self, spark):
        result = transform(self._full_raw(spark))
        assert result.schema["quantity"].dataType == IntegerType()

    def test_no_duplicates(self, spark):
        result = transform(self._full_raw(spark))
        assert result.count() == result.dropDuplicates().count()

    def test_regions_are_title_case(self, spark):
        result = transform(self._full_raw(spark))
        rows = result.select("region").distinct().collect()
        for row in rows:
            assert row["region"] == row["region"].title()


class TestFilterSince:
    def test_filters_rows_before_watermark(self, spark):
        df = spark.createDataFrame(
            [
                make_row(order_date="2024-01-18"),
                make_row(order_date="2024-01-21"),
            ]
        )
        wm = datetime(2024, 1, 20, tzinfo=timezone.utc)
        result = _filter_since(df, wm)
        assert result.count() == 1

    def test_watermark_date_excluded(self, spark):
        df = spark.createDataFrame([make_row(order_date="2024-01-20")])
        wm = datetime(2024, 1, 20, tzinfo=timezone.utc)
        assert _filter_since(df, wm).count() == 0

    def test_all_rows_after_watermark_kept(self, spark):
        df = spark.createDataFrame(
            [
                make_row(order_date="2024-01-10"),
                make_row(order_date="2024-01-15"),
                make_row(order_date="2024-01-20"),
            ]
        )
        wm = datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert _filter_since(df, wm).count() == 3

    def test_unparseable_dates_excluded(self, spark):
        df = spark.createDataFrame(
            [
                make_row(order_date="not-a-date"),
                make_row(order_date="2024-01-15"),
            ]
        )
        wm = datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert _filter_since(df, wm).count() == 1


class TestExtractSpark:
    def test_raises_file_not_found(self, spark, tmp_path):
        from spark.extract_spark import extract

        with pytest.raises(FileNotFoundError):
            extract(spark, tmp_path / "ghost.csv")

    def test_raises_for_missing_column(self, spark, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text("order_id,customer_name\n1001,Alice")
        with pytest.raises(ValueError, match="product"):
            extract(spark, csv)

    def test_returns_all_rows_without_watermark(self, spark, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(
            textwrap.dedent("""
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-16,South
        """).strip()
        )
        assert extract(spark, csv).count() == 2

    def test_filters_with_watermark(self, spark, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(
            textwrap.dedent("""
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-28,South
        """).strip()
        )
        wm = datetime(2024, 1, 20, tzinfo=timezone.utc)
        result = extract(spark, csv, since=wm)
        assert result.count() == 1
        assert result.collect()[0]["order_id"] == "1002"
