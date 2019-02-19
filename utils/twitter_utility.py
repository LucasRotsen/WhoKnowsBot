import random
import time
from datetime import datetime, timedelta
from time import strptime

from twitter import error

from configuration.bot_config import development, verbose
from utils import file_utility, text_utility, time_utility


def get_mentions(api, search_limit: int):
    mentions_collection = []
    max_id = 9000000000000000000
    since_id = int(search_limit)

    while True:
        try:
            # Get the most recent mentions for the authenticating user
            mentions = api.GetMentions(since_id=since_id, max_id=max_id, count=200)

        except error.TwitterError as e:
            message = str(datetime.now()) + " - " + "Getting mentions on 'TwitterUtility'" + ": " + e.message[1] + "\n"
            file_utility.append('resources/errors_log.txt', message)
            continue

        # Print user and text of mentions collected
        for mention in mentions:
            mentions_collection.append(mention)

        if len(mentions) == 0:
            break

        else:
            max_id = mentions_collection[len(mentions) - 1].id - 1

    # Update value from since_id
    if len(mentions_collection) > 0:
        if not development:
            file_utility.write('resources/search_limit.txt', mentions_collection[0].id)

        if verbose:
            print(str(len(mentions_collection)) + " menções coletadas. Limite de consulta atualizado.")

    elif verbose:
        print("Não há novas menções.")

    # Return mentions collected
    return mentions_collection


def get_oldest_tweet_timestamp(users_used_term):
    lowest = 9999999999999

    for user in users_used_term:
        for tweet in users_used_term[user]:
            timestamp = time_utility.convert_to_timestamp(tweet.created_at)

            if timestamp < lowest:
                lowest = timestamp

    # Return the lowest timestamp among all posts analysed
    return lowest


def get_user_base(api, user_id, collect_from):
    # Get user base according type of analysis
    user_base = None
    if collect_from == "friends":
        user_base = api.GetFriendIDs(user_id=user_id)
    elif collect_from == "followers":
        user_base = api.GetFollowerIDs(user_id=user_id)

    # Get posts no more than 100 people
    if len(user_base) > 100:
        user_base = random.sample(user_base, 100)

    return user_base


def get_user_name(api, user_id: str) -> str:
    try:
        user = api.GetUser(user_id=user_id)
        return user.screen_name

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "Getting user name on 'TwitterUtility'" + ": " + e.message[1] + "\n"
        file_utility.append('resources/errors_log.txt', message)


def get_user_id(api, user_name: str) -> str:
    try:
        user = api.GetUser(screen_name=user_name)
        return user.id

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "Getting user id on 'TwitterUtility'" + ": " + e.message[1] + "\n"
        file_utility.append('resources/errors_log.txt', message)


def get_users_posts_term(api, user_base, term):
    dic_users_used_term = {}

    # Get the date from 7 days ago
    limit_date = datetime.strptime(str(datetime.now()),
                                   '%Y-%m-%d %H:%M:%S.%f') - timedelta(days=7)

    for user in user_base:
        tweets = []
        max_id = 9000000000000000000
        current_time_line = []
        num_tweets = 0

        while True:
            time.sleep(1)
            try:
                current_time_line = api.GetUserTimeline(count=200, user_id=user, max_id=max_id,
                                                        exclude_replies=False, include_rts=True)
            except error.TwitterError as e:
                message = str(datetime.now()) + " - " + "GetUserTimeline" + ": " + e.message[1] + "\n"
                file_utility.append('resources/errors_log.txt', message)

            # For each post collected...
            for tweet in current_time_line:

                # If term exists into a tweet....
                if text_utility.accent_remover(tweet.text).count(text_utility.accent_remover(term)) > 0:

                    # Get when the tweet was created in format yyyy-mm-dd HH-MM-SS
                    created = tweet.created_at.split(" ")
                    tweet_date = created[5] + "-" + str(strptime(created[1], '%b').tm_mon) + "-" + created[2] + \
                                 " " + created[3]
                    tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')

                    # If post is recenter than limitDate...
                    if tweet_date > limit_date:
                        tweets.append(tweet)
                    else:
                        break

            num_tweets += len(current_time_line)
            # Stop the reading if the user time line finish
            if len(current_time_line) == 0:
                break
            else:
                # Get when a post was created in format YYYY-mm-dd HH-MM-SS
                created = current_time_line[len(current_time_line) - 1].created_at.split(" ")
                tweet_date = created[5] + "-" + str(strptime(created[1], '%b').tm_mon) + "-" + created[2] + \
                             " " + created[3]
                tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')

                # Define a new limit for search user time line
                if tweet_date < limit_date:
                    break
                else:
                    if len(current_time_line) > 0:
                        max_id = current_time_line[len(current_time_line) - 1].id - 1

        dic_users_used_term[user] = [tweets, num_tweets]

    return dic_users_used_term
