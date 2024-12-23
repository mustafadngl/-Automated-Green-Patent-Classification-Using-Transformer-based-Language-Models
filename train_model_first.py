from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import sqlite3
import pandas as pd

cur = sqlite3.connect('em500database.db')
df_green = pd.read_sql_query("SELECT * FROM g_detail_desc_text_2024_isgreen LIMIT 100", cur) 

# Clean rows with None data
labeled_data = df_green.dropna(subset=['description_text', 'is_green'])

# Ensure 'is_green' is an integer (required for classification)
labeled_data['is_green'] = labeled_data['is_green'].astype(int)

# Create a trainable dataset
hf_dataset = Dataset.from_pandas(labeled_data[['description_text', 'is_green']])

# Tokenize the data
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    tokens = tokenizer(examples['description_text'], truncation=True, padding='max_length')
    tokens['labels'] = examples['is_green']  # Add labels to the tokenized output
    return tokens

tokenized_dataset = hf_dataset.map(tokenize_function, batched=True)

# Train-test split (adjusted for small datasets)
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
test_dataset = train_test_split['test']

# Load model
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    save_total_limit=2,  # Save only the last 2 checkpoints
)

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Evaluate
results = trainer.evaluate()
print(results)

# Save trained model
model.save_pretrained("green_patent_model")
tokenizer.save_pretrained("green_patent_model")
print("Model and tokenizer saved in 'green_patent_model' directory.")
