from src.shared.nltk_utils import clean_sentence
from src.shared.utils import flatten
from src.llm.encoder import Encoder
from collections import defaultdict
import json

enc = Encoder()
enc.load("models\\enc.bin")

def load_crawled_websites(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inverse_indexing(data):
    local_hash_map = []
    hash_map = defaultdict(list)

    for i, x in enumerate(data):
        cleaned_sentence = clean_sentence(x["Title"].lower())
        ids = list(set(flatten(enc.encode(cleaned_sentence))))
        idx = [i] * len(ids)

        local_hash_map.append(dict(zip(ids, idx)))

    # loop through each dictionary and append values to the respective keys
    for d in local_hash_map:
        for key, value in d.items():
            hash_map[key].append(value)
            hash_map[key] = list(set(hash_map[key]))

    # convert defaultdict to a normal dictionary
    return dict(hash_map)

def save_hash_map(hash_map, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hash_map, f, ensure_ascii=False, indent=4)

save_hash_map(inverse_indexing(load_crawled_websites("data\\index.json")), "data\\index_hash_map.json")
