import sys

from configuration import twitter_connection
from configuration.bot_config import development, verbose
from whoknowsbot.console import get_user_data_with_term
from whoknowsbot.listener import listener


def main():
    api = twitter_connection.open_connection()

    if verbose:
        print("Conectado com sucesso.")

    if len(sys.argv) == 1:
        if development:
            print("Modo de desenvolvimento está ativado. Você pode alterar isso no arquivo: 'bot_config.py'. \n")

        listener(api)

    elif len(sys.argv) == 3:
        user_name = sys.argv[1]
        term = sys.argv[2]
        get_user_data_with_term(api, user_name, term)

    else:
        raise ValueError("Sintaxe esperada: $ python main.py [nome_do_usario] [termo].")


main()
