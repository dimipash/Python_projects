from datetime import timezone

import pandas as pd
import pytest

# We import private helpers directly — this is intentional and acceptable
# in tests. The underscore means "not part of the public API", not "hidden".
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

# ===========================================================================
# _drop_duplicates
# ===========================================================================


class TestDropDuplicates:
    def test_removes_exact_duplicates(self, duplicate_rows):
        """Two identical rows should become one."""
        result = _drop_duplicates(duplicate_rows)
        assert len(result) == 1

    def test_keeps_all_unique_rows(self, clean_row):
        """A DataFrame with no duplicates should be returned unchanged."""
        result = _drop_duplicates(clean_row)
        assert len(result) == 1

    def test_near_duplicates_are_kept(self):
        """Rows that differ in even one field are NOT duplicates."""
        df = pd.DataFrame(
            [
                {"order_id": 1, "customer_name": "Alice", "quantity": 1},
                {
                    "order_id": 1,
                    "customer_name": "Alice",
                    "quantity": 2,
                },  # quantity differs
            ]
        )
        result = _drop_duplicates(df)
        assert len(result) == 2

    def test_empty_dataframe_is_safe(self):
        """An empty DataFrame should not raise — just return empty."""
        df = pd.DataFrame(columns=["order_id", "customer_name"])
        result = _drop_duplicates(df)
        assert len(result) == 0


# ===========================================================================
# _drop_null_critical_fields
# ===========================================================================


class TestDropNullCriticalFields:
    def test_drops_null_customer_name(self):
        """Rows with a null customer_name should be removed."""
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
        result = _drop_null_critical_fields(df)
        assert len(result) == 1

    def test_drops_null_region(self):
        df = pd.DataFrame(
            [
                {"customer_name": "Alice", "product": "Laptop", "region": None},
                {"customer_name": "Alice", "product": "Laptop", "region": "North"},
            ]
        )
        result = _drop_null_critical_fields(df)
        assert len(result) == 1

    def test_keeps_row_with_null_non_critical_field(self):
        """
        A null in a non-critical field (e.g. order_id) must NOT cause the
        row to be dropped. This is the key behaviour of dropna(subset=...).
        """
        df = pd.DataFrame(
            [
                {
                    "customer_name": "Alice",
                    "product": "Laptop",
                    "region": "North",
                    "order_id": None,  # non-critical — row should survive
                }
            ]
        )
        result = _drop_null_critical_fields(df)
        assert len(result) == 1

    def test_all_critical_fields_covered(self):
        """Verify CRITICAL_FIELDS constant matches what this test exercises."""
        assert set(CRITICAL_FIELDS) == {"customer_name", "product", "region"}

    def test_null_rows_fixture(self, null_rows):
        """
        Integration check using the conftest fixture:
        3 critical-field nulls → dropped, 1 non-critical null → kept.
        """
        result = _drop_null_critical_fields(null_rows)
        assert len(result) == 1


# ===========================================================================
# _validate_numerics
# ===========================================================================


class TestValidateNumerics:
    def test_drops_string_quantity(self):
        """A non-numeric string like "abc" should cause the row to be dropped."""
        df = pd.DataFrame(
            [
                {"quantity": "abc", "unit_price": 9.99},
                {"quantity": 2, "unit_price": 9.99},
            ]
        )
        result = _validate_numerics(df)
        assert len(result) == 1

    def test_drops_null_quantity(self):
        """A null quantity should cause the row to be dropped."""
        df = pd.DataFrame(
            [
                {"quantity": None, "unit_price": 9.99},
                {"quantity": 2, "unit_price": 9.99},
            ]
        )
        result = _validate_numerics(df)
        assert len(result) == 1

    def test_drops_null_unit_price(self):
        df = pd.DataFrame(
            [
                {"quantity": 2, "unit_price": None},
                {"quantity": 2, "unit_price": 9.99},
            ]
        )
        result = _validate_numerics(df)
        assert len(result) == 1

    def test_quantity_cast_to_int(self):
        """After validation, quantity must be int (not float)."""
        df = pd.DataFrame([{"quantity": 2, "unit_price": 9.99}])
        result = _validate_numerics(df)
        assert result["quantity"].dtype == int

    def test_unit_price_cast_to_float(self):
        """After validation, unit_price must be float."""
        df = pd.DataFrame([{"quantity": 2, "unit_price": 9.99}])
        result = _validate_numerics(df)
        assert result["unit_price"].dtype == float

    def test_numeric_string_is_coerced_and_kept(self):
        """A quantity like "3" (a numeric string) should be coerced and kept."""
        df = pd.DataFrame([{"quantity": "3", "unit_price": 9.99}])
        result = _validate_numerics(df)
        assert len(result) == 1
        assert result.iloc[0]["quantity"] == 3

    def test_all_numeric_fields_covered(self):
        """Verify NUMERIC_FIELDS constant matches what this test exercises."""
        assert set(NUMERIC_FIELDS) == {"quantity", "unit_price"}

    def test_bad_numerics_fixture(self, bad_numerics):
        """2 bad rows (string + null quantity) → dropped, 1 valid row → kept."""
        result = _validate_numerics(bad_numerics)
        assert len(result) == 1


