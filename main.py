from utils import text_similarity, lemmatize, stop_words, tokenize
from pprint import pprint
import json, time

json_file = open("data\\index.json", "r", encoding="utf-8")
data = json.load(json_file)
def database():
    urls = [
        (idx, ele["URL"])
        for idx, ele in enumerate(data)
    ]

    unique_urls = set()
    no_duplicate_urls_list = list(filter(lambda x: x[1] not in unique_urls and not unique_urls.add(x[1]), urls))

    titles = [(i[0], data[i[0]]["Title"]) for i in no_duplicate_urls_list]

    tokenize_titles = [(idx, tokenize(sent.lower())) for idx, sent in titles]
    clean_titles = [(idx, stop_words(tok)) for idx, tok in tokenize_titles]

    lemmatize_titles = [
        (idx, " ".join([lemmatize(word) for word in toks]))
        for idx, toks in clean_titles
    ]

    return lemmatize_titles

def clean_sentence(text):
    toks = tokenize(text.lower())
    clean_toks = stop_words(toks)
    return " ".join([lemmatize(word) for word in clean_toks])

list_of_titles = database()
def color_rank(text):
    results = text_similarity(clean_sentence(text), list_of_titles)
    indexes = [i["index"] for i in results]

    return [data[i] for i in indexes]

if __name__ == "__main__":
    text = "onestate coding"

    start_time = time.time()
    results = color_rank(text)
    end_time = time.time()

    print("SEARCH QUERY:", text)
    pprint(results)
    print("About", (end_time - start_time), "seconds")
