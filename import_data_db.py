import sqlite3
import csv
import sys


csv.field_size_limit(10**9)

tsv_file_path = "./tsv_files/g_detail_desc_text_2024.tsv"  
sqlite_db_path = "em500database.db"  
table_name = "g_detail_desc_text_2024"          


conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()


with open(tsv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    headers = next(reader) 
    columns = ", ".join(f"{header} TEXT" for header in headers)  


cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")

with open(tsv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader) 
    for row in reader:
        placeholders = ", ".join("?" for _ in row) 
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", row)

conn.commit()
conn.close()

print(f"Data from {tsv_file_path} has been successfully imported into the {table_name} table in {sqlite_db_path}.")