# ===========================================================================
# _validate_dates
# ===========================================================================


class TestValidateDates:
    def test_drops_unparseable_date(self):
        """Strings that cannot be parsed as dates should cause row removal."""
        df = pd.DataFrame(
            [
                {"order_date": "not-a-date"},
                {"order_date": "2024-01-15"},
            ]
        )
        result = _validate_dates(df)
        assert len(result) == 1

    def test_valid_date_string_is_parsed(self):
        """Valid date strings should be converted to datetime objects."""
        df = pd.DataFrame([{"order_date": "2024-01-15"}])
        result = _validate_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

    def test_already_datetime_is_kept(self):
        """If order_date is already a datetime, the row should still pass."""
        df = pd.DataFrame([{"order_date": pd.Timestamp("2024-01-15")}])
        result = _validate_dates(df)
        assert len(result) == 1

    def test_bad_dates_fixture(self, bad_dates):
        """1 bad date → dropped, 1 valid date → kept."""
        result = _validate_dates(bad_dates)
        assert len(result) == 1

    def test_empty_string_date_is_dropped(self):
        """An empty string should not parse as a valid date."""
        df = pd.DataFrame(
            [
                {"order_date": ""},
                {"order_date": "2024-01-15"},
            ]
        )
        result = _validate_dates(df)
        assert len(result) == 1


# ===========================================================================
# _standardize_text
# ===========================================================================


class TestStandardizeText:
    def test_lowercase_region_becomes_title_case(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "north"}])
        result = _standardize_text(df)
        assert result.iloc[0]["region"] == "North"

    def test_uppercase_region_becomes_title_case(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "SOUTH"}])
        result = _standardize_text(df)
        assert result.iloc[0]["region"] == "South"

    def test_whitespace_stripped_from_customer_name(self):
        df = pd.DataFrame([{"customer_name": "  alice  ", "region": "North"}])
        result = _standardize_text(df)
        assert result.iloc[0]["customer_name"] == "Alice"

    def test_whitespace_stripped_from_region(self):
        df = pd.DataFrame([{"customer_name": "Alice", "region": "  East  "}])
        result = _standardize_text(df)
        assert result.iloc[0]["region"] == "East"

    def test_already_correct_casing_unchanged(self):
        """Title case input should pass through without modification."""
        df = pd.DataFrame([{"customer_name": "Alice Johnson", "region": "North"}])
        result = _standardize_text(df)
        assert result.iloc[0]["customer_name"] == "Alice Johnson"
        assert result.iloc[0]["region"] == "North"

    def test_messy_text_fixture(self, messy_text):
        """All three messy rows should be normalised correctly."""
        result = _standardize_text(messy_text)
        assert all(r[0].isupper() for r in result["region"].str[0])
        assert all(name == name.strip() for name in result["customer_name"])


# ===========================================================================
# _derive_columns
# ===========================================================================


