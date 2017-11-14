import tweepy
import json

class TwitterAPI:
    def __init__(self):
        #Authentication data. DO NOT CHANGE!
        with open('auth_codes.json', 'r+') as f: auth_codes = json.load(f)
        
        CONSUMER_KEY = auth_codes['CONSUMER_KEY']
        CONSUMER_SECRET = auth_codes['CONSUMER_SECRET']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        ACCESS_TOKEN = auth_codes['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = auth_codes['ACCESS_TOKEN_SECRET']
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
      
    def tweet(self, message):
        '''Makes a text tweet'''
        try:
            self.api.update_status(status=message)
        except tweepy.error.TweepError:
            #Twitter doesn't allow consecutive tweets to be the same
            #...not that we would want to tweet something twice, right?
            print('Problem with tweet.')

    
