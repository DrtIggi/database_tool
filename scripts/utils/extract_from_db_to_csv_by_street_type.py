import sqlite3
import pandas as pd

# Database and output file paths
db_path = "../../db/dataset.db"   # Update with your actual SQLite file
csv_output = "aeroport.csv"  # Output CSV file
street_type_filter = "усиевича"  # Update with the street type you want to filter

# Connect to SQLite database
conn = sqlite3.connect(db_path)

# Define SQL query to filter data
query = f"SELECT * FROM table1 WHERE street = '{street_type_filter}'"

# Read the filtered data into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Save the DataFrame as a CSV file
df.to_csv(csv_output, index=False, encoding="utf-8")

# Close the database connection
conn.close()

print(f"Filtered data saved to {csv_output}")
