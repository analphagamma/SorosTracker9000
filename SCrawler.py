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

    def keyword_filter(self, keyword, href_link):
        '''uses regex to find the keyword in the link
           then transform the link to a valid hyperlink
           returns an url in string format'''

        if re.search(keyword, href_link.lower()) and not re.search('cth', href_link.lower()):
            if href_link[0] == '/':
                #no double slashes
                href_link = href_link.strip('/')
            if href_link[:3] == 'www':
                href_link = 'http://' + href_link
            if not re.search(self.url, href_link):
                #sometimes the href doesn't have the full, absolute path
                href_link = self.url + href_link
            
            return href_link
        else:
            return None

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
                link = self.keyword_filter('soros', link)
                if link != None:
                    print(link)
                    try:
                        html = requests.get(link).content
                    except:
                        print('Requests encountered an error with the link:\n', link)
                    else:
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

       [In] -> takes a dictionary as an argument {source name: link to source's main page}
       [Out] -> dict {source: list of links}'''

    todays_articles = {}

    for name, url in websites.items():
        '''Iterating through all the news sources
           Scraping links
           Logging links to date'''

        obj = SorosCrawler(name, url)

        print('\nGetting news from {}'.format(name))
        todays_links = obj.parse_links()
        print('Number of articles found: ', len(todays_links))

        #logging links
        with open('links.txt', 'r+') as f: linkdb = f.read().split('\n')
        rejected_links = []
        for link in todays_links:
            print(link)
            #removing the ones that are already in the db
            if link[1] in linkdb:
                rejected_links.append(link)
                print('Link already in list')
            else:
                print('New article found.')
        
        for link in rejected_links:
            todays_links.remove(link)

        simple_log(name, todays_links)
        todays_articles[name] = todays_links

    return todays_articles

if __name__ == '__main__':
    NEWS_SOURCES = {'Magyar Hírlap': 'http://magyarhirlap.hu/',
                'Hirado.hu': 'http://www.hirado.hu/',
                'Magyar Idők': 'http://magyaridok.hu/',
                'Origo.hu': 'http://www.origo.hu/',
                '888.hu': 'http://888.hu/'}
    print(crawl_websites(NEWS_SOURCES))
