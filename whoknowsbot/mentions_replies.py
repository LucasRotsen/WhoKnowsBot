from datetime import datetime

from twitter import error

from configuration.bot_config import verbose
from resources.replies import *
from utils import file_utility
from utils.image_utility import get_wordcloud, save_wordcloud_image


def reply(api, data, mention, operation):
    if operation == "QUANTOSSABEM":
        reply_mention_how_many(api, data, mention)

    elif operation == "QUEMSABE":
        reply_mention_who_know(api, data, mention)

    elif operation == "TERMOSMAISUSADOS":
        reply_mention_most_used_terms(api, data, mention)

    else:
        reply_invalid_tweet(api, mention)


def reply_mention_how_many(api, data, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    term = data["term"]
    users_amount = data["friends_with_knowledge"]
    knowledge = data["proportion_of_knowledge"]
    specialization = data["level_of_specialization"]

    knowledge_str = str(int(knowledge * 100))
    specialization_str = ("%.3f" % specialization)

    if users_amount == 0:
        reply_how_many = get_negative_how_many_reply(term, user)

    else:
        reply_how_many = get_positive_how_many_reply(knowledge_str, specialization_str, term, user)

    # Post the reply on Twitter
    try:
        print("Respondendo usuário...") if verbose else None

        api.PostUpdate(status=reply_how_many, in_reply_to_status_id=mention_id, auto_populate_reply_metadata=True)

        print("Resposta enviada. \n") if verbose else None

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_who_know(api, data, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    term = data["term"]

    if "suitable_follower_screen_name" in data:
        reply_who_know = get_positive_who_knows_reply(data, term, user)

    else:
        reply_who_know = get_negative_who_knows_reply(term, user)

    # Post the reply on Twitter
    try:
        print("Respondendo usuário...") if verbose else None

        api.PostUpdate(status=reply_who_know, in_reply_to_status_id=mention_id, auto_populate_reply_metadata=True)

        print("Resposta enviada. \n") if verbose else None

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_most_used_terms(api, data, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    words_frequency = data["word_frequency"]

    wordcloud = get_wordcloud(words_frequency)
    image_path = save_wordcloud_image(str(mention_id), "temp/", wordcloud)

    reply_most_used_terms = get_most_used_terms_reply(user)

    try:
        print("Respondendo usuário...") if verbose else None

        api.PostUpdate(status=reply_most_used_terms, media=image_path,
                       in_reply_to_status_id=mention_id, auto_populate_reply_metadata=True)

        print("Resposta enviada. \n") if verbose else None

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)

    file_utility.delete_file(image_path)


def reply_invalid_tweet(api, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    reply_invalid = get_invalid_tweet_reply(user)

    # Post the reply on Twitter
    try:
        print("Respondendo usuário...") if verbose else None

        api.PostUpdate(status=reply_invalid, in_reply_to_status_id=mention_id, auto_populate_reply_metadata=True)

        print("Resposta enviada. \n") if verbose else None

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)
