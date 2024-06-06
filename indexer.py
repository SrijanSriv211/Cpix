from src.utils import clean_sentence
import json

def load_crawled_websites(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inverse_indexing(data):
    hash_map = {}

    for i, x in enumerate(data):
        title = x["Title"]
        cleaned_sentence = clean_sentence(title)
        keywords = cleaned_sentence.split()

        for keyword in keywords:
            if keyword in hash_map:
                hash_map[keyword].append(i)
                hash_map[keyword] = list(set(hash_map[keyword]))

            else:
                hash_map[keyword] = [i]

    return hash_map

def save_hash_map(hash_map, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hash_map, f, ensure_ascii=False, indent=4)

save_hash_map(inverse_indexing(load_crawled_websites("data\\index.json")), "data\\index_hash_map.json")
