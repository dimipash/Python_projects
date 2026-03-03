from datetime import timezone

import pandas as pd
import pytest

from transform import (
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


class TestDropDuplicates:
    def test_removes_exact_duplicates(self, duplicate_rows):
        assert len(_drop_duplicates(duplicate_rows)) == 1

    def test_keeps_unique_rows(self, clean_row):
        assert len(_drop_duplicates(clean_row)) == 1

    def test_near_duplicates_kept(self):
        df = pd.DataFrame(
            [
                {"order_id": 1, "customer_name": "Alice", "quantity": 1},
                {"order_id": 1, "customer_name": "Alice", "quantity": 2},
            ]
        )
        assert len(_drop_duplicates(df)) == 2

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["order_id", "customer_name"])
        assert len(_drop_duplicates(df)) == 0


class TestDropNullCriticalFields:
    def test_drops_null_customer_name(self):
        df = pd.DataFrame(
            [
                {"customer_name": None, "product": "Laptop", "region": "North"},
                {"customer_name": "Alice", "product": "Laptop", "region": "North"},
            ]
        )
        result = _drop_null_critical_fields(df)
        assert len(result) == 1
        assert result.iloc[0]["customer_name"] == "Alice"

    def test_drops_null_product(self):
        df = pd.DataFrame(
            [
                {"customer_name": "Alice", "product": None, "region": "North"},
                {"customer_name": "Alice", "product": "Laptop", "region": "North"},
            ]
        )
        assert len(_drop_null_critical_fields(df)) == 1

    def test_drops_null_region(self):
        df = pd.DataFrame(
            [
                {"customer_name": "Alice", "product": "Laptop", "region": None},
                {"customer_name": "Alice", "product": "Laptop", "region": "North"},
            ]
        )
        assert len(_drop_null_critical_fields(df)) == 1

    def test_keeps_null_non_critical_field(self):
        df = pd.DataFrame(
            [
                {
                    "customer_name": "Alice",
                    "product": "Laptop",
                    "region": "North",
                    "order_id": None,
                }
            ]
        )
        assert len(_drop_null_critical_fields(df)) == 1

    def test_critical_fields_constant(self):
        assert set(CRITICAL_FIELDS) == {"customer_name", "product", "region"}

    def test_null_rows_fixture(self, null_rows):
        assert len(_drop_null_critical_fields(null_rows)) == 1


class TestValidateNumerics:
    def test_drops_string_quantity(self):
        df = pd.DataFrame(
            [
                {"quantity": "abc", "unit_price": 9.99},
                {"quantity": 2, "unit_price": 9.99},
            ]
        )
        assert len(_validate_numerics(df)) == 1

    def test_drops_null_quantity(self):
        df = pd.DataFrame(
            [
                {"quantity": None, "unit_price": 9.99},
                {"quantity": 2, "unit_price": 9.99},
            ]
        )
        assert len(_validate_numerics(df)) == 1

    def test_drops_null_unit_price(self):
        df = pd.DataFrame(
            [{"quantity": 2, "unit_price": None}, {"quantity": 2, "unit_price": 9.99}]
        )
        assert len(_validate_numerics(df)) == 1

    def test_quantity_cast_to_int(self):
        df = pd.DataFrame([{"quantity": 2, "unit_price": 9.99}])
        assert _validate_numerics(df)["quantity"].dtype == int

    def test_unit_price_cast_to_float(self):
        df = pd.DataFrame([{"quantity": 2, "unit_price": 9.99}])
        assert _validate_numerics(df)["unit_price"].dtype == float

    def test_numeric_string_coerced_and_kept(self):
        df = pd.DataFrame([{"quantity": "3", "unit_price": 9.99}])
        result = _validate_numerics(df)
        assert len(result) == 1
        assert result.iloc[0]["quantity"] == 3

    def test_numeric_fields_constant(self):
        assert set(NUMERIC_FIELDS) == {"quantity", "unit_price"}

    def test_bad_numerics_fixture(self, bad_numerics):
        assert len(_validate_numerics(bad_numerics)) == 1


class TestValidateDates:
    def test_drops_unparseable_date(self):
        df = pd.DataFrame([{"order_date": "not-a-date"}, {"order_date": "2024-01-15"}])
        assert len(_validate_dates(df)) == 1

    def test_valid_date_parsed(self):
        df = pd.DataFrame([{"order_date": "2024-01-15"}])
        assert pd.api.types.is_datetime64_any_dtype(_validate_dates(df)["order_date"])

    def test_already_datetime_kept(self):
        df = pd.DataFrame([{"order_date": pd.Timestamp("2024-01-15")}])
        assert len(_validate_dates(df)) == 1

    def test_bad_dates_fixture(self, bad_dates):
        assert len(_validate_dates(bad_dates)) == 1

    def test_empty_string_dropped(self):
        df = pd.DataFrame([{"order_date": ""}, {"order_date": "2024-01-15"}])
        assert len(_validate_dates(df)) == 1


