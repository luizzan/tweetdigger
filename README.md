# tweetdigger

Get tweets by time, location, language, etc.

## Usage example
```
import tweetdigger

tweets = tweetdigger.get(
    q='@barackobama,
    since='2018-01-01',
    n_tweets=25,
)

for tweet in tweets:
    print(tweet.text)
```

## Save to csv file
```
import tweetdigger

tweetdigger.get(
    q='@barackobama,
    since='2018-01-01',
    n_tweets=25,
    filename = 'output.csv',
)
```

## .get() arguments
- q : str  # Query, e.g. '@barackobama #republicans'
- from : str  # Tweeted by @...
- to : str  # Replying to @...
- since : str  # YYYY-MM-DD
- until : str  # YYYY-MM-DD
- lang : str  # Language, e.g. 'en'
- near : str  # Location, e.g. 'London'
- within : str  # Radius around location, e.g. 15mi
- n_tweets : int  # Number of tweets - use 0 for unlimited
- filename : str  # Save tweets to file

## Note
When *not* saving to a csv file, all tweets will be collected and returned in bulk. Be careful when using this mode to collect a large amount of tweets!

When saving to a csv file, tweetdigger will collect small batches of up to 20 tweets at a time, which will be immediately saved to the file. The file can be copied and the copy used during the digging process without affecting the original file.