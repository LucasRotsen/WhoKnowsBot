import sys

from configuration import twitter_connection
from utils.log_utility import log_info
from whoknowsbot.console.console import get_user_data_with_term
from whoknowsbot.twitter.listener import listener


def main():
    api = twitter_connection.open_connection()

    log_info("API configurada com sucesso.", "Main")

    if len(sys.argv) == 1:
        listener(api)

    elif len(sys.argv) == 3:
        user_name = sys.argv[1]
        term = sys.argv[2]
        get_user_data_with_term(api, user_name, term)

    else:
        raise ValueError("Sintaxe esperada: $ python main.py [nome_do_usario] [termo].")


main()
