from utils import *
import json

class Color:
    def __init__(self):
        self.data = None
        lemmatize_titles = None
        self.no_duplicate_urls = None

    def search(self, text):
        results = self.word_matching(clean_sentence(text), self.clean_site_data)
        indexes = [i["index"] for i in results]

        return [self.data[i] for i in indexes]

    def load_websites(self, path):
        json_file = open(path, "r", encoding="utf-8")
        self.data = json.load(json_file)

        urls = [
            (idx, ele["URL"])
            for idx, ele in enumerate(self.data)
        ]

        unique_urls = set()
        self.no_duplicate_urls = list(filter(lambda x: x[1] not in unique_urls and not unique_urls.add(x[1]), urls))

    def preprocess(self):
        titles = [(i[0], self.data[i[0]]["Title"], i[1]) for i in self.no_duplicate_urls]

        tokenize_titles = [(idx, tokenize(sent.lower()), tokenize(url.replace("https", "").replace("http", "").lower())) for idx, sent, url in titles]
        clean_titles = [(idx, stop_words(title_toks), stop_words(url_toks)) for idx, title_toks, url_toks in tokenize_titles]
        self.clean_site_data = [
            (
                idx,
                " ".join([lemmatize(word) for word in title_toks]) + " " + " ".join([lemmatize(word) for word in url_toks])
            )
            for idx, title_toks, url_toks in clean_titles
        ]

    # sentence (str): The sentence to be compared.
    # sentences [list of tuples -> (index, sentence)]: A list of (index, sentences) to be compared with.
    # returns a list of dictionaries, each containing the sentences index, and matching score.
    def word_matching(self, sentence, sentences):
        matching_sentences = sorted(
            [
                (idx, sent, len(set(sentence.split()) & set(sent.split())))
                for idx, sent in sentences
                if len(set(sentence.split()) & set(sent.split())) > 0
            ],
            key=lambda x: x[2],
            reverse=True
        )[:20]

        similar_sentences = []
        for i in matching_sentences:
            similar_sentences.append({
                "index": i[0],
                "score": i[2],
            })

        return sorted(similar_sentences, key=lambda x: x["score"], reverse=True)
