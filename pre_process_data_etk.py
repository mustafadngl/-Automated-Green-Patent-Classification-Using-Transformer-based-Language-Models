import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    abstracts = []
    classifications = []
    
    for patent in root.findall('.//us-patent-grant'): 
        abstract_text = patent.findtext('abstract')
        classification = patent.findtext('.//classification-ipc')
        
        if abstract_text and classification:
            abstracts.append(abstract_text.strip())
            classifications.append(classification.strip())
    
    return pd.DataFrame({'abstract': abstracts, 'classification': classifications})


data = parse_xml("ipg240102.xml")
print(data.columns)

data['label'] = data['classification'].apply(lambda x: 1 if "green" in x.lower() else 0)
data = data.dropna(subset=['abstract'])  # Remove rows with missing abstracts
