import csv

# Data to be written into the CSV file
row_data = ['Doe', 25, 'New York']

# Open the CSV file in write mode and create a CSV writer object
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the row data into the CSV file
    writer.writerow(row_data)