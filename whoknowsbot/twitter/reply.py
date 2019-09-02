from resources.text.replies import *
from utils.file_utility import delete_file
from utils.image_utility import get_wordcloud, save_wordcloud_image
from utils.log_utility import log_info
from utils.twitter_utility import retryable_post_update


def reply(api, data, mention, operation):
    log_info("Respondendo usuário...", "Reply")

    if operation == "QUANTOSSABEM":
        reply_mention_how_many(api, data, mention)

    elif operation == "QUEMSABE":
        reply_mention_who_know(api, data, mention)

    elif operation == "SOBREOQUESABEM":
        reply_mention_most_used_terms(api, data, mention)

    else:
        reply_invalid_tweet(api, mention)

    log_info("Resposta enviada.", "Reply")


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
        reply_how_many = get_positive_how_many_reply(
            knowledge_str, specialization_str, term, user)

    # Post the reply on Twitter
    retryable_post_update(api, reply_how_many, mention_id)


def reply_mention_who_know(api, data, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    term = data["term"]

    if "suitable_follower_screen_name" in data:
        reply_who_know = get_positive_who_knows_reply(
            str(data["suitable_follower_screen_name"]), term, user)

    else:
        reply_who_know = get_negative_who_knows_reply(term, user)

    # Post the reply on Twitter
    retryable_post_update(api, reply_who_know, mention_id)


def reply_mention_most_used_terms(api, data, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    words_frequency = data["word_frequency"]

    wordcloud = get_wordcloud(words_frequency)
    image_path = save_wordcloud_image(str(mention_id), "temp/", wordcloud)

    reply_most_used_terms = get_most_used_terms_reply(user)

    # Post the reply on Twitter
    retryable_post_update(api, reply_most_used_terms, mention_id, image_path)

    delete_file(image_path)


def reply_invalid_tweet(api, mention):
    mention_id = mention.id
    user = mention.user.screen_name

    reply_invalid = get_invalid_tweet_reply(user)

    # Post the reply on Twitter
    retryable_post_update(api, reply_invalid, mention_id)
