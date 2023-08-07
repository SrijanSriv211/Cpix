from sentence_transformers import SentenceTransformer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import torch.nn, numpy, nltk

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('nps_chat')
# nltk.download('stopwords')

stemmer = PorterStemmer()
Lemmatizer = WordNetLemmatizer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence.strip())

def stem(word):
    return stemmer.stem(word.lower().strip())

def lemmatize(word):
    return Lemmatizer.lemmatize(word.lower().strip())

def stop_words(tokens):
    ignore_words = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    filler_words = set(stopwords.words("english"))
    all_words = [stem(words) for words in tokens if words not in ignore_words]
    return [word for word in all_words if word not in filler_words]

# Arrange words in such a way to form a logical sentence.
def arrange_words(tokens):
    """
    A number will represent the number of empty strings in a list.
    For example: 4 -> ["", "", "", ""].
    """

    processed_tokens = []
    for sublist in tokens:
        if isinstance(sublist[-1], int):
            empty_list = [""] * sublist[-1]
            processed_tokens.append(sublist[:-1] + empty_list)

        else:
            processed_tokens.append(sublist)

    # Construct a logical sentence.
    sentence = [numpy.random.choice(i).strip() for i in processed_tokens]
    return " ".join(sentence)

def text_similarity(sent1, sent2):
    # https://stackoverflow.com/a/65201576/18121288
    tok1 = tokenize(sent1.lower())
    tok2 = tokenize(sent2.lower())

    clean_tok1 = stop_words(tok1)
    clean_tok2 = stop_words(tok2)

    clean_sent1 = [lemmatize(word) for word in clean_tok1]
    clean_sent2 = [lemmatize(word) for word in clean_tok2]

    common = set(clean_sent1) & set(clean_sent2)
    similarity = len(common) / max(len(clean_sent1), len(clean_sent2))
    return similarity

    # sentences = [" ".join(clean_sent1), " ".join(clean_sent2)]

    # model = SentenceTransformer("distilbert-base-nli-mean-tokens")
    # sentence_embeddings = model.encode(sentences)

    # cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    # b = torch.from_numpy(sentence_embeddings)

    # similarity = cos(b[0], b[1])
    # return similarity
