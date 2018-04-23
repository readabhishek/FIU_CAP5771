import os
import re
import csv
import json
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TwitterClient(object):

    def __init__(self):

        # Initialize the keys and tokens for connection
        # keys and tokens from the Twitter Dev Console
        tw_access_token = 'xxxxxxxxxxxxxxxxxxxxxx'
        tw_access_token_secret = 'yyyyyyyyyyyyyyyyyyyyyy'
        tw_consumer_key = 'zzzzzzzzzzzzzzzzzzzzz'
        tw_consumer_secret = 'ddddddddddddddddddddd'

        # Authentication Process ......
        try:
            # Get object of OAuthHandler
            self.auth_twitter = OAuthHandler(tw_consumer_key, tw_consumer_secret)
            # Update access token, access token secret
            self.auth_twitter.set_access_token(tw_access_token, tw_access_token_secret)
            # Create tweepy API object. This is a python package to fetch tweets
            self.twitter_api = tweepy.API(self.auth_twitter, wait_on_rate_limit=True)
            print("Successful Authentication ", self.twitter_api)
        except:
            print("Error: Authentication Failed")

    def preProcess_tweet(self, tweet):

        # Utility function to clean tweet text by removing links, special characters using simple regex statements.
        print(tweet)
        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                "
                   "| (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_sentiment_twitter(self, tweet):

        # Use textblob API to analyze the sentiments from the tweets. Clean the tweets and pass the tweet text
        analysis = TextBlob(self.preProcess_tweet(tweet))
        # Check the polarity of the sentiment and assign +ve, -ve or neutral values.
        if analysis.sentiment.polarity > 0:
            # print("\n Positive Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'positive', analysis.sentiment.polarity
        elif analysis.sentiment.polarity == 0:
            # print("\n Neutral Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'neutral', analysis.sentiment.polarity
        else:
            # print("\n Negative Polarity  ", analysis.sentiment.polarity, "  ", tweet)
            return 'negative', analysis.sentiment.polarity

    def get_online_tweets(self, query, count=10):

        # Twitter Analysis Main function. Fetch online tweets realtime.
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.twitter_api.search(q=query, count=count, full_text='true')
            # print("Fetched Tweets ", fetched_tweets)
            # Loop and get each tweets...
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text.encode('utf8')
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

    def analyze_sentiments(self, filename):

        tweets = []
        with open('./project_modules/data_temp.csv', 'w', newline='') as writefile:
            with open(filename, newline='') as readfile:
                fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
                reader = csv.DictReader(readfile)
                writer = csv.DictWriter(writefile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    parsed_tweet = {}
                    parsed_tweet['Date'] = row['Date']
                    parsed_tweet['Tweet'] = row['Tweet']
                    parsed_tweet['Sentiment'], parsed_tweet['Score'] = self.get_sentiment_twitter(row['Tweet'])
                    row['Sentiment'] = parsed_tweet['Sentiment']
                    row['Score'] = parsed_tweet['Score']
                    writer.writerow(row)
                    tweets.append(parsed_tweet)
            readfile.close()
        writefile.close()

        os.remove(filename)
        os.rename('./project_modules/data_temp.csv', filename)
        return tweets


def print_sentiment_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    snt = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(snt)))


def load_JSON_file(filename, entity):
    query = [];
    data = json.load(open(filename))
    raw_keys = data[entity]["keys"].split(",")
    title = data[entity]["title"].split(",")
    for keys in raw_keys:
        query.append(keys.strip(' \t\n\r'))
    return query, title


def plot_chart(ptweets, ntweets, tot_tweets, title):  # Plot the Pie-Chart
    labels = 'Positive Tweets', 'Negative Tweets', 'Neutral'
    sizes = [(100 * len(ptweets) / len(tot_tweets)), (100 * len(ntweets) / len(tot_tweets)),
             100 * ((len(tot_tweets) - len(ntweets) - len(ptweets)) / len(tot_tweets))]
    colors = ['gold', 'yellowgreen', 'lightcoral'];
    explode = (0, 0, 0)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(title);
    plt.axis('equal')
    plt.show()


def parse_tweet_polarity(tweets):
    tweets_polarity = [0, 1, 2]
    tweets_polarity[0] = [tweet for tweet in tweets if tweet['Sentiment'] == 'positive']
    tweets_polarity[1] = [tweet for tweet in tweets if tweet['Sentiment'] == 'negative']
    tweets_polarity[2] = [tweet for tweet in tweets if tweet['Sentiment'] == 'neutral']
    return tweets_polarity


def get_tweets_online(tweets, title):
    positive_tweets, negative_tweets, neutral_tweets = [], [], []

    tweets_polarity = parse_tweet_polarity(tweets)
    for items in tweets_polarity[0]:
        if items not in positive_tweets:
            positive_tweets.append(items)
    for items in tweets_polarity[1]:
        if items not in negative_tweets:
            negative_tweets.append(items)
    for items in tweets_polarity[2]:
        if items not in neutral_tweets:
            neutral_tweets.append(items)

    tot_tweets = positive_tweets + negative_tweets + neutral_tweets


    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tot_tweets)))
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tot_tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(
        100 * (len(tot_tweets) - len(negative_tweets) - len(positive_tweets)) / len(tot_tweets)))

    # Plot the Graph...
    plot_chart(positive_tweets, negative_tweets, tot_tweets, title)

# printing first 5 positive tweets
'''
print("\n\nPositive tweets:")
f = open("Twitter_Comments.txt", "w+")
for tweet in positive_tweets[:10]:
    print(tweet['text'])
    f.write(tweet['text'])


# printing first 5 negative tweets
print("\n\nNegative tweets:")
for tweet in negative_tweets[:10]:
    print(tweet['text'])

# printing first 5 neutral tweets
print("\n\n Neutral tweets:")
for tweet in neutral_tweets[:10]:
    print(tweet['text'])
    print_sentiment_scores(tweet['text'])

'''


def main():
    # TwitterClient Object
    twitter_api = TwitterClient()
    '''
    #Get keywords and official twitter handle for 'American Express' and use those keywords for retrieving the tweets.
    query_Amex, title_Amex = load_JSON_file('Keywords.json', 'Amex')

    # Get keywords and official twitter handle for 'Chase Bank' which is competitor for Amex and use those keywords for retrieving the tweets.
    query_Chase, title_Chase = load_JSON_file('Keywords.json', 'Chase')

    # Get keywords and official twitter handle for 'Capital One Bank' which is competitor for Amex and use those keywords for retrieving the tweets.
    query_CapOne, title_CapOne = load_JSON_file('Keywords.json', 'CapitalOne')

    get_tweets_online(twitter_api, query_Amex, *title_Amex)      # Astricks(*) is used to unpack the tuple value.
    get_tweets_online(twitter_api, query_Chase, *title_Chase)
    get_tweets_online(twitter_api, query_CapOne, *title_CapOne)

    '''

    tweets = twitter_api.analyze_sentiments('./project_modules/Tweets_Amex.csv')
    get_tweets_online(tweets, "Amex")


if __name__ == "__main__":
    # Call the main function
    main()