class TestStandardizeText:
    def test_lowercase_region_title_cased(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "north"}])
        assert _standardize_text(df).iloc[0]["region"] == "North"

    def test_uppercase_region_title_cased(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "SOUTH"}])
        assert _standardize_text(df).iloc[0]["region"] == "South"

    def test_whitespace_stripped_from_name(self):
        df = pd.DataFrame([{"customer_name": "  alice  ", "region": "North"}])
        assert _standardize_text(df).iloc[0]["customer_name"] == "Alice"

    def test_whitespace_stripped_from_region(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "  East  "}])
        assert _standardize_text(df).iloc[0]["region"] == "East"

    def test_correct_casing_unchanged(self):
        df = pd.DataFrame([{"customer_name": "Alice Johnson", "region": "North"}])
        result = _standardize_text(df)
        assert result.iloc[0]["customer_name"] == "Alice Johnson"
        assert result.iloc[0]["region"] == "North"


class TestDeriveColumns:
    def test_total_revenue_calculated(self):
        df = pd.DataFrame([{"quantity": 2, "unit_price": 10.00}])
        assert _derive_columns(df).iloc[0]["total_revenue"] == 20.00

    def test_total_revenue_rounded(self):
        df = pd.DataFrame([{"quantity": 3, "unit_price": 1.005}])
        assert _derive_columns(df).iloc[0]["total_revenue"] == 3.02

    def test_column_added(self, clean_row):
        assert "total_revenue" not in clean_row.columns
        assert "total_revenue" in _derive_columns(clean_row).columns

    def test_zero_quantity(self):
        df = pd.DataFrame([{"quantity": 0, "unit_price": 99.99}])
        assert _derive_columns(df).iloc[0]["total_revenue"] == 0.00


class TestAddMetadata:
    def test_loaded_at_column_added(self, clean_row):
        assert "loaded_at" not in clean_row.columns
        assert "loaded_at" in _add_metadata(clean_row).columns

    def test_loaded_at_is_timezone_aware(self, clean_row):
        ts = _add_metadata(clean_row).iloc[0]["loaded_at"]
        assert ts.tzinfo is not None

    def test_loaded_at_is_utc(self, clean_row):
        ts = _add_metadata(clean_row).iloc[0]["loaded_at"]
        assert ts.tzinfo == timezone.utc

    def test_loaded_at_is_recent(self, clean_row):
        import time

        before = pd.Timestamp.now(tz=timezone.utc).timestamp()
        result = _add_metadata(clean_row)
        after = pd.Timestamp.now(tz=timezone.utc).timestamp()
        ts = result.iloc[0]["loaded_at"].timestamp()
        assert before <= ts <= after


class TestTransformIntegration:
    def test_correct_row_count(self, full_raw_df):
        assert len(transform(full_raw_df)) == 9

    def test_has_total_revenue(self, full_raw_df):
        assert "total_revenue" in transform(full_raw_df).columns

    def test_has_loaded_at(self, full_raw_df):
        assert "loaded_at" in transform(full_raw_df).columns

    def test_no_nulls_in_critical_fields(self, full_raw_df):
        result = transform(full_raw_df)
        for field in CRITICAL_FIELDS:
            assert result[field].notna().all()

    def test_quantity_is_int(self, full_raw_df):
        assert transform(full_raw_df)["quantity"].dtype == int

    def test_order_date_is_datetime(self, full_raw_df):
        assert pd.api.types.is_datetime64_any_dtype(
            transform(full_raw_df)["order_date"]
        )

    def test_no_duplicates(self, full_raw_df):
        assert transform(full_raw_df).duplicated().sum() == 0

    def test_revenue_spot_check(self, full_raw_df):
        result = transform(full_raw_df)
        row = result[result["order_id"] == 1001]
        assert not row.empty
        assert row.iloc[0]["total_revenue"] == pytest.approx(1999.98)

    def test_regions_are_title_case(self, full_raw_df):
        for region in transform(full_raw_df)["region"]:
            assert region == region.title()

    def test_clean_row_passes_through(self, clean_row):
        assert len(transform(clean_row)) == 1
