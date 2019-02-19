import time
from datetime import datetime

from configuration.bot_config import development
from utils import file_utility, twitter_utility
from whoknowsbot.bot_core import how_many_knows, who_knows
from whoknowsbot.mentions_replies import reply


def listener(api):
    while True:
        try:
            time_before_processing = datetime.now()

            search_limit = file_utility.read('resources/search_limit.txt')
            new_mentions = twitter_utility.get_mentions(api, search_limit)

            for mention in new_mentions:
                tweet_text = mention.text
                tweet_text_splitted = tweet_text.split(" ")

                if len(mention.hashtags) > 0:
                    term = mention.hashtags[0].text
                    user_id = mention.user.id
                    user_name = mention.user.screen_name

                    operation = tweet_text_splitted[1].upper()

                    if operation == "QUANTOSSABEM":
                        data = how_many_knows(api, term, user_id, user_name)

                        if not development:
                            reply(api, data, mention, operation)

                    elif operation == "QUEMSABE":
                        data = who_knows(api, term, user_id, user_name)

                        if not development:
                            reply(api, data, mention, operation)

            time_after_processing = datetime.now()
            processing_duration = (time_after_processing - time_before_processing).total_seconds()
            {} if processing_duration > 60 else time.sleep(60 - processing_duration)

        # If something happens with the network, sleep for 1 minute and restart bot.
        except ConnectionError as e:
            message = str(datetime.now()) + " - " + "Listener" + ": " + e.args[0].args[0] + "\n"
            file_utility.append('resources/errors_log.txt', message)

            time.sleep(60)
