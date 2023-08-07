from pprint import pprint
from utils import text_similarity
import json

print("STARTING:")
json_file = open("data\\index.json", "r", encoding="utf-8")
content = json.load(json_file)

site_metadata = []
for idx, ele in enumerate(content):
    site_metadata.append({
        "title": ele["Title"],
        "url": ele["URL"],
        "index": idx
    })

sentence = "Google's Quantum Computer Achieves Quantum Supremacy"

ranked_sites = text_similarity(sentence, site_metadata)
pprint(ranked_sites)
