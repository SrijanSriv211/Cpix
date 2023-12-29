from sentence_transformers import SentenceTransformer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import torch.nn, numpy, nltk, re

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('nps_chat')
# nltk.download('stopwords')

stemmer = PorterStemmer()
Lemmatizer = WordNetLemmatizer()
model = SentenceTransformer("distilbert-base-nli-mean-tokens")

def tokenize(sentence):
    return nltk.word_tokenize(sentence.strip())

def stem(word):
    return stemmer.stem(word.lower().strip())

def lemmatize(word):
    return Lemmatizer.lemmatize(word.lower().strip())

def stop_words(tokens):
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
    all_words = [stem(word) for word in clean_toks]
    remove_filler_words = [word for word in all_words if word not in filler_words]
    return (" ".join(remove_filler_words)).split()

# Code refrence from: https://stackoverflow.com/a/65201576/18121288
def text_similarity(sentence, sentences):
    """Calculates the similarity between the given sentence and a list of titles.

    Args:
        sentence (str): The sentence to be compared.
        sentences [list of tuples -> (index, sentence)]: A list of (index, sentences) to be compared with.

    Returns:
        list: A list of dictionaries, each containing the sentences index, and similarity score.
    """

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

    # sentences = []
    # sentences.append(sentence)
    # sentences.extend([i[1] for i in matching_sentences])

    # sentence_embeddings = model.encode(sentences)

    # cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    # b = torch.from_numpy(sentence_embeddings)

    # similar_sentences = []
    # for i, item in enumerate(matching_sentences):
    #     idx, _, _ = item
    #     score = cos(b[0], b[i+1]).item()
    #     if (score >= 0.6):
    #         similar_sentences.append({
    #             "index": idx,
    #             "score": score,
    #         })

    return sorted(similar_sentences, key=lambda x: x["score"], reverse=True)
