import tweetdigger

tweets = tweetdigger.get_tweets(
	since='2018-08-25',
	q='@wizzair',
	n_tweets=25,
	#filename='output.csv',
)

for tweet in tweets:
	print(tweet.username)


info = tweetdigger.get_info(
	['wizzair', 'barackobama'],
	#filename='output.csv',
)

for i in info:
	print(i.name)