import sqlite3
import pandas as pd
import re
import json

conn = sqlite3.connect('em500database.db')
cursor = conn.cursor()
table_name_checked = "g_detail_desc_text_2024_isgreen"

#conn.execute(f"DROP TABLE {table_name_checked}") 

with open("green_cpc_keywords.json", "r") as json_file:
    green_data = json.load(json_file)

GREEN_CPC_CODES = green_data["cpc_codes"]
GREEN_KEYWORDS = green_data["keywords"]
escaped_keywords = [re.escape(keyword) for keyword in GREEN_KEYWORDS]

def classify_patent(row):
    """Function to classify a patent as green or not"""
    try:
        description = row['description_text'].lower()
        cpc_code = str(row.get('cpc_code', '')).lower() 
        is_green_cpc = any(code in cpc_code for code in GREEN_CPC_CODES)
        is_green_keyword = any(re.search(keyword, description) for keyword in escaped_keywords)
        return 1 if is_green_cpc or is_green_keyword else 0
    except Exception as e:
        print(f"Error processing row: {row}, Error: {e}")
        return 0 

columns_all = ""
chunk_size = 1000  
offset = 0
count_final = 0
while True:
    query = f"SELECT * FROM g_detail_desc_text_2024 LIMIT {chunk_size} OFFSET {offset}"
    chunk_df = pd.read_sql_query(query, conn)
    print(chunk_df.head())
    if not columns_all:
        cols = list(chunk_df.columns) + ["is_green"]
        columns_all = ", ".join(f"{header} TEXT" for header in cols)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name_checked}({columns_all});")
    chunk_df['is_green'] = chunk_df.apply(classify_patent, axis=1)
    if chunk_df.empty:
        break
    chunk_df.to_sql(table_name_checked, conn, if_exists='append', index=False)
    offset += chunk_size
    count_final += chunk_df['is_green'].value_counts()
#data = pd.concat(dfs)
conn.commit()
conn.close()
print(count_final) # =241911.0 for  granted patents in 2024
