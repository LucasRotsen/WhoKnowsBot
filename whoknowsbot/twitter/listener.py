import re
import time
from datetime import datetime

from utils import file_utility, twitter_utility
from whoknowsbot.core import how_many_knows, most_used_terms, who_knows
from whoknowsbot.twitter.reply import reply


def listener(api):
    while True:
        time_before_processing = datetime.now()

        search_limit = file_utility.read('resources/search_limit.txt')
        new_mentions = twitter_utility.get_mentions(api, search_limit)

        # reversed is used to dispatch mentions in the order they are tweeted.
        for mention in reversed(new_mentions):
            tweet_text = mention.text
            tweet_text_redundant_spaces_removed = re.sub(' +', ' ', tweet_text)
            tweet_text_splitted = tweet_text_redundant_spaces_removed.split(
                " ")

            term = "twitter"
            operation = None

            if len(tweet_text_splitted) >= 3:
                term = tweet_text_splitted[2]

            if len(tweet_text_splitted) >= 2:
                operation = tweet_text_splitted[1].upper()

            user_id = mention.user.id
            user_name = mention.user.screen_name

            dispatcher(api, mention, operation, term, user_id, user_name)

            # update value of last processed mention
            file_utility.write('resources/search_limit.txt', mention.id)

        time_after_processing = datetime.now()
        processing_duration = (time_after_processing -
                               time_before_processing).total_seconds()
        None if processing_duration > 60 else time.sleep(
            60 - processing_duration)


def dispatcher(api, mention, operation, term, user_id, user_name):
    data = None

    if operation == "QUANTOSSABEM":
        data = how_many_knows(api, term, user_id, user_name)

    elif operation == "QUEMSABE":
        data = who_knows(api, term, user_id, user_name)

    elif operation == "SOBREOQUESABEM":
        data = most_used_terms(api, user_id, user_name)

    else:
        operation = None

    reply(api, data, mention, operation)
