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
        try:
            self.api.update_status(status=message)
        except tweepy.error.TweepError:
            #Twitter deosn't allow consecutive tweets to be the same
            #...not that we would want to tweet something twice, right?
            print('Problem with tweet. Possible duplicate')

