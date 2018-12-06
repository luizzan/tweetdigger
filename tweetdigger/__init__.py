import json
import re
import datetime as dt
import sys
import csv
import http.cookiejar
import requests
import urllib
from bs4 import BeautifulSoup

__version__ = '0.2.0'

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
			cols = [
				'date',
				'username',
				'text',
				'retweets',
				'favorites',
				'id',
				'permalink',
				'verified',
				'language',
				'emojis',
				'date_original',
			]
			with open(filename, 'w') as f:
				csv.writer(f).writerow(cols)
		
		tweet_count = 0
		exception_count = 0
		tweets = []
		while True:
			
			params, tweet_batch, status = _get_json_to_tweets(params)

			if status == 'skipped':
				continue

			if status == 'finished':
				break

			# Break if 3 exceptions in a row
			if status == 'exception':
				if exception_count >= 3:
					break
				else:
					exception_count += 1
					continue
			else:
				exception_count = 0

			if not tweet_batch:
				break
			
			if params['n_tweets'] > 0:
				remaining = params['n_tweets'] - tweet_count
				tweet_batch = tweet_batch[0:remaining]

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
							tweet.verified,
							tweet.language,
							tweet.emojis,
							tweet.date_original,
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

	# Use 'by' instead of 'from' to avoid syntax conflicts
	# "from" should come just after "q" ?
	_bys = kwargs.pop('by', None)
	if _bys:
		if type(_bys) == list:
			_bys = [i.replace('@', '') for i in _bys]
			url_add += ' from:{}'.format(_bys[0])
			for _by in _bys[1:]:
				url_add += ' OR from:{}'.format(_by)
		else:
			url_add += ' from:{}'.format(_bys.replace('@', ''))

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
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Referer': url,
		'Connection': 'keep-alive'
	}

	try:
		response = requests.get(url, headers=headers, cookies=params['cookiejar'])
		json_response = response.json()

		if len(json_response['items_html'].strip()) == 0:
		return params, [], 'finished'

	except:
		return params, [], 'exception'

	if params['cursor'] == json_response['min_position']:
		# If Twitter has sent the same batch of tweets, skip them
		return params, [], 'skipped'

	else:
		params['cursor'] = urllib.parse.quote(json_response['min_position'])

		html_tweets = BeautifulSoup(json_response['items_html'], 'lxml').find_all('div', 'tweet')

		tweet_batch = []
		for tw in html_tweets:

			try:
				tweet = TweetHolder()
				tweet.date = tw.find('span', '_timestamp')['data-time']
				tweet.date = dt.datetime.fromtimestamp(int(tweet.date))
				tweet.date = tweet.date.astimezone(tz=dt.timezone.utc)
				try:
					tweet.date_original = tw.find('a', 'tweet-timestamp')['title']
					tweet.date_original = dt.datetime.strptime(tweet.date_original, '%I:%M %p - %d %b %Y')
				except:
					tweet.date_original = None
				tweet.username = tw.find('span', 'username').get_text()
				tweet.text = tw.find('p', 'tweet-text').get_text()
				tweet.retweets = tw.find('span', 'ProfileTweet-action--retweet')
				tweet.retweets = int(tweet.retweets.find('span', 'ProfileTweet-actionCount')['data-tweet-stat-count'])
				tweet.favorites = tw.find('span', 'ProfileTweet-action--favorite')
				tweet.favorites = int(tweet.favorites.find('span', 'ProfileTweet-actionCount')['data-tweet-stat-count'])
				tweet.id = tw['data-item-id']
				tweet.permalink = 'https://twitter.com' + tw['data-permalink-path']
				tweet.verified = tw.find('span', 'FullNameGroup').find('span', 'Icon--verified')
				tweet.verified = True if tweet.verified else False
				tweet.language = tw.find('p', 'tweet-text')['lang']
				emojis = tw.find('p', 'tweet-text').find_all('img')
				tweet.emojis = [emoji.get('alt') for emoji in emojis]
				tweet.emojis = ''.join(tweet.emojis)

				tweet_batch.append(tweet)

			except:
				# Avoids issues with withheld or defective tweets.
				pass
		
		return params, tweet_batch, 'working'


def get_followers(username):

	url = 'https://twitter.com/{}'.format(username.replace('@', ''))
	cookiejar = http.cookiejar.CookieJar()
	
	headers = {
		'Host': 'twitter.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Referer': url,
		'Connection': 'keep-alive'
	}

	try:
		text = requests.get(url, headers=headers, cookies=cookiejar).text
		followers = int(re.findall('followers_count&quot;:([0-9]*)', text)[0])
	except:
		followers = 0

	return followers
