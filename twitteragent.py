import tweepy

class TwitterAPI:
    def __init__(self):
        #Authentication data. DO NOT CHANGE!
        CONSUMER_KEY = "mnfxwU0x7PiF2eSOfWwHCv75V"
        CONSUMER_SECRET = "zvTqivkeEl1NlHN5sbu9FcCPZ3RWMz6MP9p5vqncdJshTGo4k0"
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        ACCESS_TOKEN = "922910810493603845-tqwv3w5IU7Cpg9R16FfJqYGvtUseu38"
        ACCESS_TOKEN_SECRET = "wEQVNHqMuMJZGCBqvLnednY6Q5ZX3JuO2e1Yg9JjQjEMn"
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

