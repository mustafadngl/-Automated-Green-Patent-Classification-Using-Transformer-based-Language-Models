This is a model training project in order to specify green data. An Example .xml file has demonstrated in repo. Aim is use last 2 years grandted and application data in order to classify patent "green" or not.

# In order to process any python file in the project follow the process below accordingly:
## Create a virtual environment in order to make sure requirements has been imported from Command Line Interface (CLI or terminal).
     python -m venv .venv
## Install requirements. ('requirement.txt' provided for used stack). Also, torch library can be need to installed seperately if used script throws an error. 
     pip insrall -r requrements.txt     
*    pip3 install torch torchvision torchaudio
     pip install transformers[torch]
## Then from Command Line Interface (CLI or terminal)
     python <python_script_name>
*data_collection branch demonstrates an example output for a patent data which is extracted from USPTO database.m

# Below Steps have been performed while training model.
### Step 1:
Data collection has been performed from USPTO website. "g_cpc_title.tsv" and "g_detail_desc_text_2024" data gathered. Because of the storage and memory efficiency "g_detail_desc_text_2024" data (approximetely 14.7 gigabyte (GB)) has ben imported to SQLite database via "import_data_db.py". And "output.csv" has been generated in order to demonstrated an patent data as an example to raw dataset via "obserce_db.py".
### Step 2:
Needed to extract cpc codes and keywords related "green" terms. "green_cpc_keywords.json" file has been created via script "pull_green_cpc_codes_and_keywords.py".
### Step 3:
Granted data (from database g_detail_desc_text_2024 table) has been classified as "green" terms. Imported to database vias 'label_data.py' script.
## Step 4:
Selected model has been trained via !train_model_first.py' in order to observe code reliability and process time in local machine. Later in order to train via mass data, 'train_model_all.py' has been used.
Example a part of training instance in terminal:
***
Map: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:01<00:00, 88.74 examples/s]
Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
{'eval_loss': 0.09320060908794403, 'eval_runtime': 3.277, 'eval_samples_per_second': 6.103, 'eval_steps_per_second': 0.915, 'epoch': 1.0}
{'eval_loss': 0.03281847760081291, 'eval_runtime': 3.4369, 'eval_samples_per_second': 5.819, 'eval_steps_per_second': 0.873, 'epoch': 2.0}
{'eval_loss': 0.023905927315354347, 'eval_runtime': 3.3778, 'eval_samples_per_second': 5.921, 'eval_steps_per_second': 0.888, 'epoch': 3.0}
{'train_runtime': 204.0818, 'train_samples_per_second': 1.176, 'train_steps_per_second': 0.147, 'train_loss': 0.12877427736918132, 'epoch': 3.0}
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 30/30 [03:24<00:00,  6.80s/it]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:01<00:00,  1.55it/s]
{'eval_loss': 0.023905927315354347, 'eval_runtime': 3.2466, 'eval_samples_per_second': 6.16, 'eval_steps_per_second': 0.924, 'epoch': 3.0}
Model and tokenizer saved in 'green_patent_model_100' directory.
***
## Step 5:
In order to test model result a script has been created ('test_layout.py'). Will be optimized.

