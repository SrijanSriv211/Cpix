from sentence_transformers import SentenceTransformer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import torch.nn, numpy, nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('nps_chat')
nltk.download('stopwords')

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

def text_similarity(sentence, dict_of_sents):
    lis_of_sents = [i["title"] for i in dict_of_sents]

    tokens = tokenize(sentence.lower())
    lis_of_toks = [tokenize(sent.lower()) for sent in lis_of_sents]

    clean_toks = stop_words(tokens)
    clean_lis_of_toks = [stop_words(tok) for tok in lis_of_toks]

    clean_sent1 = [lemmatize(word) for word in clean_toks]
    clean_sent2 = [[lemmatize(word) for word in toks] for toks in clean_lis_of_toks]

    # Save only those websites which share keywords with the input sentence.
    num_of_sites_to_be_ranked = 10
    pre_ranked_sites = [
        {
            "match_name": " ".join(sent),
            "match_index": idx,
            "match_score": len(set(clean_sent1) & set(sent))
        }
        for idx, sent in enumerate(clean_sent2)
        if len(set(clean_sent1) & set(sent)) > 0
    ]

    sorted_pre_ranked_sites = sorted(pre_ranked_sites, key=lambda x: x["match_score"], reverse=True)
    limited_sorted_pre_ranked_sites = [i["match_name"] for i in sorted_pre_ranked_sites][:num_of_sites_to_be_ranked]

    sentences = []
    sentences.append(" ".join(clean_sent1))
    sentences.extend(limited_sorted_pre_ranked_sites)

    # Code refrence from: https://stackoverflow.com/a/65201576/18121288
    model = SentenceTransformer("distilbert-base-nli-mean-tokens")
    sentence_embeddings = model.encode(sentences)

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    b = torch.from_numpy(sentence_embeddings)

    duplicates = []
    similarities = []
    for idx, ele in enumerate(sorted_pre_ranked_sites[:num_of_sites_to_be_ranked]):
        title = ele["match_name"]
        if title in duplicates:
            continue

        similarities.append({
            "title": dict_of_sents[ele["match_index"]]["title"],
            "url": dict_of_sents[ele["match_index"]]["url"],
            "score": cos(b[0], b[idx+1]).item(),
        })

        duplicates.append(title)

    sorted_similarities = sorted(similarities, key=lambda x: x["score"], reverse=True)
    return sorted_similarities
