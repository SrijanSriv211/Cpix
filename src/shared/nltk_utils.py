from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk, re

stemmer = PorterStemmer()
Lemmatizer = WordNetLemmatizer()

def clean_sentence(text):
    toks = tokenize(text.lower())
    clean_toks = stop_words(toks)
    return " ".join([lemmatize(word) for word in clean_toks])

def tokenize(sentence):
    return nltk.word_tokenize(sentence.strip())

def stem(word):
    return stemmer.stem(word.lower().strip())

def lemmatize(word):
    return Lemmatizer.lemmatize(word.lower().strip())

def stop_words(tokens):
    ignore_words = '''|!()-[]{};:'"\\,<>./?@#$%^&*_~+·'''
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
