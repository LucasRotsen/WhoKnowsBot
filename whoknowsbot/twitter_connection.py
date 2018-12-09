import twitter
from twitter import error

consumerKey = '1pTq010ZJiHFSkz7HCuqzXUpN'
consumerSecret = 'ePcw81En1Twu2AXCOg6iacbXDMNdckEE0yuikR8QHrll4T5Okg'
accessToken = '977978225870729216-XjrjD03txdtbRXYu9ZhB11W0pBHeiep'
accessTokenSecret = 'zCdrMT0GTEi2UmEylsBWj5JTYF0U9s0601yIfW7pUv2ig'


def open_connection():
    try:
        # Twitter account connection
        api = twitter.Api(consumer_key=consumerKey,
                          consumer_secret=consumerSecret,
                          access_token_key=accessToken,
                          access_token_secret=accessTokenSecret)
        print("Conectado com sucesso")
        return api
    except error.TwitterError as e:
        print("Erro ao se conectar: " + str(e.message))
        return None
