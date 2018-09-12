import json
import re
import datetime as dt
import sys
import csv
import http.cookiejar
import requests
import urllib
from bs4 import BeautifulSoup

__version__ = '0.1.0'

"""
kwargs
- q : str  # Query
- from : str  # Tweeted by @...
- to : str  # Replying to @...
- since : str  # YYYY-MM-DD
- until : str  # YYYY-MM-DD
- lang : str  # Language
- near : str  # Location
- within : str  # Radius around location, e.g. 15mi
- n_tweets : int  # Number of tweets - use 0 for unlimited
- filename : str  # Save tweets to file
"""

class TweetHolder():
	# Placeholder class to store each component of a tweet
	pass


def get(**kwargs):

		filename = kwargs.pop('filename', '')

		params = {}
		params['n_tweets'] = kwargs.pop('n_tweets', 0)
		params['cursor'] = kwargs.pop('cursor', '')
		params['cookiejar'] = http.cookiejar.CookieJar()
		params['url'] = _build_url(kwargs)

		if filename:
			cols = ['date', 'username', 'text', 'retweets', 'favorites', 'id', 'permalink']
			with open(filename, 'w') as f:
				csv.writer(f).writerow(cols)
		
		tweet_count = 0
		tweets = []
		while True:
			
			params, tweet_batch = _get_json_to_tweets(params)

			if tweet_batch and params['n_tweets'] > 0:
				remaining = params['n_tweets'] - tweet_count
				tweet_batch = tweet_batch[0:remaining]

			if not tweet_batch:
				break

			tweet_count += len(tweet_batch)

			if filename:
				try:
					tws = []
					for tweet in tweet_batch:
						tw = [
							tweet.date,
							tweet.username,
							tweet.text,
							tweet.retweets,
							tweet.favorites,
							tweet.id,
							tweet.permalink,
						]
						tws.append(tw)

					with open(filename, 'a') as f:
						csv.writer(f).writerows(tws)

				except:
					print('Error! Last cursor: ' + self.cursor)
					print(sys.exc_info()[0])
					return

			else:
				tweets += tweet_batch

			if params['n_tweets'] > 0 and tweet_count >= params['n_tweets']:
				break

		if not filename:
			return tweets
		else:
			return []


def _build_url(kwargs):
	
	url = 'https://twitter.com/i/search/timeline?f=tweets&src=typd'

	lang = kwargs.pop('lang', '')
	if lang:
		url += '&l={}'.format(lang)

	url += '&q='
	
	url_add = ''
	url_add += kwargs.pop('q', '')

	_near = kwargs.pop('near', None)
	if _near:
		kwargs['near'] = '"' + _near + '"'
	
	for k, v in kwargs.items():
		if v:
			url_add += ' {}:{}'.format(k, v)

	url += urllib.parse.quote(url_add)

	return url


def _get_json_to_tweets(params):

	url = params['url'] + '&max_position={}'.format(params['cursor'])

	headers = {
		'Host': 'twitter.com',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
		'Referer': url,
		'Connection': 'keep-alive'
	}

	try:
		response = requests.get(url, headers=headers, cookies=params['cookiejar'])
		json_response = response.json()
	except:
		return params, []

	if len(json_response['items_html'].strip()) == 0:
		return params, []

	params['cursor'] = json_response['min_position']

	html_tweets = BeautifulSoup(json_response['items_html'], 'lxml').find_all('div', 'tweet')

	tweet_batch = []
	for tw in html_tweets:

		tweet = TweetHolder()
		tweet.date = tw.find('span', '_timestamp')['data-time']
		tweet.date = dt.datetime.fromtimestamp(int(tweet.date))
		tweet.username = tw.find('span', 'username').get_text()
		tweet.text = tw.find('p', 'tweet-text').get_text()
		tweet.retweets = tw.find('span', 'ProfileTweet-action--retweet')
		tweet.retweets = int(tweet.retweets.find('span', 'ProfileTweet-actionCount')['data-tweet-stat-count'])
		tweet.favorites = tw.find('span', 'ProfileTweet-action--favorite')
		tweet.favorites = int(tweet.favorites.find('span', 'ProfileTweet-actionCount')['data-tweet-stat-count'])
		tweet.id = tw['data-item-id']
		tweet.permalink = 'https://twitter.com' + tw['data-permalink-path']

		tweet_batch.append(tweet)
		
	return params, tweet_batch
