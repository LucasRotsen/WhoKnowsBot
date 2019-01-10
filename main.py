import random
import time
from datetime import datetime

from requests import ConnectionError
from twitter import error

from configuration import twitter_connection
from utils import file_utility
from utils import time_utility
from utils import twitter_utility
from whoknowsbot.mentions_replies import MentionsReplies


class TwitterBot(object):
    def __init__(self):
        self.api = twitter_connection.open_connection()
        self.replies = MentionsReplies(self.api)

    def test(self):
        pass

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
                        if tweet_text_splitted[1].upper() == "QUANTOSSABEM":
                            self.how_many_knows(mention)

                        elif tweet_text_splitted[1].upper() == "QUEMSABE":
                            self.who_knows(mention)

                        else:
                            pass
                    else:
                        pass

                time_after_processing = datetime.now()
                processing_duration = (time_after_processing - time_before_processing).total_seconds()
                {} if processing_duration > 60 else time.sleep(60 - processing_duration)

            # If something happens with the network, sleep for 1 minute and restart bot.
            except ConnectionError as e:
                message = str(datetime.now()) + " - " + "Listener" + ": " + e.args[0].args[0] + "\n"
                file_utility.append('resources/errors_log.txt', message)

                time.sleep(60)

    def who_knows(self, mention):
        term = mention.hashtags[0].text
        user_name = mention.user.screen_name
        user_id = mention.user.id

        print("Analisando menção de: " + str(user_name) + " | QUEMSABE")

        followers = self.get_user_base(user_id, "followers")
        followers_used_term = twitter_utility.get_users_posts_term(self.api, followers, term)
        lowest_timestamp = twitter_utility.get_oldest_tweet_timestamp(followers_used_term)

        if lowest_timestamp == 9999999999999:
            self.replies.reply_mention_who_know(mention.id, term, mention.user.screen_name, None)

        else:
            current_timestamp = time_utility.get_current_timestamp()
            suitable_follower_score = 0
            suitable_follower_id = None

            for follower in followers_used_term:
                score = 0

                for tweet in followers_used_term[follower]:
                    if tweet.retweeted_status is not None:
                        score = score + 0.5

                    elif tweet.in_reply_to_user_id is not None:
                        score = score + 1.0

                    else:
                        score = score + 0.75

                    tweet_timestamp = time_utility.convert_to_timestamp(tweet.created_at)
                    score = score + (1 - (current_timestamp - tweet_timestamp) / (current_timestamp - lowest_timestamp))

                if score > suitable_follower_score:
                    suitable_follower_score = score
                    suitable_follower_id = follower

            suitable_follower_screen_name = twitter_utility.get_user_name(self.api, suitable_follower_id)
            self.replies.reply_mention_who_know(mention.id, term, mention.user.screen_name,
                                                suitable_follower_screen_name)

    def how_many_knows(self, mention):
        term = mention.hashtags[0].text
        user_name = mention.user.screen_name
        user_id = mention.user.id

        print("Analisando menção de: " + str(user_name) + " | QUANTOSSABEM")

        friends_with_knowledge = 0
        total_of_specialization = 0

        friends = self.get_user_base(user_id, "friends")
        friends_used_term = twitter_utility.get_users_posts_term(self.api, friends, term)

        for friend in friends_used_term:
            friend_actions_with_term = len(friends_used_term[friend])

            if friend_actions_with_term > 0:
                max_id = 9000000000000000000
                tweets = []

                try:
                    tweets = self.api.GetUserTimeline(count=200, user_id=friend, max_id=max_id,
                                                      exclude_replies=False, include_rts=True)
                except error.TwitterError as e:
                    message = str(datetime.now()) + " - " + "GetUserTimeline" + ": " + e.message[1] + "\n"
                    file_utility.append('resources/errors_log.txt', message)

                friends_with_knowledge += 1
                total_of_specialization += friend_actions_with_term / len(tweets)

        proportion_of_knowledge = friends_with_knowledge / len(friends)
        level_of_specialization = total_of_specialization / len(friends)

        self.replies.reply_mention_how_many(mention.id, term, mention.user.screen_name, friends_with_knowledge,
                                            proportion_of_knowledge, level_of_specialization)

    # TODO Analisar uso do método. Talvez não precise de um método só para isso.
    def get_user_base(self, user_id, collect_from):
        # Get user base according type of analysis
        user_base = None
        if collect_from == "friends":
            user_base = self.api.GetFriendIDs(user_id=user_id)
        elif collect_from == "followers":
            user_base = self.api.GetFollowerIDs(user_id=user_id)

        # Get posts no more than 100 people
        if len(user_base) > 100:
            user_base = random.sample(user_base, 100)

        return user_base

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
