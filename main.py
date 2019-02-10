import time

from configuration.bot_config import verbose
from configuration import twitter_connection
from datetime import datetime
from requests import ConnectionError
from twitter import error
from utils import file_utility, twitter_utility

from whoknowsbot.mentions_replies import reply_mention_how_many, reply_mention_who_know
from whoknowsbot.bot_core import how_many_knows, who_knows


class TwitterBot(object):
    def __init__(self):
        self.api = twitter_connection.open_connection()

        if verbose:
            print("Conectado com sucesso.")

    def listener(self):
        while True:
            try:
                time_before_processing = datetime.now()

                search_limit = file_utility.read('resources/search_limit.txt')
                new_mentions = twitter_utility.get_mentions(self.api, search_limit)

                for mention in new_mentions:
                    tweet_text = mention.text
                    tweet_text_splitted = tweet_text.split(" ")

                    if len(mention.hashtags) > 0:
                        operation = tweet_text_splitted[1].upper()

                        if operation == "QUANTOSSABEM":
                            data = how_many_knows(self.api, mention)
                            # self.reply(data, mention, operation)

                        elif operation == "QUEMSABE":
                            data = who_knows(self.api, mention)
                            # self.reply(data, mention, operation)

                time_after_processing = datetime.now()
                processing_duration = (time_after_processing - time_before_processing).total_seconds()
                {} if processing_duration > 60 else time.sleep(60 - processing_duration)

            # If something happens with the network, sleep for 1 minute and restart bot.
            except ConnectionError as e:
                message = str(datetime.now()) + " - " + "Listener" + ": " + e.args[0].args[0] + "\n"
                file_utility.append('resources/errors_log.txt', message)

                time.sleep(60)

    def reply(self, data, mention, operation):
        if operation == "QUANTOSSABEM":
            term = data["term"]
            friends_with_knowledge = data["friends_with_knowledge"]
            proportion_of_knowledge = data["proportion_of_knowledge"]
            level_of_specialization = data["level_of_specialization"]

            reply_mention_how_many(self.api, mention.id, term, mention.user.screen_name, friends_with_knowledge,
                                   proportion_of_knowledge, level_of_specialization)

        elif operation == "QUEMSABE":
            term = data["term"]

            if len(data) == 3:
                # This is the case where the lowest timestamp is 9999999999999
                reply_mention_who_know(self.api, mention.id, term, mention.user.screen_name, None)

            else:
                suitable_follower_screen_name = data["suitable_follower_screen_name"]

                reply_mention_who_know(self.api, mention.id, term, mention.user.screen_name,
                                       suitable_follower_screen_name)

    # TODO-Eric modify algorithm to use this method
    def get_users_timeline(self, users):
        max_id = 9000000000000000000
        user_dict = {}

        for user in users:
            time.sleep(1)

            try:
                current_time_line = self.api.GetUserTimeline(count=200, user_id=user, max_id=max_id,
                                                             exclude_replies=False, include_rts=True)
                user_dict[user] = current_time_line
            except error.TwitterError as e:
                message = str(datetime.now()) + " - " + "GetUserTimeline" + ": " + e.message[1] + "\n"
                file_utility.append('resources/errors_log.txt', message)

        return user_dict


who_knows_bot = TwitterBot()
who_knows_bot.listener()
