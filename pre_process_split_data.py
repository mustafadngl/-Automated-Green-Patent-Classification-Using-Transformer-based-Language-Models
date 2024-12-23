import pandas as pd
from datasets import Dataset
import xml.etree.ElementTree as ET
import os



path = "data/ipg240102.xml"
name_first = path.split("/")[1]
name = name_first.split(".")[0]
folder_path = f"data_processed/{name}"
os.makedirs(folder_path, exist_ok=True)
with open(path, "r") as file:
    content = file.read()

parts = content.split('<?xml version="1.0" encoding="UTF-8"?>\n')
for index, part in enumerate(parts):
    if part.strip():
        part_cleaned = '<?xml version="1.0" encoding="UTF-8"?>\n' + part
        file_name = f"processed_{name}_{index}.xml"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(part_cleaned)
        # Veri yükleme
        #data = pd.read_xml(part_cleaned)
        #print(data.columns)

        ## İlgili sütunları seçme ve eksik verileri temizleme
        #data = data[['abstract', 'classification']].dropna()
        #data = data[data['abstract'].str.len() > 20]  # Çok kısa açıklamaları çıkarıyoruz
#
        ## Yeşil patent etiketi oluşturma: "green" içeren sınıfları pozitif (1), diğerlerini negatif (0) olarak etiketliyoruz
        #data['label'] = data['classification'].apply(lambda x: 1 if "green" in x.lower() else 0)
#
        ## Eğitim ve test kümelerine ayırma
        #train_data = data.sample(frac=0.8, random_state=42)
        #test_data = data.drop(train_data.index)
#
        ## Dataset formatına dönüştürme
        #train_dataset = Dataset.from_pandas(train_data)
        #test_dataset = Dataset.from_pandas(test_data)


