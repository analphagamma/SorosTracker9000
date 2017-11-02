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
    
    #because we didn't store the links in memory we need to open the json again
    #//TODO: optimalise this for when the json file grows too big?
    with open('tweet_log.json', 'r+') as f: tweet_log = json.load(f)
    with open('links.txt', 'r+') as f: linkdb = f.read().split('\n')
    
    tweets = 0
    for title, link in tweet_log[str(date.today())][name]:
        if name in title:
            site = ''
        else:
            site = name
        if link not in linkdb:      
            tweet_content = '{}\n{}\n#Soros #SorosTerv\n{}'.format(site, title, link).strip('\n').strip()
            
            SorosTrackerBot.tweet(tweet_content)
            #add new links to logfile
            with open('links.txt', 'a+') as f: f.write(link + '\n')
            time.sleep(1) #let's not overload Twitter
            print('Tweeting link for ', title)
            tweets += 1
        else:
            print('Link already tweeted\n', link)
    
    if tweets == 0:
        print('A(z) {} {} cikket jelentetett meg Sorosról, de ma nem jelent meg új cikk.'.format(name, links[name]))
        SorosTrackerBot.tweet('A(z) {} {} cikket jelentetett meg Sorosról, de ma nem jelent meg új cikk.'.format(name, links[name]))
    else:
        print('Ma a(z) {} {} cikket jelentetett meg Sorosról. Ebből {} cikk volt új.\n#Soros #SorosTerv'.format(name, links[name], tweets))
        SorosTrackerBot.tweet('Ma a(z) {} {} cikket jelentetett meg Sorosról. Ebből {} cikk volt új.\n#Soros #SorosTerv'.format(name, links[name], tweets))
            
if __name__ == '__main__':
    main()
    print('\nCrawling done.\nSoros uncovered.')

