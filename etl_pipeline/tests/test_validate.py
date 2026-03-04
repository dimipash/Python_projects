import pandas as pd
import pytest

gx = pytest.importorskip("great_expectations")

from validate import VALID_REGIONS, DataQualityError, validate_clean, validate_raw


def make_raw_row(**overrides) -> dict:
    defaults = {
        "order_id": 1001,
        "customer_name": "Alice Johnson",
        "product": "Laptop",
        "quantity": "2",
        "unit_price": "999.99",
        "order_date": "2024-01-15",
        "region": "North",
    }
    return {**defaults, **overrides}


def make_clean_row(**overrides) -> dict:
    defaults = {
        "order_id": 1001,
        "customer_name": "Alice Johnson",
        "product": "Laptop",
        "quantity": 2,
        "unit_price": 999.99,
        "order_date": pd.Timestamp("2024-01-15"),
        "region": "North",
        "total_revenue": 1999.98,
        "loaded_at": pd.Timestamp("2024-01-28 06:00:00", tz="UTC"),
    }
    return {**defaults, **overrides}


class TestValidateRaw:
    def test_passes_valid_data(self):
        df = pd.DataFrame([make_raw_row()])
        assert validate_raw(df, action="halt") is True

    def test_passes_multiple_valid_rows(self):
        df = pd.DataFrame([make_raw_row(order_id=i) for i in range(1, 6)])
        assert validate_raw(df, action="halt") is True

    def test_halts_on_missing_column(self):
        df = pd.DataFrame([make_raw_row()])
        df = df.drop(columns=["region"])
        with pytest.raises(DataQualityError, match="region"):
            validate_raw(df, action="halt")

    def test_warns_on_missing_column(self):
        df = pd.DataFrame([make_raw_row()])
        df = df.drop(columns=["region"])
        result = validate_raw(df, action="warn")
        assert result is False

    def test_halts_on_empty_dataframe(self):
        df = pd.DataFrame(columns=list(make_raw_row().keys()))
        with pytest.raises(DataQualityError):
            validate_raw(df, action="halt")

    def test_halts_on_null_order_id(self):
        df = pd.DataFrame([make_raw_row(order_id=None)])
        with pytest.raises(DataQualityError):
            validate_raw(df, action="halt")

    def test_does_not_halt_on_null_non_critical_field(self):
        df = pd.DataFrame([make_raw_row(customer_name=None)])
        assert validate_raw(df, action="halt") is True

    def test_allows_dirty_data_through(self):
        df = pd.DataFrame([make_raw_row(quantity="abc", order_date="not-a-date")])
        assert validate_raw(df, action="halt") is True


class TestValidateClean:
    def test_passes_valid_clean_data(self):
        df = pd.DataFrame([make_clean_row()])
        assert validate_clean(df, action="halt") is True

    def test_passes_multiple_rows(self):
        df = pd.DataFrame([make_clean_row(order_id=i) for i in range(1, 6)])
        assert validate_clean(df, action="halt") is True

    def test_halts_on_null_customer_name(self):
        df = pd.DataFrame([make_clean_row(customer_name=None)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_null_region(self):
        df = pd.DataFrame([make_clean_row(region=None)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_invalid_region(self):
        df = pd.DataFrame([make_clean_row(region="InvalidRegion")])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_valid_regions_accepted(self):
        for region in VALID_REGIONS:
            df = pd.DataFrame([make_clean_row(region=region)])
            assert validate_clean(df, action="halt") is True

    def test_halts_on_zero_quantity(self):
        df = pd.DataFrame([make_clean_row(quantity=0)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_negative_quantity(self):
        df = pd.DataFrame([make_clean_row(quantity=-1)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_zero_unit_price(self):
        df = pd.DataFrame([make_clean_row(unit_price=0.0)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_duplicate_order_id(self):
        df = pd.DataFrame([make_clean_row(order_id=1), make_clean_row(order_id=1)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_halts_on_null_total_revenue(self):
        df = pd.DataFrame([make_clean_row(total_revenue=None)])
        with pytest.raises(DataQualityError):
            validate_clean(df, action="halt")

    def test_warns_instead_of_halting(self):
        df = pd.DataFrame([make_clean_row(region="BadRegion")])
        result = validate_clean(df, action="warn")
        assert result is False

    def test_valid_regions_constant(self):
        assert VALID_REGIONS == {"North", "South", "East", "West"}


class TestDataQualityError:
    def test_is_exception_subclass(self):
        assert issubclass(DataQualityError, Exception)

    def test_message_preserved(self):
        try:
            raise DataQualityError("suite failed: expect_column_to_exist(region)")
        except DataQualityError as e:
            assert "region" in str(e)
