# import csv
# import pandas as pd
# input_file = "../../db/DIT.txt"   # Change to your file name
# output_file = "../../db/db.csv"      # Desired output file name

# df = pd.read_csv(input_file, sep="|", on_bad_lines="skip", low_memory=False)

# # Replace '\N' with an empty value or 'NULL'
# df.replace("\\N", "", inplace=True)  # Use "NULL" instead of "" if needed

# # Save as CSV
# df.to_csv(output_file, index=False, encoding="utf-8")

# print(f"Conversion complete! CSV saved as {output_file}")

import pandas as pd

# File paths
input_file = "input/input.csv"  # Change this to your actual input file
output_file = "input/input.csv" # Output file

# Read the semicolon-separated CSV
df = pd.read_csv(input_file, sep=";", dtype=str)  # Read as strings to preserve formatting

# Save as comma-separated CSV
df.to_csv(output_file, sep=",", index=False, encoding="utf-8")

print(f"Conversion complete! CSV saved as {output_file}")
