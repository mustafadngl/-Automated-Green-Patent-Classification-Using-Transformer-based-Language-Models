from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import sqlite3
import pandas as pd

cur = sqlite3.connect('em500database.db')
#df_green = pd.read_sql_query("SELECT * FROM g_detail_desc_text_2024_isgreen", cur) 
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

def tokenize_function(examples):
    tokens = tokenizer(examples['description_text'], truncation=True, padding='max_length')
    tokens['labels'] = examples['is_green']  # Add labels to the tokenized output
    return tokens

chunk_size = 100  
offset = 0
df_green = []
while True:
    print(offset)
    query = f"SELECT * FROM g_detail_desc_text_2024_isgreen LIMIT {chunk_size} OFFSET {offset}"
    df_green = pd.read_sql_query(query, cur)
    print(df_green.head())
    if df_green.empty:
        break
    #if offset > 10000:
    #    break
    labeled_data = df_green.dropna(subset=['description_text', 'is_green'])
    labeled_data['is_green'] = labeled_data['is_green'].astype(int)
    hf_dataset = Dataset.from_pandas(labeled_data[['description_text', 'is_green']])
    tokenized_dataset = hf_dataset.map(tokenize_function, batched=True)
    #train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
    #train_dataset = train_test_split['train']
    #test_dataset = train_test_split['test']

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        save_total_limit=2, 
    )

    # Define Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,#train_dataset,
        eval_dataset=tokenized_dataset,#test_dataset,
        processing_class=tokenizer,
    )
    # Train the model
    offset += chunk_size
    trainer.train()

# Evaluate
#results = trainer.evaluate()
#print(results)

# Save trained model
model.save_pretrained("green_patent_model_trained_granted2024")
tokenizer.save_pretrained("green_patent_model_trained_granted2024")
print("Model and tokenizer saved in 'green_patent_model_trained_granted2024' directory.")
