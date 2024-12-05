import sqlite3
import csv
con = sqlite3.connect("em500database.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM g_detail_desc_text_2024 LIMIT 10")
#names = [description[0] for description in cur.description]
#print(names)
row = cur.fetchone()

csv_filename = 'output.csv'
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(row) 

print(f"Row has been written to {csv_filename}")

con.close()