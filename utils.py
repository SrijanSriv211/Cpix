from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy, nltk

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
