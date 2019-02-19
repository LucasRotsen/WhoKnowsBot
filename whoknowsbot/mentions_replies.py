from datetime import datetime

from twitter import error

from configuration.bot_config import verbose
from utils import file_utility


def reply(api, data, mention, operation):
    if operation == "QUANTOSSABEM":
        term = data["term"]
        friends_with_knowledge = data["friends_with_knowledge"]
        proportion_of_knowledge = data["proportion_of_knowledge"]
        level_of_specialization = data["level_of_specialization"]

        reply_mention_how_many(api, mention.id, term, mention.user.screen_name, friends_with_knowledge,
                               proportion_of_knowledge, level_of_specialization)

    elif operation == "QUEMSABE":
        term = data["term"]

        if len(data) == 3:
            # This is the case where the lowest timestamp is 9999999999999
            # In this scenario, there isn't a friend who knows about the term
            reply_mention_who_know(api, mention.id, term, mention.user.screen_name, None)

        else:
            suitable_follower_screen_name = data["suitable_follower_screen_name"]

            reply_mention_who_know(api, mention.id, term, mention.user.screen_name,
                                   suitable_follower_screen_name)


def reply_invalid_tweet(api, mention_id, user):
    reply_invalid = "@" + user + " Ops @" + user + ", verifique se você tweetou como o exemplo que eu coloquei aqui: " \
                                                   "https://twitter.com/WhoKnowsBot/status/1009919330006589440"

    # Post the reply on Twitter
    try:
        api.PostUpdate(status=reply_invalid, in_reply_to_status_id=mention_id)
    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_how_many(api, mention_id, term, user, users_amount, knowledge, specialization):
    knowledge_str = str(int(knowledge * 100))

    if users_amount == 0:
        reply_how_many = "@" + user + " Olá @" + user + ", infelizmente não encontrei ninguém entre quem você segue " \
                                                        "falando sobre #" + term + " :("

    else:
        specialization_str = ("%.3f" % specialization)
        reply_how_many = \
            "@" + user + " Olá @" + user + ", " + knowledge_str + "% das pessoas que você segue falam sobre #" + term + \
            ". O nível de especialização da sua rede é " + specialization_str + " em uma escala entre 0 e 1" \
            ". Diga-me, de 1 a 5, o quanto você concorda com esta resposta :) "

    # Post the reply on Twitter
    try:
        if verbose:
            print("Respondendo usuário...")

        api.PostUpdate(status=reply_how_many, in_reply_to_status_id=mention_id)

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_who_know(api, mention_id, term, user, suitable_user):
    if suitable_user is None:
        reply_who_know = "@" + user + " Olá @" + user + ", infelizmente não encontrei ninguém entre seus seguidores que " \
                                                        "sabe sobre #" + term + " :("
    else:
        reply_who_know = "@" + user + " Olá @" + user + ", entre seus seguidores quem mais sabe sobre #" + term + \
                         " é @" + str(suitable_user) + ". Diga-me, de 1 a 5, o quanto você concorda com esta resposta :)"

    # Post the reply on Twitter
    try:
        if verbose:
            print("Respondendo usuário...")

        api.PostUpdate(status=reply_who_know, in_reply_to_status_id=mention_id)

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)
