import tweetdigger

tweets = tweetdigger.get(
	since='2018-08-25',
	q='@wizzair',
	n_tweets=25,
	#filename='output.csv',
)

for tweet in tweets:
	print(tweet.username)
