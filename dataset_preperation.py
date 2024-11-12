from datasets import Dataset

train_data = data.sample(frac=0.8, random_state=42)
test_data = data.drop(train_data.index)

train_dataset = Dataset.from_pandas(train_data)
test_dataset = Dataset.from_pandas(test_data)