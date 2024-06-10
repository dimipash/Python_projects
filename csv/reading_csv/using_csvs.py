import csv

with open('employee_birthday.txt') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_counter = 0
    for row in csv_reader:
        if line_counter == 0:
            print(f'Column names are {", ".join(row)}')
            line_counter += 1        
        print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        line_counter += 1

    print(f'Processed {line_counter} lines.')