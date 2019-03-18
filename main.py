import sys
from utils.file_utility import write
from utils.log_utility import log_info
from whoknowsbot.console.console import get_user_data_with_term
from whoknowsbot.twitter.listener import listener

from configuration import twitter_connection


def main():
    api = twitter_connection.open_connection()

    log_info("API configurada com sucesso.", "Main")

    if len(sys.argv) == 1:
        listener(api)

    elif len(sys.argv) == 3:
        user_name = sys.argv[1]
        term = sys.argv[2]
        data = get_user_data_with_term(api, user_name, term)
        write("result.txt", str(data))

    else:
        raise ValueError("Sintaxe esperada: $ python main.py [nome_do_usario] [termo].")


main()
