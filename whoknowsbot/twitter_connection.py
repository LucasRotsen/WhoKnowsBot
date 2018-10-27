import twitter
from twitter import error

consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = ''


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
