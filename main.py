from utils import text_similarity
import json

from pprint import pprint

print("STARTING:")
json_file = open("data\\index.json", "r", encoding="utf-8")
content = json.load(json_file)

title_metadata = []
for idx, ele in enumerate(content):
    title_metadata.append({
        "title": ele["Title"].lower(),
        "index": idx
    })

sentence = "Long Walk to Freedom Chapter Explanation"
pprint(text_similarity(sentence, title_metadata))

#     data = {
#         "title": "",
#         "url": "",
#         "score": 0
#     }

#     score = text_similarity(sentence1, i["Title"])
#     if score < 0.6:
#         continue

#     data["title"] = i["Title"]
#     data["url"] = i["URL"]
#     data["score"] = score
#     results.append(data)


# sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
# pprint(sorted_results[:20])
