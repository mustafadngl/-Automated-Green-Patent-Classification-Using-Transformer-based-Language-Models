import xml.etree.ElementTree as ET
import pandas as pd
import re

# Define green CPC codes and green-related keywords
GREEN_CPC_CODES = ['Y02', 'F03D', 'H02J50']  # Example CPC codes for green technologies
GREEN_KEYWORDS = [
    r'\bsustainable\b', r'\brenewable energy\b', r'\bsolar\b', r'\bwind\b',
    r'\bcarbon capture\b', r'\benergy efficiency\b', r'\bbiofuel\b'
]

# Function to parse the XML file and extract relevant data
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for patent in [root]:
    # Extract relevant fields
    abstract = root.findtext('.//abstract')
    cpc_codes = [cpc.text for cpc in root.findall('.//classification-cpc-text')]
    title = root.findtext('.//invention-title')
    claim = [claim.text for claim in root.findall('.//claim-text')]
    description_drawings = [desc_draw.text for desc_draw in root.findall('.//description-of-drawings')]

    print(description_drawings)

    # Skip if no abstract or title
    #if not abstract or not title:
    #    continue

    # Combine CPC codes into a single string for filtering
    cpc_combined = " ".join(cpc_codes)
    claim_combined = " ".join(claim)

    # Append data for processing
    data.append({
        "abstract": abstract.strip(),
        "cpc_codes": cpc_combined.strip(),
        "title": title.strip()
    })
    
    return pd.DataFrame(data)

# Function to filter patents based on CPC codes and keywords
def filter_patents(data):
    filtered = []
    for _, row in data.iterrows():
        if (any(cpc in row['cpc_codes'] for cpc in GREEN_CPC_CODES) or 
            any(re.search(keyword, row['abstract'], re.IGNORECASE) for keyword in GREEN_KEYWORDS) or
            any(re.search(keyword, row['title'], re.IGNORECASE) for keyword in GREEN_KEYWORDS)):
            filtered.append(row)

    return pd.DataFrame(filtered)

# Parse and filter the XML data
file_path = "data_processed/ipg240102/processed_ipg240102_38.xml"  # Replace with your file path
parsed_data = parse_xml(file_path)
filtered_data = filter_patents(parsed_data)

# Save filtered patents to a CSV file for further processing
filtered_data.to_csv("filtered_patents.csv", index=False)
