import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# BASE FACTORY
# ---------------------------------------------------------------------------


def make_row(**overrides) -> dict:
    """
    Return a dict representing one valid sales row, with optional overrides.

    Using a factory function (rather than a hardcoded dict in each fixture)
    means we only define the "default valid row" once. To test a null
    customer_name, you write: make_row(customer_name=None).

    This pattern — a valid baseline with targeted overrides — is the cleanest
    way to test data cleaning functions because the test communicates exactly
    which field is being exercised and why the row is expected to fail.
    """
    defaults = {
        "order_id": 1001,
        "customer_name": "Alice Johnson",
        "product": "Laptop",
        "quantity": 2,
        "unit_price": 999.99,
        "order_date": "2024-01-15",
        "region": "North",
    }
    return {**defaults, **overrides}


# ---------------------------------------------------------------------------
# CORE FIXTURES
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_row() -> pd.DataFrame:
    """A single fully valid row. Used as a baseline — should always survive."""
    return pd.DataFrame([make_row()])


@pytest.fixture
def duplicate_rows() -> pd.DataFrame:
    """Two rows that are identical in every field — one should be removed."""
    row = make_row()
    return pd.DataFrame([row, row])


@pytest.fixture
def null_rows() -> pd.DataFrame:
    """
    Four rows testing null behaviour:
      - null customer_name  → critical field, should be dropped
      - null product        → critical field, should be dropped
      - null region         → critical field, should be dropped
      - null order_id       → non-critical field, should be kept
    """
    return pd.DataFrame(
        [
            make_row(customer_name=None),  # dropped
            make_row(product=None),  # dropped
            make_row(region=None),  # dropped
            make_row(order_id=None),  # kept — order_id is not critical
        ]
    )


@pytest.fixture
def bad_numerics() -> pd.DataFrame:
    """
    Three rows testing numeric coercion:
      - "abc" quantity   → cannot be coerced, should be dropped
      - null quantity    → NaN after coercion, should be dropped
      - valid quantity   → should be kept and cast to int
    """
    return pd.DataFrame(
        [
            make_row(quantity="abc"),  # dropped
            make_row(quantity=None),  # dropped
            make_row(quantity=3),  # kept
        ]
    )


@pytest.fixture
def bad_dates() -> pd.DataFrame:
    """
    Two rows testing date coercion:
      - "not-a-date"   → cannot be parsed, should be dropped
      - valid date     → should be kept and cast to datetime
    """
    return pd.DataFrame(
        [
            make_row(order_date="not-a-date"),  # dropped
            make_row(order_date="2024-01-15"),  # kept
        ]
    )


@pytest.fixture
def messy_text() -> pd.DataFrame:
    """
    Three rows testing text standardisation:
      - lowercase region        → "north"    should become "North"
      - uppercase region        → "SOUTH"    should become "South"
      - whitespace-padded name  → " alice "  should become "Alice"
    """
    return pd.DataFrame(
        [
            make_row(region="north"),
            make_row(region="SOUTH"),
            make_row(customer_name=" alice "),
        ]
    )


@pytest.fixture
def numeric_for_revenue() -> pd.DataFrame:
    """
    Rows with specific values for testing total_revenue calculation.
    quantity=2, unit_price=10.00  →  total_revenue should be 20.00
    quantity=3, unit_price=1.005  →  total_revenue should be 3.02 (rounded)
    """
    return pd.DataFrame(
        [
            make_row(quantity=2, unit_price=10.00),
            make_row(quantity=3, unit_price=1.005),
        ]
    )


@pytest.fixture
def full_raw_df() -> pd.DataFrame:
    """
    Mirrors the real data/sales_raw.csv exactly.
    Used for the integration test of transform() — verifies end-to-end
    that 15 rows in produces exactly 9 clean rows out.

    If you change sales_raw.csv, update this fixture to match.
    """
    return pd.DataFrame(
        [
            make_row(
                order_id=1001,
                customer_name="Alice Johnson",
                product="Laptop",
                quantity=2,
                unit_price=999.99,
                order_date="2024-01-15",
                region="North",
            ),
            make_row(
                order_id=1002,
                customer_name="Bob Smith",
                product="Mouse",
                quantity=5,
                unit_price=29.99,
                order_date="2024-01-16",
                region="South",
            ),
            make_row(
                order_id=1003,
                customer_name=None,
                product="Keyboard",
                quantity=1,
                unit_price=79.99,
                order_date="2024-01-17",
                region="East",
            ),  # null name
            make_row(
                order_id=1004,
                customer_name="Carol White",
                product="Monitor",
                quantity="abc",
                unit_price=349.99,
                order_date="2024-01-18",
                region="West",
            ),  # bad quantity
            make_row(
                order_id=1005,
                customer_name="Dave Brown",
                product="Laptop",
                quantity=1,
                unit_price=999.99,
                order_date="not-a-date",
                region="North",
            ),  # bad date
            make_row(
                order_id=1006,
                customer_name="Eve Davis",
                product="Headset",
                quantity=3,
                unit_price=149.99,
                order_date="2024-01-20",
                region="South",
            ),
            make_row(
                order_id=1007,
                customer_name="Frank Miller",
                product="Mouse",
                quantity=2,
                unit_price=29.99,
                order_date="2024-01-21",
                region=None,
            ),  # null region
            make_row(
                order_id=1008,
                customer_name="Grace Lee",
                product="Webcam",
                quantity=1,
                unit_price=89.99,
                order_date="2024-01-22",
                region="East",
            ),
            make_row(
                order_id=1009,
                customer_name="Alice Johnson",
                product="Mouse",
                quantity=5,
                unit_price=29.99,
                order_date="2024-01-16",
                region="South",
            ),
            make_row(
                order_id=1002,
                customer_name="Bob Smith",
                product="Mouse",
                quantity=5,
                unit_price=29.99,
                order_date="2024-01-16",
                region="South",
            ),  # exact duplicate of row 2
            make_row(
                order_id=1010,
                customer_name="Hank Wilson",
                product="Keyboard",
                quantity=None,
                unit_price=79.99,
                order_date="2024-01-23",
                region="West",
            ),  # null quantity
            make_row(
                order_id=1011,
                customer_name="Ivy Moore",
                product="Laptop",
                quantity=1,
                unit_price=999.99,
                order_date="2024-01-24",
                region="North",
            ),
            make_row(
                order_id=1012,
                customer_name=None,
                product="Headset",
                quantity=None,
                unit_price=149.99,
                order_date="2024-01-25",
                region="South",
            ),  # null name + null qty
            make_row(
                order_id=1013,
                customer_name="Jack Taylor",
                product="Monitor",
                quantity=2,
                unit_price=349.99,
                order_date="2024-01-26",
                region="East",
            ),
            make_row(
                order_id=1014,
                customer_name="Karen Anderson",
                product="Webcam",
                quantity=3,
                unit_price=89.99,
                order_date="2024-01-27",
                region="West",
            ),
        ]
    )
