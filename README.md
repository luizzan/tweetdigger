# old_tweets

Get tweets

Arguments:
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

tweets = tweetdigger.get(
    q='@barackobama,
    since='2018-01-01',
    n_tweets=25,
    filename = 'output.csv',
)

for tweet in tweets:
    print(tweet.text)
```
