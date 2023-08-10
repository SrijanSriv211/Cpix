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
lemmatizer = WordNetLemmatizer()
model = SentenceTransformer("distilbert-base-nli-mean-tokens")

def tokenize(sentence):
    return nltk.word_tokenize(sentence.strip())

def stem(word):
    return stemmer.stem(word.lower().strip())

def lemmatize(word):
    return lemmatizer.lemmatize(word.lower().strip())

def stop_words(tokens):
    ignore_words = '''!()-[]{\};:'"\,<>./?@#$%^&*_~+'''
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

# Code refrence from: https://stackoverflow.com/a/65201576/18121288
def text_similarity(sent, sentences):
    """Calculates the similarity between the given sentence and a list of titles.

    Args:
        sentence (str): The sentence to be compared.
        sentences (list): A list of sentences to be compared with.

    Returns:
        list: A list of dictionaries, each containing the sentences index, and similarity score.
    """

    toks = tokenize(sent.lower())
    tokenize_sentences = [tokenize(sent.lower()) for sent in sentences]

    clean_toks = stop_words(toks)
    clean_tokenize_sentences = [stop_words(tok) for tok in tokenize_sentences]

    clean_sentence = " ".join([lemmatize(word) for word in clean_toks])
    clean_sentences = [
        (idx, " ".join([lemmatize(word) for word in toks]))
        for idx, toks in enumerate(clean_tokenize_sentences)
    ]

    unique_strings = set()
    unique_clean_sentences = list(filter(lambda x: x[1] not in unique_strings and not unique_strings.add(x[1]), clean_sentences))


    # lis_of_sents = [i["title"] for i in dict_of_sents]

    # tokens = tokenize(sentence.lower())
    # lis_of_toks = [tokenize(sent.lower()) for sent in lis_of_sents]

    # clean_toks = stop_words(tokens)
    # clean_lis_of_toks = [stop_words(tok) for tok in lis_of_toks]

    # clean_sent1 = [lemmatize(word) for word in clean_toks]
    # clean_sent2 = [[lemmatize(word) for word in toks] for toks in clean_lis_of_toks]

    # # Save only those websites which share keywords with the input sentence.
    # num_of_sites_to_be_ranked = 10
    # pre_ranked_sites = [
    #     {
    #         "match_name": " ".join(sent),
    #         "match_index": idx,
    #         "match_url": dict_of_sents[idx]["url"],
    #         "match_score": len(set(clean_sent1) & set(sent))
    #     }
    #     for idx, sent in enumerate(clean_sent2)
    #     if len(set(clean_sent1) & set(sent)) > 0
    # ]

    # sorted_pre_ranked_sites = sorted(pre_ranked_sites, key=lambda x: x["match_score"], reverse=True)
    # limited_sorted_pre_ranked_sites = [i["match_name"] for i in sorted_pre_ranked_sites][:num_of_sites_to_be_ranked]

    # sentences = []
    # sentences.append(" ".join(clean_sent1))
    # sentences.extend(limited_sorted_pre_ranked_sites)

    # sentence_embeddings = model.encode(sentences)

    # cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    # b = torch.from_numpy(sentence_embeddings)

    # duplicates = []
    # similarities = []
    # for idx, ele in enumerate(sorted_pre_ranked_sites[:num_of_sites_to_be_ranked]):
    #     URL = ele["match_url"]
    #     if URL in duplicates:
    #         continue

    #     similarities.append({
    #         "title": dict_of_sents[ele["match_index"]]["title"],
    #         "url": dict_of_sents[ele["match_index"]]["url"],
    #         "score": cos(b[0], b[idx+1]).item(),
    #     })

    #     duplicates.append(URL)

    # sorted_similarities = sorted(similarities, key=lambda x: x["score"], reverse=True)
    # return sorted_similarities
