from configuration.bot_config import verbose
from datetime import datetime
from twitter import error

from utils import file_utility


def reply_invalid_tweet(api, mention_id, user):
    reply = "@" + user + " Ops @" + user + ", verifique se você tweetou como o exemplo que eu coloquei aqui: " \
                                           "https://twitter.com/WhoKnowsBot/status/1009919330006589440"

    # Post the reply on Twitter
    try:
        api.PostUpdate(status=reply, in_reply_to_status_id=mention_id)
    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_how_many(api, mention_id, term, user, users_amount, knowledge, specialization):
    reply = None
    knowledge_str = str(int(knowledge * 100))

    if users_amount == 0:
        reply = "@" + user + " Olá @" + user + ", infelizmente não encontrei ninguém entre quem você segue " \
                                               "falando sobre #" + term + " :("

    else:
        specialization_str = ("%.3f" % specialization)
        reply = \
            "@" + user + " Olá @" + user + ", " + knowledge_str + "% das pessoas que você segue falam sobre #" + term + \
            ". O nível de especialização da sua rede é " + specialization_str + " em uma escala entre 0 e 1" \
            ". Diga-me, de 1 a 5, o quanto você concorda com esta resposta :) "

    # Post the reply on Twitter
    try:
        if verbose:
            print("Respondendo usuário...")

        api.PostUpdate(status=reply, in_reply_to_status_id=mention_id)

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)


def reply_mention_who_know(api, mention_id, term, user, suitable_user):
    if suitable_user is None:
        reply = "@" + user + " Olá @" + user + ", infelizmente não encontrei ninguém entre seus seguidores que " \
                                               "sabe sobre #" + term + " :("
    else:
        reply = "@" + user + " Olá @" + user + ", entre seus seguidores quem mais sabe sobre #" + term + \
                " é @" + str(suitable_user) + ". Diga-me, de 1 a 5, o quanto você concorda com esta resposta :)"

    # Post the reply on Twitter
    try:
        if verbose:
            print("Respondendo usuário...")

        api.PostUpdate(status=reply, in_reply_to_status_id=mention_id)

    except error.TwitterError as e:
        message = str(datetime.now()) + " - " + "PostUpdate" + ": " + e.message + "\n"
        file_utility.append('resources/error_log.txt', message)
