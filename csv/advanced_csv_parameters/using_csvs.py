"""
CSV File Reader

This script reads a CSV file with a pipe (|) delimiter and prints information about each row.
It displays column names and formatted data for each entry, including name, address, and join date.
The script also counts and reports the total number of lines processed.
"""

import csv

with open("different_delim.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter="|")
    line_counter = 0
    for row in csv_reader:
        if line_counter == 0:
            print(f'Column names are {", ".join(row)}')
            line_counter += 1
        print(
            f'\t{row["name"]} lives at {row["address"]} and joined on {row["date joined"]}.'
        )
        line_counter += 1

    print(f"Processed {line_counter} lines.")