class TestDeriveColumns:
    def test_total_revenue_calculated(self):
        """total_revenue should equal quantity * unit_price."""
        df = pd.DataFrame([{"quantity": 2, "unit_price": 10.00}])
        result = _derive_columns(df)
        assert result.iloc[0]["total_revenue"] == 20.00

    def test_total_revenue_rounded_to_2dp(self):
        """Result should be rounded to 2 decimal places."""
        df = pd.DataFrame([{"quantity": 3, "unit_price": 1.005}])
        result = _derive_columns(df)
        assert result.iloc[0]["total_revenue"] == 3.02

    def test_total_revenue_column_added(self, clean_row):
        """The column 'total_revenue' should be present after derivation."""
        assert "total_revenue" not in clean_row.columns
        result = _derive_columns(clean_row)
        assert "total_revenue" in result.columns

    def test_revenue_fixture(self, numeric_for_revenue):
        """Verify both rows in the fixture produce correct results."""
        result = _derive_columns(numeric_for_revenue)
        assert result.iloc[0]["total_revenue"] == 20.00
        assert result.iloc[1]["total_revenue"] == 3.02

    def test_zero_quantity_produces_zero_revenue(self):
        df = pd.DataFrame([{"quantity": 0, "unit_price": 99.99}])
        result = _derive_columns(df)
        assert result.iloc[0]["total_revenue"] == 0.00


# ===========================================================================
# _add_metadata
# ===========================================================================


class TestAddMetadata:
    def test_loaded_at_column_added(self, clean_row):
        """The 'loaded_at' column should not exist before and exist after."""
        assert "loaded_at" not in clean_row.columns
        result = _add_metadata(clean_row)
        assert "loaded_at" in result.columns

    def test_loaded_at_is_timezone_aware(self, clean_row):
        """loaded_at must be timezone-aware (UTC), not naive."""
        result = _add_metadata(clean_row)
        ts = result.iloc[0]["loaded_at"]
        assert ts.tzinfo is not None

    def test_loaded_at_is_utc(self, clean_row):
        """loaded_at timezone should be UTC."""
        result = _add_metadata(clean_row)
        ts = result.iloc[0]["loaded_at"]
        assert ts.tzinfo == timezone.utc

    def test_loaded_at_is_recent(self, clean_row):
        """loaded_at should be a recent timestamp — not epoch, not the future."""
        import time

        before = pd.Timestamp.now(tz=timezone.utc).timestamp()
        result = _add_metadata(clean_row)
        after = pd.Timestamp.now(tz=timezone.utc).timestamp()
        ts = result.iloc[0]["loaded_at"].timestamp()
        assert before <= ts <= after


# ===========================================================================
# transform() — INTEGRATION TEST
# ===========================================================================


class TestTransformIntegration:
    """
    Tests for the full public transform() function.

    These tests treat transform() as a black box — they don't care which
    internal step removed a row, only that the correct rows survive and the
    output has the expected shape and types. Think of them as the "contract"
    tests: they define what transform() promises to deliver.
    """

    def test_correct_row_count(self, full_raw_df):
        """15 messy input rows should produce exactly 9 clean output rows."""
        result = transform(full_raw_df)
        assert len(result) == 9

    def test_output_has_total_revenue_column(self, full_raw_df):
        result = transform(full_raw_df)
        assert "total_revenue" in result.columns

    def test_output_has_loaded_at_column(self, full_raw_df):
        result = transform(full_raw_df)
        assert "loaded_at" in result.columns

    def test_no_nulls_in_critical_fields(self, full_raw_df):
        """After transform, no critical field should contain nulls."""
        result = transform(full_raw_df)
        for field in CRITICAL_FIELDS:
            assert result[field].notna().all(), f"Null found in critical field: {field}"

    def test_quantity_is_int_dtype(self, full_raw_df):
        result = transform(full_raw_df)
        assert result["quantity"].dtype == int

    def test_order_date_is_datetime_dtype(self, full_raw_df):
        result = transform(full_raw_df)
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

    def test_no_exact_duplicates_in_output(self, full_raw_df):
        """The output should contain no exact duplicate rows."""
        result = transform(full_raw_df)
        assert result.duplicated().sum() == 0

    def test_total_revenue_values_are_correct(self, full_raw_df):
        """Spot-check a known row: order 1001, qty=2, price=999.99 → 1999.98."""
        result = transform(full_raw_df)
        row_1001 = result[result["order_id"] == 1001]
        assert not row_1001.empty
        assert row_1001.iloc[0]["total_revenue"] == pytest.approx(1999.98)

    def test_regions_are_title_case(self, full_raw_df):
        """All region values in the output should be Title Case."""
        result = transform(full_raw_df)
        for region in result["region"]:
            assert region == region.title(), f"Region not Title Case: {region!r}"

    def test_clean_dataframe_passes_unchanged_row_count(self, clean_row):
        """A DataFrame with one already-clean row should produce one output row."""
        result = transform(clean_row)
        assert len(result) == 1
