from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, accuracy_score
import torch

model_dir = "green_patent_model_trained_granted2024"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Example: Load test dataset (if it's saved or still available in memory) ???
# Use the already tokenized test_dataset from earlier or re-tokenize your test data
test_texts = [item['description_text'] for item in test_dataset]  # Original test descriptions
test_labels = [item['labels'] for item in test_dataset]  # True labels

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

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")

report = classification_report(true_labels, predictions, target_names=["Non-Green", "Green"])
print("\nClassification Report:\n")
print(report)

print("\nSummary of Results:")
print(f"- Total Samples: {len(true_labels)}")
print(f"- Correctly Classified: {sum(1 for t, p in zip(true_labels, predictions) if t == p)}")
print(f"- Incorrectly Classified: {sum(1 for t, p in zip(true_labels, predictions) if t != p)}")