import pandas as pd
import re
import json

file_path = "../tsv_files/g_cpc_title.tsv" 
data = pd.read_csv(file_path, sep="\t")

print(data.head())

green_terms = [
    # Core concepts
    r'sustainable', r'renewable', r'energy', r'climate',
    r'carbon', r'biofuel', r'environment', r'wind', r'solar',

    # Environmental concerns
    r'pollution', r'emissions', r'waste', r'recycling',
    r'conservation', r'deforestation', r'biodiversity',
    r'sustainability', r'eco-friendly', r'greenhouse gas',

    # Green technologies
    r'clean energy', r'solar power', r'wind power',
    r'hydropower', r'geothermal energy', r'biomass',
    r'electric vehicle', r'EV', r'hybrid', r'zero-emission',

    # Sustainable practices
    r'organic', r'fair trade', r'local', r'sustainable farming',
    r'permaculture', r'green building', r'LEED', r'energy efficiency',

    # Climate change
    r'global warming', r'climate change', r'sea level rise',
    r'extreme weather', r'climate action', r'mitigation',
    r'adaptation', r'Paris Agreement', r'COP21', r'IPCC',

    # Social and economic aspects
    r'green jobs', r'circular economy', r'sustainable development',
    r'ESG', r'corporate social responsibility', r'social impact',
    r'ethical consumption', r'eco-conscious', r'green consumerism',

    # Additional terms
    r'nature', r'wildlife', r'ecosystem', r'forest', r'ocean',
    r'conservation', r'preservation', r'restoration', r'resilience',
    r'low-carbon', r'net-zero', r'carbon neutral', r'carbon footprint',
    r'green technology', r'cleantech', r'sustainable living', r'eco-friendly',
    r'greenwashing', r'sustainability reporting', r'climate finance',
    r'renewable energy sources', r'green infrastructure', r'urban sustainability',
    r'sustainable tourism', r'eco-tourism', r'green business', r'sustainable business'
] ## ! Estimated from state of art consepts it can be improved and expanded.

def is_green(title):
    return any(re.search(term, title, re.IGNORECASE) for term in green_terms)

columns_all_data = list(data.columns)
for title in columns_all_data:
    print(str(title))
    data[str(title)] = data[str(title)].astype(str).fillna("")
    data['is_green'] = data[str(title)].apply(is_green)

green_cpc_data = data[data['is_green']]
print("HERE!", green_cpc_data.head())
green_cpc_codes = green_cpc_data[str(columns_all_data[0])].tolist()
green_keywords = list()
for title in columns_all_data[1:]:
  print(title)
  set_new = set(
    word.lower() for desc in green_cpc_data[str(title)] for word in desc.split()
    if any(re.search(term, word, re.IGNORECASE) for term in green_terms)
    )
  green_keywords.extend(set_new)

print("keywords", green_keywords)

green_data_json = {
    "cpc_codes": green_cpc_codes,
    "keywords": green_keywords
}

output_path = "green_cpc_keywords.json"
with open(output_path, "w") as json_file:
    json.dump(green_data_json, json_file, indent=4)

print(f"Green CPC codes and keywords saved to {output_path}")
