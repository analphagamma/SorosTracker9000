#!/usr/bin/env python

import re
import json
import requests
import time
from datetime import date
from bs4 import BeautifulSoup

class SorosCrawler(object):
	'''This object is a crawler that 
		-opens the website
		-gets all links from it
		-picks out the links that have "soros" in them
		-updates the JSON log file with today's date and the links it found
		
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
		
		return set(all_links)
		
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
				if re.search('soros', link.lower()):
					if not re.search(self.url, link):
						link = self.url + link
					if link[:5] != 'http:':
						link = 'http:' + link
					
					html = requests.get(link).content
					soup = BeautifulSoup(html, 'html.parser')
					
					links.append((soup.title.string.strip('\n').strip(), link))
					time.sleep(2)
		return links
