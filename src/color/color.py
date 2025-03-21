from src.shared.nltk_utils import clean_sentence
from src.shared.utils import flatten
from src.llm.encoder import Encoder
import json

enc = Encoder()
enc.load("models\\enc.bin")

class Color:
    def __init__(self, index_path, hash_map_path):
        self.index = []
        self.hash_map = {}

        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        with open(hash_map_path, "r", encoding="utf-8") as f:
            self.hash_map = json.load(f)

    def search(self, query):
        cleaned_sentence = clean_sentence(query.lower())
        ids = list(set(flatten(enc.encode(cleaned_sentence))))
        sites_idx = set()
        for id in ids:
            sites_idx.update(self.hash_map[str(id)])

        # return [self.index[i] for i in list(set(sites_idx))]
        return [self.index[i] for i in sites_idx]
