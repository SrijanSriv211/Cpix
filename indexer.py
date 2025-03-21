from src.shared.utils import flatten
from src.llm.encoder import Encoder
from collections import defaultdict
import json

enc = Encoder()
enc.load("models\\enc.bin")

def load_crawled_websites(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_hash(sent, i):
    ids = list(set(flatten(enc.encode(sent.lower()))))
    idx = [i] * len(ids)
    return dict(zip(ids, idx))

def inverse_indexing(data):
    local_hash_map = []
    hash_map = defaultdict(list)

    for i, x in enumerate(data):
        local_hash_map.append(create_hash(x["Title"], i))
        local_hash_map.append(create_hash(x["URL"], i))

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
