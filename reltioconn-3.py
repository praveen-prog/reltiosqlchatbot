import csv
import sqlite3
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for credentials and endpoints

patient_data_endpoint = os.getenv("patient_data_endpoint")
table_name = os.path.basename(patient_data_endpoint)

# Define the path to your CSV file
csv_file_path = 'outputflattened.csv'

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Read the CSV file to get column names and rows
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # Get column names dynamically from the CSV file
    columns = reader.fieldnames
    
    # Generate the CREATE TABLE SQL statement dynamically based on column names
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} TEXT' for col in columns])});"
    cursor.execute(create_table_query)

    # Prepare the INSERT INTO SQL statement
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])});"

    # Insert each row into the SQLite table
    for row in reader:
        # Convert row values to a tuple, which is required for `execute`
        values = tuple(row[col] for col in columns)
        cursor.execute(insert_query, values)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data has been inserted into the SQLite database successfully.")
