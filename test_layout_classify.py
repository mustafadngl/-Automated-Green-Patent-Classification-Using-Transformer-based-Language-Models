from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sqlite3
import pandas as pd
import random
from datasets import Dataset

cur = sqlite3.connect('em500database.db')
model_dir = "green_patent_model_trained_granted2024"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

def tokenize_function(examples):
    return tokenizer(examples['description_text'], truncation=True, padding='max_length')

random_offset = random.randint(1, 20000)
query = f"SELECT description_text FROM g_detail_desc_text_2024 LIMIT 10 OFFSET {random_offset}"
df_test = pd.read_sql_query(query, cur)

print("Columns in dataset:", df_test.columns)
labeled_data = df_test.dropna(subset=['description_text'])  
hf_dataset = Dataset.from_pandas(labeled_data[['description_text']]) 

tokenized_dataset_test = hf_dataset.map(tokenize_function, batched=True)

test_texts = [item['description_text'] for item in tokenized_dataset_test]
predictions = []

for text in test_texts:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
        predictions.append(predicted_label)

label_map = {0: "Non-Green", 1: "Green"}
predicted_classes = [label_map[pred] for pred in predictions]

for text, pred_class in zip(test_texts, predicted_classes):
    print(f"Description: {text}\nPredicted Label: {pred_class}\n")
