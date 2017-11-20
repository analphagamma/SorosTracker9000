#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import time
import json
import SCrawler
from sorosstats import Table
from datetime import date
from twitteragent import *
from random import randint

NEWS_SOURCES = {'Magyar Hírlap': 'http://magyarhirlap.hu/',
                'Hirado.hu': 'http://www.hirado.hu/',
                'Magyar Idők': 'http://magyaridok.hu/',
                'Origo.hu': 'http://www.origo.hu/',
                '888.hu': 'http://888.hu/'}
                
DAILY_MESSAGES = ['\nMa ennyire volt fontos Sorossal foglalkozni.',
                  '\nMa is lelepleztük Sorost!',
                  '\nEgy lépéssel közelebb a megváltáshoz.',
                  '\nNem alszunk!',
                  '\nNem hagytuk!',
                  '\nMegint sokat foglalkoztunk Sorossal!']

def main():
    ''' main function that creates the bot object
        makes the daily stats
        tweets all the articles
        '''
    
    SorosTrackerBot = TwitterAPI()
    print('Bot initialized.')
    links = SCrawler.crawl_websites(NEWS_SOURCES)
    print('Crawling done.\n')
    
    def tweet_daily_stats():
        ''' crawls NEWS SOURCE websites
            stores link in the tweet_log.json
            creates a pandas df from the json file
            tweets todays statistics'''
        
        
        stat_obj = Table('tweet_log.json')
        ##TODO// if no articles were posted the tweet should say something different
        d_message = DAILY_MESSAGES[randint(0, len(DAILY_MESSAGES)-1)]
        
        SorosTrackerBot.tweet('Ma ennyi cikk jelent meg Sorosról.\n#Soros #SorosTerv\n' +
                              stat_obj.sum_today().to_string() +
                              d_message)
        print('Ma ennyi cikk jelent meg Sorosról:\n' +
              stat_obj.sum_today().to_string() +
              '\n#Soros #SorosTerv\n' +
              d_message)
    
    def tweet_articles():   
        ''' loops through today's links
            tweets articles one by one
            stores link in a txt logfile to later prevent duplicate posting'''
                
        for source in links:
            for title, link in links[source]:
                if source in title:
                    source = ''
                
                tweet_content = '{}\n{}\n#Soros\n{}'.format(source, title, link).strip('\n').strip()
                print(tweet_content)    
                SorosTrackerBot.tweet(tweet_content)
                
                #add new links to logfile
                with open('links.txt', 'a+') as f: f.write(link + '\n')
                time.sleep(1) #let's not overload Twitter
                print('Tweeting link for ', title) 
    
    tweet_articles()
    tweet_daily_stats()
    
            
if __name__ == '__main__':
    main()
    print('\nCrawling done.\nSoros uncovered.')

