import random
from datetime import timedelta
from time import strptime

from utils import text_utility, time_utility
from utils.retryable_utility import *


def get_mentions(api, search_limit: int):
    log_info("Recuperando menções...", "Get_Mentions")

    mentions_collection = []
    max_id = 9000000000000000000
    since_id = int(search_limit)

    while True:
        # Get the most recent mentions for the authenticating user
        mentions = retryable_get_mentions(api, since_id, max_id)

        # Print user and text of mentions collected
        for mention in mentions:
            mentions_collection.append(mention)

        if len(mentions) == 0:
            break

        else:
            max_id = mentions_collection[len(mentions) - 1].id - 1

    if len(mentions_collection) > 0:
        log_info("{quantidade} menções coletadas.".format(quantidade=str(len(mentions_collection))), "Get_Mentions")

    else:
        log_info("Não há novas menções.", "Get_Mentions")

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
    log_info("Recuperando base de '{source}' do usuário: {id}".format(source=collect_from, id=user_id), "Get_User_Base")

    # Get user base according type of analysis
    user_base = None

    if collect_from == "friends":
        user_base = retryable_get_friend_ids(api, user_id)

    elif collect_from == "followers":
        user_base = retryable_get_follower_ids(api, user_id)

    # Get posts from no more than 100 people
    if len(user_base) > 100:
        user_base = random.sample(user_base, 100)

    log_info("Base recuperada.", "Get_User_Base")

    return user_base


def get_users_posts_term(api, user_base, term):
    dic_users_used_term = {}

    # Get the date from 7 days ago
    limit_date = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f') - timedelta(days=7)

    for user in user_base:
        log_info("Iniciando análise dos tweets do usuário: {id}".format(id=user), "Get_Users_Posts_Term")

        max_id = 9000000000000000000
        num_tweets = 0
        tweets = []

        while True:
            user_timeline = retryable_get_user_timeline(api, max_id, user)

            # For each post collected...
            for tweet in user_timeline:
                term_without_accents = text_utility.accent_remover(term)
                tweet_without_accents = text_utility.accent_remover(tweet.text)
                tweet_contains_term = tweet_without_accents.count(term_without_accents) > 0
                tweet_date = get_tweet_creation_date(tweet)

                # If post is newer than limitDate and tweet contains the term.
                if tweet_date > limit_date and tweet_contains_term:
                    tweets.append(tweet)

                else:
                    break

            num_tweets += len(user_timeline)

            # Stop if timeline finishes or the last tweet from timeline is older than the limit date.
            if len(user_timeline) == 0 or get_tweet_creation_date(user_timeline[len(user_timeline) - 1]) < limit_date:
                log_info("Fim da análise dos tweets do usuário: {id}".format(id=user), "Get_Users_Posts")
                break

            max_id = user_timeline[len(user_timeline) - 1].id - 1

        dic_users_used_term[user] = [tweets, num_tweets]

    return dic_users_used_term


def get_users_posts(api, user_base):
    dic_users_posts = {}

    # Get the date from 7 days ago
    limit_date = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f') - timedelta(days=7)

    for user in user_base:
        log_info("Iniciando análise dos tweets do usuário: {id}".format(id=user), "Get_Users_Posts")

        max_id = 9000000000000000000
        tweets = []

        while True:
            user_timeline = retryable_get_user_timeline(api, max_id, user)

            # For each post collected...
            for tweet in user_timeline:
                tweet_date = get_tweet_creation_date(tweet)

                # If post is newer than limitDate we append it otherwise we stop analysing this user's tweets.
                if tweet_date > limit_date:
                    tweets.append(tweet)

                else:
                    break

            # Stop if timeline finishes or the last tweet from timeline is older than the limit date.
            if len(user_timeline) == 0 or get_tweet_creation_date(user_timeline[len(user_timeline) - 1]) < limit_date:
                log_info("Fim da análise dos tweets do usuário: {id}".format(id=user), "Get_Users_Posts")
                break

            max_id = user_timeline[len(user_timeline) - 1].id - 1

        dic_users_posts[user] = tweets

    return dic_users_posts


def get_tweet_creation_date(tweet):
    creation_date = tweet.created_at.split(" ")

    year = creation_date[5]
    month = str(strptime(creation_date[1], '%b').tm_mon)
    day = creation_date[2]
    hour = creation_date[3]

    creation_date_formatted = "{Y}-{m}-{d} {hour}".format(Y=year, m=month, d=day, hour=hour)

    return datetime.strptime(creation_date_formatted, '%Y-%m-%d %H:%M:%S')

