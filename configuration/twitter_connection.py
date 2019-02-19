import twitter
from twitter import error

consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = ''


def open_connection():
    if are_keys_valid():
        try:
            api = twitter.Api(consumer_key=consumerKey,
                              consumer_secret=consumerSecret,
                              access_token_key=accessToken,
                              access_token_secret=accessTokenSecret,
                              sleep_on_rate_limit=True)

            return api

        except error.TwitterError as e:
            print("Erro ao se conectar: " + str(e.message))
            return None

    else:
        raise ValueError('Todos as chaves devem ser corretamente preenchidas antes de executar algoritmo.')


def are_keys_valid() -> bool:
    are_valid = True

    if consumerKey == '' or consumerSecret == '' or accessToken == '' or accessTokenSecret == '':
        are_valid = False

    return are_valid
