#   command: python scrape.py

import requests
from bs4 import BeautifulSoup
from pprint import pprint

#page 1
res = requests.get('https://news.ycombinator.com/news')

#page 2
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
links.extend(soup2.select('.storylink'))

subtext = soup.select('.subtext')
subtext.extend(soup2.select('.subtext'))

print(len(links))

def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key=lambda x : x['votes'], reverse=True)

def create_custom_hn(links, subtext):
	hn = []
	for idx, item in enumerate(links):
		title = item.getText()
		href = item.get('href', None)
		vote = subtext[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace('points', ''))
			if points > 99:
				hn.append({'title': title, 'link': href, 'votes': points})
	return sort_stories_by_votes(hn)

pprint(create_custom_hn(links, subtext))