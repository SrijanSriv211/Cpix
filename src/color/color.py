from src.shared.nltk_utils import clean_sentence
from src.shared.utils import flatten, similarity
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
        ids = list(set(flatten(enc.encode(query.lower()))))
        sites_idx = set()
        for id in ids:
            sites_idx.update(self.hash_map[str(id)])

        return self.rank(query, [self.index[i] for i in list(set(sites_idx))])

    def rank(self, query, results):
        raw_query = query.lower()
        cleaned_query = clean_sentence(raw_query)
        query_tokens = cleaned_query.split()
        ranked_results = []

        for result in results:
            raw_title = result["Title"].lower()
            cleaned_title = clean_sentence(raw_title)
            title_tokens = cleaned_title.split()

            # base score: token overlap between query and title
            token_matches = sum(1 for token in query_tokens if token in title_tokens)

            # calculate percentage of query tokens found in title
            query_coverage = token_matches / len(query_tokens) if query_tokens else 0

            # consider the length ratio between raw and cleaned text
            # this rewards titles with higher information density (less stop words)
            query_density = len(cleaned_query) / len(raw_query) if raw_query else 0
            title_density = len(cleaned_title) / len(raw_title) if raw_title else 0
            density_similarity = similarity(query_density, title_density)

            # find the relative positions of matching terms
            # (rewards titles where matching terms appear earlier)
            position_score = 0
            if token_matches > 0:
                for i, token in enumerate(title_tokens):
                    # earlier positions get higher scores
                    if token in query_tokens:
                        position_score += 1 / (i + 1)

            # combined score with weights
            score = (
                query_coverage * 5.0 +     # most important: how much of the query matches
                density_similarity * 2.0 +  # somewhat important: similar text structure
                position_score * 1.5        # somewhat important: matching terms appear early
            )

            # optional: boost exact title matches
            if cleaned_query == cleaned_title:
                score *= 2

            # url as tiebreaker (shorter URLs often indicate more relevant pages)
            url_length = len(result["URL"])
            url_score = 1 / (url_length / 100 + 1)  # normalize URL length effect

            # add URL score as small tiebreaker
            final_score = score + (url_score * 0.2)
            ranked_results.append((result, final_score))

        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in ranked_results]
