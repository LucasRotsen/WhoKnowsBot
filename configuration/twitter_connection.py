import twitter
from twitter import error

consumerKey = '1pTq010ZJiHFSkz7HCuqzXUpN'
consumerSecret = 'ePcw81En1Twu2AXCOg6iacbXDMNdckEE0yuikR8QHrll4T5Okg'
accessToken = '977978225870729216-XjrjD03txdtbRXYu9ZhB11W0pBHeiep'
accessTokenSecret = 'zCdrMT0GTEi2UmEylsBWj5JTYF0U9s0601yIfW7pUv2ig'


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
