from unicodedata import normalize

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def accent_remover(text: str):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').upper()


def get_filtered_words(culture, phrases):
    # at first nltk request to download this libs.
    nltk.download('punkt')
    nltk.download('stopwords')

    # set the culture from which the stop words will be recovered.
    stop_words = set(stopwords.words(culture))
    stop_words.update(custom_stop_words())

    words = []

    for phrase in phrases:
        tokens = word_tokenize(phrase, language=culture)

        # remove numbers and special characters from the list.
        filtered_tokens = [token.lower() for token in tokens if token.isalpha()]

        # remove stop words, such as articles and prepositions, from the list.
        filtered_tokens = [token.lower() for token in filtered_tokens if token not in stop_words]

        words.extend(filtered_tokens)

    return words


def get_word_frequencies(words):
    return dict((i, words.count(i)) for i in words)


def custom_stop_words():
    return ((
        "rt",
        "https",
        "http"
    ))
