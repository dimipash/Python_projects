# Expense Tracker

This Python application helps you track and analyze your monthly expenses by processing transaction data from a CSV file and storing the results in a JSON file.

## Features

- Parse transaction data from a CSV file
- Calculate total expenses for a specified month
- Update and store monthly expense data in a JSON file
- Handle various error cases and data inconsistencies

## Requirements

- Python 3.6+
- CSV file named `transactions.csv` in the same directory as the script
- (Optional) Existing `monthly_expenses.json` file for storing expense data

## Usage

1. Ensure your transaction data is in a CSV file named `transactions.csv` in the same directory as the script.
2. Run the script:
   ```
   python expense_tracker.py
   ```
3. When prompted, enter the month for which you want to calculate expenses in the format YYYY-MM (e.g., 2023-04 for April 2023).
4. The script will output the total expenses for the specified month and update the `monthly_expenses.json` file with the new data.

## CSV File Format

The `transactions.csv` file should have the following columns:

1. Date
2. Details
3. Amount
4. Currency
5. Transaction Type
6. Status

Ensure that the CSV file has a header row with these column names.

## Functions

### `parse_expense_row(row: list) -> Tuple[str, str, float, str, str, str]`

Parses a row from the CSV file and returns the relevant data as a tuple.

### `sum_expenses_for_month(csv_file_path: str) -> float`

Calculates the total expenses for the given month based on the data in the CSV file.

### `update_expenses_json(json_file_path: str, month: str, total_expenses: float) -> None`

Updates the monthly expenses data in the JSON file.

### `main()`

The main function that orchestrates the expense tracking process.

## Error Handling

The script includes error handling for:

- Rows with insufficient columns
- Non-numeric amount values
- Missing CSV or JSON files
