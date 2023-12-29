from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import json, nltk, re

stemmer = PorterStemmer()
Lemmatizer = WordNetLemmatizer()

class Color:
    def __init__(self):
        self.data = None
        self.lemmatize_titles = None
        self.no_duplicate_urls = None

    def search(self, text):
        results = self.word_matching(self.clean_sentence(text), self.clean_site_data)
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

        tokenize_titles = [(idx, self.tokenize(sent.lower()), self.tokenize(url.replace("https", "").replace("http", "").lower())) for idx, sent, url in titles]
        clean_titles = [(idx, self.stop_words(title_toks), self.stop_words(url_toks)) for idx, title_toks, url_toks in tokenize_titles]
        self.clean_site_data = [
            (
                idx,
                " ".join([self.lemmatize(word) for word in title_toks]) + " " + " ".join([self.lemmatize(word) for word in url_toks])
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

    def clean_sentence(self, text):
        toks = self.tokenize(text.lower())
        clean_toks = self.stop_words(toks)
        return " ".join([self.lemmatize(word) for word in clean_toks])

    def tokenize(self, sentence):
        return nltk.word_tokenize(sentence.strip())

    def stem(self, word):
        return stemmer.stem(word.lower().strip())

    def lemmatize(self, word):
        return Lemmatizer.lemmatize(word.lower().strip())

    def stop_words(self, tokens):
        ignore_words = '''|!()-[]{};:'"\,<>./?@#$%^&*_~+·'''
        filler_words = set(stopwords.words("english"))
        # https://stackoverflow.com/a/58356570/18121288
        emoj = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            "]+", re.UNICODE
        )

        # https://stackoverflow.com/a/47301893/18121288
        removetable = str.maketrans(dict.fromkeys(ignore_words, ' ')) # Create a translation table to replace ignore_words with whitespaces
        all_toks = [tok.translate(removetable) for tok in tokens]
        remove_emoji = [re.sub(emoj, '', i) for i in all_toks]
        clean_toks = list(filter(None, remove_emoji))
        all_words = [self.stem(word) for word in clean_toks]
        remove_filler_words = [word for word in all_words if word not in filler_words]
        return (" ".join(remove_filler_words)).split()
