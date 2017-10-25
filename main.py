#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SCrawler import SorosCrawler
import tweepy
import time
from datetime import date
import json

NEWS_SOURCES = {'Magyar Hírlap': 'http://magyarhirlap.hu',
					'Hirado.hu': 'http://www.hirado.hu',
					'Magyar Idők': 'http://magyaridok.hu',
					'Origo.hu': 'http://www.origo.hu'}


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


def simple_log(source_website, links):
		with open('tweet_log.json', 'r+') as f: log = json.load(f)
		try:
			log[str(date.today())]
		except KeyError:
			log[str(date.today())] = {}
		
		log[str(date.today())][source_website] = links
		
		with open('tweet_log.json', 'w+') as f: json.dump(log, f)
		print('Links for {} logged for {}'.format(source_website, date.today()))
		f.close()



if __name__ == '__main__':
	SorosTrackerBot = TwitterAPI()
	print('Waking up bot...')
	
	for name, url in NEWS_SOURCES.items():
		'''Iterating through all the news sources
		   Scraping links
		   Logging links to date
		   
		   Tweeting.'''
		   
		obj = SorosCrawler(name, url)
		
		print('\nGetting news from {}'.format(name))
		todays_links = obj.parse_links()
		print('Number of articles found: ', len(todays_links))
		#logging links
		simple_log(name, todays_links)
		
		
		for title, link in todays_links:
			
			#some article titles already have the name of the news source
			if name in title:
				name = ''
			
			tweet_content = '{}\n{}\n{}'.format(name, title, link).strip('\n').strip()
			#Tweeting
			SorosTrackerBot.tweet(tweet_content)
			time.sleep(1)
			print('Tweeting links for ', name)
			
	print('\nCrawling done.\nSoros uncovered.')

