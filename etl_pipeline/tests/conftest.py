import pandas as pd
import pytest


def make_row(**overrides) -> dict:
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


@pytest.fixture
def clean_row() -> pd.DataFrame:
    return pd.DataFrame([make_row()])


@pytest.fixture
def duplicate_rows() -> pd.DataFrame:
    row = make_row()
    return pd.DataFrame([row, row])


@pytest.fixture
def null_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_row(customer_name=None),
            make_row(product=None),
            make_row(region=None),
            make_row(order_id=None),
        ]
    )


@pytest.fixture
def bad_numerics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_row(quantity="abc"),
            make_row(quantity=None),
            make_row(quantity=3),
        ]
    )


@pytest.fixture
def bad_dates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_row(order_date="not-a-date"),
            make_row(order_date="2024-01-15"),
        ]
    )


@pytest.fixture
def messy_text() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_row(region="north"),
            make_row(region="SOUTH"),
            make_row(customer_name=" alice "),
        ]
    )


@pytest.fixture
def numeric_for_revenue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_row(quantity=2, unit_price=10.00),
            make_row(quantity=3, unit_price=1.005),
        ]
    )


@pytest.fixture
def full_raw_df() -> pd.DataFrame:
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
            ),
            make_row(
                order_id=1004,
                customer_name="Carol White",
                product="Monitor",
                quantity="abc",
                unit_price=349.99,
                order_date="2024-01-18",
                region="West",
            ),
            make_row(
                order_id=1005,
                customer_name="Dave Brown",
                product="Laptop",
                quantity=1,
                unit_price=999.99,
                order_date="not-a-date",
                region="North",
            ),
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
            ),
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
            ),
            make_row(
                order_id=1010,
                customer_name="Hank Wilson",
                product="Keyboard",
                quantity=None,
                unit_price=79.99,
                order_date="2024-01-23",
                region="West",
            ),
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
            ),
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
