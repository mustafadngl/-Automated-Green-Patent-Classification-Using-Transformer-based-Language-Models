from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, accuracy_score
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
    tokens = tokenizer(examples['description_text'], truncation=True, padding='max_length')
    #tokens['labels'] = examples['is_green']  # Add labels to the tokenized output
    return tokens
random_offset = random.randint(1,20000)
query = f"SELECT * FROM g_detail_desc_text_2024 LIMIT 10 OFFSET {random_offset}"
df_test = pd.read_sql_query(query, cur)
labeled_data = df_test.dropna(subset=['description_text']) #'is_green'
#labeled_data['is_green'] = len(labeled_data.index)*[0]#labeled_data['is_green'].astype(int)
hf_dataset = Dataset.from_pandas(labeled_data[['description_text']])#, 'is_green'(may attend later)
tokenized_dataset_test = hf_dataset.map(tokenize_function, batched=True)

test_texts = [item['description_text'] for item in tokenized_dataset_test]  # Original test descriptions
test_labels = [random.randint(0, 1) for _ in range(len(test_texts))] #Randomly stated classificion results.

predictions = []
true_labels = []

for text, true_label in zip(test_texts, test_labels):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
    
    predictions.append(predicted_label)
    true_labels.append(true_label)

accuracy = accuracy_score(true_labels, predictions)
precision = precision_score(true_labels, predictions)
recall = recall_score(true_labels, predictions)
f1 = f1_score(true_labels, predictions)

print(true_labels, predictions)
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")

report = classification_report(true_labels, predictions, target_names=["Non-Green", "Green"],  labels=[0, 1]) 
print("\nClassification Report:\n")
print(report)

print("\nSummary of Results:")
print(f"- Total Samples: {len(true_labels)}")
print(f"- Correctly Classified: {sum(1 for t, p in zip(true_labels, predictions) if t == p)}")
print(f"- Incorrectly Classified: {sum(1 for t, p in zip(true_labels, predictions) if t != p)}")
