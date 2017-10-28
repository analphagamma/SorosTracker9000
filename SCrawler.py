#!/usr/bin/env python

import re
import json
import requests
from datetime import date
from bs4 import BeautifulSoup

class SorosCrawler(object):
	'''This object is a crawler that 
		-opens the website
		-gets all links from it
		-picks out the links that have "soros" in them
			
		To instantiate the object provide a name (i.e. the website name) and an URL
		Example: obj = SorosCrawler('Best News Site', 'http://www.bestnewssite.com')'''
		
		
	def __init__(self, source_name, url):
		self.source_name = source_name
		self.url = url
		
	def get_links(self):
		'''opens the website and gets all links from the html source
			Returns a set of the links to prevent duplication'''
		
		html = requests.get(self.url).content
		soup = BeautifulSoup(html, 'html.parser')
		
		all_links = []
		for link in soup.find_all('a'):
			all_links.append(link.get('href'))
		
		return set(all_links) #all the hyperlinks from the website + duplicates removed
		
	def parse_links(self):
		'''Picks all links that have 'soros' in them
			If the href is incomplete it adds 'http:' to the front'''
		
		links = []
		for link in self.get_links():
			try:
				re.search('soros', link)
			except TypeError:
				pass
			else:	
				#search for the word soros in link
				if re.search('soros', link.lower()):
					if not re.search(self.url, link):
						#sometimes the href doesn't have the full, absolute path
						link = self.url + link
					if link[:4] != 'http':
						#sometimes links are from the absolute path but requests needs the http too.
						link = 'http' + link
					
					html = requests.get(link).content
					soup = BeautifulSoup(html, 'html.parser')
					
					links.append((soup.title.string.strip('\n').strip(), link))

		return links #list of tuples (article title, article link)

def simple_log(source_website, links):
	'''updates the JSON log with today's articles'''
	
	with open('tweet_log.json', 'r+') as f: tweet_log = json.load(f)
	try:
		#if there's no entry for today it creates key
		tweet_log[str(date.today())]
	except KeyError:
		tweet_log[str(date.today())] = {}
	
	tweet_log[str(date.today())][source_website] = links
	
	with open('tweet_log.json', 'w+') as f: json.dump(tweet_log, f)
	print('Links for {} logged for {}'.format(source_website, date.today()))
	f.close()

def crawl_websites(websites):
	'''collects all the articles from all sources
	   then picks out the sources that has the most articles
	   and returns the links in list
	   
	   takes a dictionary as an argument {source name: link to source's main page}'''
	
	todays_articles = {}
	
	for name, url in websites.items():
		'''Iterating through all the news sources
		   Scraping links
		   Logging links to date'''
		   
		obj = SorosCrawler(name, url)
		
		print('Getting news from {}'.format(name))
		todays_links = obj.parse_links()
		print('Number of articles found: ', len(todays_links))
		#logging links
		simple_log(name, todays_links)
		todays_articles[name] = len(todays_links)
		
	return todays_articles
