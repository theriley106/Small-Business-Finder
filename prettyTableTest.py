import csv

def pad_col(col, max_width):
    return col.ljust(max_width)

with open('addresses.csv') as csvfile:
    reader = csv.reader(csvfile)
    all_rows = []
    for row in reader:
        all_rows.append(row)

max_col_width = [0] * len(all_rows[0])
for row in all_rows:
    for idx, col in enumerate(row):
        max_col_width[idx] = max(len(col), max_col_width[idx])

for row in all_rows:
    to_print = ""
    for idx, col in enumerate(row):
        to_print += pad_col(col, max_col_width[idx]) + " | "
    print("-"*len(to_print))
    print(to_print)