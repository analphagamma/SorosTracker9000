#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SCrawler import *
import tweepy
from twitteragent import *
import time
from datetime import date
import json

NEWS_SOURCES = {'Magyar Hírlap': 'http://magyarhirlap.hu',
				'Hirado.hu': 'http://www.hirado.hu',
				'Magyar Idők': 'http://magyaridok.hu',
				'Origo.hu': 'http://www.origo.hu'}

def main():
	SorosTrackerBot = TwitterAPI()
	print('Waking up bot...')
	
	links = crawl_websites(NEWS_SOURCES)
	name = max(links, key=links.get) #finds which source has the most links
	
	#Once per day, we tweet which source had the most articles
	#SorosTrackerBot.tweet('Ma a(z) {} {} cikket jelentetett meg Sorosról.\n#Soros #SorosTerv'.format(name, links[name]))
	
	#because we didn't store the links in memory we need to open the json again
	#//TODO: optimalise this for when the json file grows too big?
	with open('tweet_log.json', 'r+') as f: tweet_log = json.load(f)
	with open('links.txt', 'r+') as f: linkdb = f.read().split('\n')
	
	for title, link in tweet_log[str(date.today())][name]:
		if name in title:
			name = ''
		if link not in linkdb:		
			tweet_content = '{}\n{}\n#Soros\n{}'.format(name, title, link).strip('\n').strip()
			
			#SorosTrackerBot.tweet(tweet_content)
			#add new links to logfile
			with open('links.txt', 'a+') as f: f.write(link + '\n')
			time.sleep(1) #let's not overload Twitter
			print('Tweeting link for ', title) 
		else:
			pass
		
if __name__ == '__main__':
	main()
	print('\nCrawling done.\nSoros uncovered.')

