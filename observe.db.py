import sqlite3
import csv
con = sqlite3.connect("em500database.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM g_detail_desc_text_2024 LIMIT 10")
row = cur.fetchone()

# Define the CSV filename
csv_filename = "output.csv"

# Open a CSV file and write the row
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(row)  # Write the row to the CSV file

print(f"Row has been written to {csv_filename}")

# Close the connection
con.close()