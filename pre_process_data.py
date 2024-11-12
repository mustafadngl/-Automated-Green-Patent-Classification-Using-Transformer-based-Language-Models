import pandas as pd
from datasets import Dataset

with open("ipg240102.xml", "r") as file:
    content = file.read()

parts = content.split('<?xml version="1.0" encoding="UTF-8"?>\n')
for part in parts:
    if part.strip():
        part_cleaned = '<?xml version="1.0" encoding="UTF-8"?>\n' + part
        # Veri yükleme
        data = pd.read_xml(part_cleaned)
        print(data.columns)

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


