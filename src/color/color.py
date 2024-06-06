from src.utils import *
import json

class Color:
    def __init__(self, index_path, hash_map_path):
        self.index = []
        self.hash_map = {}

        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        with open(hash_map_path, "r", encoding="utf-8") as f:
            self.hash_map = json.load(f)

    def search(self, query):
        clean_query = clean_sentence(query)
        keywords = clean_query.split()

        index_of_websites = set()
        for keyword in keywords:
            index_of_websites.update(self.hash_map[keyword])

        list_of_websites = []
        for i in list(set(index_of_websites)):
            if self.index[i] in list_of_websites:
                continue

            list_of_websites.append(self.index[i])

        return list_of_websites
