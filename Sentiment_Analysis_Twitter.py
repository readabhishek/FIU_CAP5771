import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TwitterClient(object):

    def __init__(self):

        # Initialize the keys and tokens for connection
        # keys and tokens from the Twitter Dev Console
        tw_access_token = '983399142331502592-qJYtaJaJzxKsexP0iVureDu0CpQ9RhR'
        tw_access_token_secret = 'ZVGmxiJ6OWfXwOKmcgYu6pi2UJNBpVTILkkm4hvc0qSpk'
        tw_consumer_key = 'eeNHxfLx3A6j9gZVodX1mjOUP'
        tw_consumer_secret = 'vivrEaNXC1zAyqOHG6rcDPw5axkNQynRDOU0Pd02gnkLnUmfUh'

        # Authentication Process ......
        try:
            # Get object of OAuthHandler
            self.auth_twitter = OAuthHandler(tw_consumer_key, tw_consumer_secret)
            # Update access token, access token secret
            self.auth_twitter.set_access_token(tw_access_token, tw_access_token_secret)
            # Create tweepy API object. This is a python package to fetch tweets
            self.twitter_api = tweepy.API(self.auth_twitter)
            print("Successful Authentication ", self.twitter_api)
        except:
            print("Error: Authentication Failed")

    def preProcess_tweet(self, tweet):

        # Utility function to clean tweet text by removing links, special characters using simple regex statements.

        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                "
                   "| (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_sentiment_twitter(self, tweet):

        # Use textblob API to analyze the sentiments from the tweets. Clean the tweets and pass the tweet text
        analysis = TextBlob(self.preProcess_tweet(tweet))
        # Check the polarity of the sentiment and assign +ve, -ve or neutral values.
        if analysis.sentiment.polarity > 0:
            #print("\n Positive Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            #print("\n Neutral Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'neutral'
        else:
            #print("\n Negative Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'negative'

    def get_online_tweets(self, query, count=10):

        # Twitter Analysis Main function. Fetch online tweets realtime.
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.twitter_api.search(q=query, count=count)
            # print("Fetched Tweets ", fetched_tweets)
            # Loop and get each tweets...
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_sentiment_twitter(tweet.text)
                if tweet.retweet_count > 0:
                    # Check if it's not duplicate
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def print_sentiment_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    snt = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(snt)))


def plot_chart(ptweets, ntweets, tot_tweets, title):               # Plot the Pie-Chart
    labels = 'Positive Tweets', 'Negative Tweets', 'Neutral'
    sizes = [(100 * len(ptweets) / len(tot_tweets)), (100 * len(ntweets) / len(tot_tweets)),
             100 * ((len(tot_tweets) - len(ntweets) - len(ptweets)) / len(tot_tweets))]
    colors = ['gold', 'yellowgreen', 'lightcoral']; explode = (0, 0, 0)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(title); plt.axis('equal')
    plt.show()


def main():
    # TwitterClient Object
    twitter_api = TwitterClient()
    # Get tweets
    tweets_by_shortname = twitter_api.get_online_tweets(query='Amex', count=1000)
    tweets_by_fullname = twitter_api.get_online_tweets(query='American Express', count=1000)
    tweets_by_handle = twitter_api.get_online_tweets(query='@AmericanExpress', count=1000)
    pos_tweets, neg_tweets, neu_tweet = [0, 1, 2], [0, 1, 2], [0, 1, 2]
    pos_tweets[0] = [tweet for tweet in tweets_by_shortname if tweet['sentiment'] == 'positive']
    pos_tweets[1] = [tweet for tweet in tweets_by_fullname if tweet['sentiment'] == 'positive']
    pos_tweets[2] = [tweet for tweet in tweets_by_handle if tweet['sentiment'] == 'positive']

    neg_tweets[0] = [tweet for tweet in tweets_by_shortname if tweet['sentiment'] == 'negative']
    neg_tweets[1] = [tweet for tweet in tweets_by_fullname if tweet['sentiment'] == 'negative']
    neg_tweets[2] = [tweet for tweet in tweets_by_handle if tweet['sentiment'] == 'negative']

    neu_tweet[0] = [tweet for tweet in tweets_by_handle if tweet['sentiment'] == 'neutral']

    # print("Request: ", tweets)
    # picking positive tweets from tweets
    ptweets = pos_tweets[0] + pos_tweets[1] + pos_tweets[2]
    tot_tweets = tweets_by_shortname + tweets_by_fullname + tweets_by_handle
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tot_tweets)))
    # picking negative tweets from tweets
    ntweets = neg_tweets[0] + neg_tweets[1] + neg_tweets[2]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tot_tweets)))
    # percentage of neutral tweets
    # print("tweets: ", tweets_by_shortname); print("\n ntweets: ", ntweets); print("\n ptweets: ", ptweets)
    print("Neutral tweets percentage: {} %".format(
        100 * (len(tot_tweets) - len(ntweets) - len(ptweets)) / len(tot_tweets)))

    # Plot the Graph...
    plot_chart(ptweets, ntweets, tot_tweets, "Sentiment Analysis - American Express in Twitter")



    # printing first 5 positive tweets
    '''
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # printing first 5 neutral tweets
    print("\n\n Neutral tweets:")
    for tweet in neu_tweet[0][:10]:
        print(tweet['text'])
        print_sentiment_scores(tweet['text'])
    '''


if __name__ == "__main__":
    # Call the main function
    main()
