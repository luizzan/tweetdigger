# old_tweets

Get old tweets<br>
Heavily based on https://github.com/Jefferson-Henrique/GetOldTweets-python<br>
Main differences are the use of a dictionary to pass parameters and the use of requests instead of urllib for getting data.

## Usage example

```
tw = OldTweets()

params = {
    'q' : '@barackobama',  # Query
    'from' : '',  # Tweeted by @...
    'to' : '',  # Replying to @...
    'since' : '2018-08-08',  # YYYY-MM-DD
    'until' : '2018-08-09',  # YYYY-MM-DD
    'lang' : '',  # Language
    'near' : 'London',  # Location
    'within' : '15mi',  # Radius around location
    'n_tweets' : 0,  # Number of tweets, 0 for unlimited
}

tweets = tw.getTweets(params)

for tweet in tweets:
    print(tweet.text)
```
