import tweetdigger as td

tweets = td.get_tweets(
	since='2018-08-25',
	q='@wizzair',
	#n_tweets=25,
	filename='output.csv',
)

for tweet in tweets:
	print(tweet.username)