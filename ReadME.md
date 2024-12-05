This is a model training project in order to specify green data. An Example .xml file has demonstrated in repo. Aim is use last 2 years grandted and application data in order to classify patent "green" or not.

1. pip install datasets (hugginface library in order to prepare dataset for model train)
*requirement.txt will be provided for used stack.

*data_collection branch demonstrates an example output for a patent data which is extracted from USPTO database.m

## Step 1:
     Data collection has been performed from USPTO website. "g_cpc_title.tsv" and "g_detail_desc_text_2024" data gathered. Because of the storage and memory efficiency "g_detail_desc_text_2024" data (approximetely 14.7 gigabyte (GB)) has ben imported to SQLite database via "import_data_db.py". And "output.csv" has been generated in order to demonstrated an patent data as an example to raw dataset via "obserce_db.py".
## Step 2:
     Needed to extract cpc codes and keywords related "green" terms. "green_cpc_keywords.json" file has been created via script "pull_green_cpc_codes_and_keywords.py".
## Step 3:
     Granted data (from database g_detail_desc_text_2024 table) has been classified as "green" terms. Imported to database.
