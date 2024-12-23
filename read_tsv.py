import pandas as pd
import os

file_path = "./tsv_files/g_detail_desc_text_2024.tsv"
print(os.access(file_path, os.R_OK))
print(os.access(file_path, os.W_OK)) 
try:
    data = pd.read_csv(file_path, delimiter='\t')
    data.to_parquet("./tsv_files/parquet/g_detail_desc_text_2024.parquet")
    print("Red")
    print(data.head())
except FileNotFoundError:
    print("File not found. Please check the file path.")
except PermissionError:
    print("Permission denied. Please check your file permissions.")
except Exception as e:
    print(f"An error occurred: {e}")

# Stream the file line by line
#file_path = "./tsv_files/g_detail_desc_text_2024.tsv"
#
#with open(file_path, 'r', encoding='utf-8') as file:
#    for i, line in enumerate(file):
#        if i == 5:  
#            break
#        print(line.strip().split('\t')) 
