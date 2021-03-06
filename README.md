# tweetdigger

Get tweets by time, location, language, etc.<br>
Get info from profiles.

## Usage example
```
import tweetdigger

tweets = tweetdigger.get_tweets(
    q='@barackobama,
    since='2018-01-01',
    n_tweets=25,
)

for tweet in tweets:
    print(tweet.text)

info = tweetdigger.get_info('barackobama')
print(info.followers)
```

Information available:
```
tweet.date
tweet.username
tweet.text
tweet.retweets
tweet.favorites
tweet.id
tweet.permalink
tweet.verified
tweet.language
tweet.emojis

info.username or info.handle
info.name
info.followers
info.following
info.likes or info.favorites
info.tweets
info.location
info.description
```

## Save to csv file
```
import tweetdigger

tweetdigger.get_tweets(
    q='@barackobama,
    since='2018-01-01',
    n_tweets=25,
    filename = 'output.csv',
)

tweetdigger.get_info(
	['wizzair', 'barackobama'],
	filename = 'output.csv',
)
```

## .get_tweets() arguments
- q : str  # Query, e.g. '@barackobama #republicans'
- by : str  or [str, ..., str]  # Tweeted by @...
- to : str  # Replying to @...
- since : str  # YYYY-MM-DD
- until : str  # YYYY-MM-DD
- lang : str  # Language, e.g. 'en'
- near : str  # Location, e.g. 'London'
- within : str  # Radius around location, e.g. 15mi
- n_tweets : int  # Number of tweets - use 0 for unlimited
- filename : str  # Save tweets to file

## .get_info() arguments
- username : str or [str, ..., str]  # Twitter handle / username
- filename : str  # Save tweets to file

## Note
When *not* saving to a csv file, all tweets will be collected and returned in bulk. Be careful when using this mode to collect a large amount of tweets!

When saving to a csv file, tweetdigger will collect small batches of up to 20 tweets at a time, which will be immediately saved to the file. The file can be copied and the copy used during the digging process without affecting the original file.

Information from profiles is added to the file one at a time.
