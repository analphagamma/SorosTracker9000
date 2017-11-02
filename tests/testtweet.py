import tweepy

class TwitterAPI:
    def __init__(self):
        #Authentication data. DO NOT CHANGE!
        CONSUMER_KEY = ""
        CONSUMER_SECRET = ""
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        ACCESS_TOKEN = ""
        ACCESS_TOKEN_SECRET = ""
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        '''Makes a text tweet'''
        self.api.update_status(status=message)

testbot = TwitterAPI()
testbot.tweet('Teszt tweet.')

