import os
import csv
import json
from typing import Tuple


def parse_expense_row(row: list) -> Tuple[str, str, float, str, str, str]:
    """Parse a row from the CSV file and return the relevant data."""
    if len(row) < 6:
        print(f"Row does not have enough columns, skipping: {row}")
        return None

    date, details, amount, currency, transaction_type, status = row
    amount = amount.replace(",", "")

    try:
        amount_float = float(amount)
    except ValueError:
        print(f"Failed to convert amount to float: {amount}")
        return None

    return date, details, amount_float, currency, transaction_type.strip(), status


def sum_expenses_for_month(csv_file_path: str) -> float:
    """Calculate the total expenses for the given month."""
    total_expenses = 0.0

    with open(csv_file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row

        for row in reader:
            expense = parse_expense_row(row)
            if expense and expense[4].lower() == "debit":
                total_expenses += expense[2]

    return total_expenses


def update_expenses_json(
    json_file_path: str, month: str, total_expenses: float
) -> None:
    """Update the monthly expenses data in the JSON file."""
    expenses_data = {}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            expenses_data = json.load(json_file)

    expenses_data[month] = total_expenses

    with open(json_file_path, "w") as json_file:
        json.dump(expenses_data, json_file, indent=4)


def main():
    month_input = input("Please enter a month (format: YYYY-MM): ")
    csv_file_name = "transactions.csv"
    json_file_name = "monthly_expenses.json"

    total_month_expenses = sum_expenses_for_month(csv_file_name)
    print(f"Total expenses for {month_input}: {total_month_expenses:.2f}")

    update_expenses_json(json_file_name, month_input, total_month_expenses)


if __name__ == "__main__":
    main()
