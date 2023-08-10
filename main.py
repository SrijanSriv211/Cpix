from utils import text_similarity
from pprint import pprint
import json

titles = []
json_file = open("data\\index.json", "r", encoding="utf-8")

for idx, ele in enumerate(json.load(json_file)):
    titles.append(ele["Title"])

text = "how to reply to an insult"
results = text_similarity(text, titles)

print("SEARCH QUERY:", text)
pprint(results)
