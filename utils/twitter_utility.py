import random
import time
from datetime import datetime, timedelta
from time import strptime

import backoff
from requests import RequestException
from twitter import error

from configuration.bot_config import verbose
from utils import text_utility, time_utility
from utils.log_utility import log_error, log_retry


def get_mentions(api, search_limit: int):
    mentions_collection = []
    max_id = 9000000000000000000
    since_id = int(search_limit)

    while True:
        # Get the most recent mentions for the authenticating user
        mentions = retry_get_mentions(api, since_id, max_id)

        # Print user and text of mentions collected
        for mention in mentions:
            mentions_collection.append(mention)

        if len(mentions) == 0:
            break

        else:
            max_id = mentions_collection[len(mentions) - 1].id - 1

    if len(mentions_collection) > 0:
        print(str(len(mentions_collection)) + " menções coletadas.") if verbose else None

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
        user_base = retry_get_friend_ids(api, user_id)

    elif collect_from == "followers":
        user_base = retry_get_follower_ids(api, user_id)

    # Get posts no more than 100 people
    if len(user_base) > 100:
        user_base = random.sample(user_base, 100)

    return user_base


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
            time.sleep(60)

            try:
                current_time_line = api.GetUserTimeline(count=200, user_id=user, max_id=max_id,
                                                        exclude_replies=False, include_rts=True)
            except error.TwitterError as e:
                log_error(e.message, "get_users_posts_term")

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


def get_users_posts(api, user_base):
    dic_users_posts = {}

    # Get the date from 7 days ago
    limit_date = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f') - timedelta(days=7)

    for user in user_base:
        max_id = 9000000000000000000

        while True:
            tweets = retry_get_user_timeline(api, max_id, user)

            # For each post collected...
            for tweet in tweets:
                tweet_date = get_tweet_creation_date(tweet)

                # If post is newer than limitDate...
                if tweet_date > limit_date:
                    tweets.append(tweet)

                else:
                    break

            # Stop if timeline finishes or last tweet from timeline is older than the limit date.
            if len(tweets) == 0 or get_tweet_creation_date(tweets[len(tweets) - 1]) < limit_date:
                break

            max_id = tweets[len(tweets) - 1].id - 1

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


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_user_timeline(api, max_id, user):
    try:
        return api.GetUserTimeline(count=200, user_id=user, max_id=max_id, exclude_replies=False, include_rts=True)

    # When user account is private a 'Not Authorized' exception will occur, this cases will be skipped.
    except error.TwitterError:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_user_id(api, user_name):
    try:
        return api.GetUser(screen_name=user_name).id

    except error.TwitterError as e:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_user_name(api, user_id):
    try:
        return api.GetUser(user_id=user_id).screen_name

    except error.TwitterError as e:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_mentions(api, since_id, max_id):
    try:
        return api.GetMentions(since_id=since_id, max_id=max_id, count=200)

    except error.TwitterError:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_friend_ids(api, user_id):
    try:
        return api.GetFriendIDs(user_id=user_id)

    except error.TwitterError:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_get_follower_ids(api, user_id):
    try:
        return api.GetFollowerIDs(user_id=user_id)

    except error.TwitterError:
        pass


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retry_post_update(api, status, mention_id, media=None):
    try:
        api.PostUpdate(status=status, in_reply_to_status_id=mention_id, media=media, auto_populate_reply_metadata=True)

    except error.TwitterError:
        pass
