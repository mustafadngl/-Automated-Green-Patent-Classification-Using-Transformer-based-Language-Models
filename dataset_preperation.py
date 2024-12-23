# Parsing XML data to extract abstracts and classifications
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    abstracts = []
    classifications = []
    
    # Traverse through each patent element
    for patent in root.findall('.//us-patent-grant'): 
        abstract_text = patent.findtext('abstract')
        classification = patent.findtext('.//classification-ipc')
        
        if abstract_text and classification:
            abstracts.append(abstract_text.strip())
            classifications.append(classification.strip())
    
    return pd.DataFrame({'abstract': abstracts, 'classification': classifications})

# Load and preprocess the data
data = parse_xml("path_to_patent_data.xml")

# Create a binary label for "green" patents
data['label'] = data['classification'].apply(lambda x: 1 if "green" in x.lower() else 0)
data = data.dropna(subset=['abstract'])  # Remove rows with missing abstracts
