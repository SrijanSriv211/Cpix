from utils import text_similarity
import json

from pprint import pprint

sentence1 = "class 10 english chapter 1 lecture"

json_file = open("data\\index.json", "r", encoding="utf-8")
content = json.load(json_file)

results = []
for i in content:
    data = {
        "title": "",
        "url": "",
        "score": 0
    }

    score = text_similarity(sentence1, i["Title"])
    if score < 0.6:
        continue

    data["title"] = i["Title"]
    data["url"] = i["URL"]
    data["score"] = score
    results.append(data)


sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
pprint(sorted_results[:20])
