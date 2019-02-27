import re
from unicodedata import normalize

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from configuration.bot_config import should_count_mentions
from resources.text.custom_stopwords import custom_stopwords, custom_stopwords_pt


def accent_remover(text: str):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').upper()


def get_filtered_words(culture, phrases):
    # nltk asks to download this resources on the first execution.
    check_and_download_nltk_resources()

    # set the culture from which the stop words will be recovered.
    stop_words = set(stopwords.words(culture))

    # extend the lib's stopwords with the ones specified on 'custom_stopwords' file.
    stop_words.update(get_custom_stopwords(culture))

    words = []

    for phrase in phrases:
        mentions = re.findall(r'\w*@\w*', phrase)
        phrase_without_mentions = re.sub(r'\w*@\w*', '', phrase)

        tokens = word_tokenize(phrase_without_mentions, language=culture)

        # remove numbers and special characters from the list.
        filtered_tokens = [token.lower() for token in tokens if token.isalpha()]

        # remove stop words, such as articles and prepositions, from the list.
        filtered_tokens = [token.lower() for token in filtered_tokens if token not in stop_words and len(token) > 1]

        words.extend(filtered_tokens)

        if should_count_mentions:
            words.extend(mentions)

    return words


def get_word_frequency(words):
    return dict((i, words.count(i)) for i in words)


def get_custom_stopwords(culture):
    temp_custom_stopwords = custom_stopwords()

    if culture == "portuguese":
        temp_custom_stopwords += custom_stopwords_pt()

    return temp_custom_stopwords


def check_and_download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')

    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
