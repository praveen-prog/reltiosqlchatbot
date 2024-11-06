import csv

with open('outputjson.csv', 'r') as infile, open('outputattributes.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Assuming the column you want is the first one (index 0)
    column_index = 6

    for row in reader:
        writer.writerow([row[column_index]])