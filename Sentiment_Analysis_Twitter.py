import os
import re
import csv
import json
import datetime
import pickle
import tweepy
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from CAP5771.Project import AuthenticationInfo
from CAP5771.Project import PreProcess_Training_Dataset
from CAP5771.Project import TextBlob_Classifier

import CAP5771.Project.Test_Codes


class TwitterClient(object):

    def __init__(self):

        # Initialize the keys and tokens for connection
        tw_access_token,  tw_access_token_secret, tw_consumer_key, tw_consumer_secret = AuthenticationInfo.getAuthenticationInfo()

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

        string = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                "
                   "| (\w +:\ / \ / \S +)", " ", tweet).split())
        string = re.sub(r'^https?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)     # Remove links
        return string



    def get_sentiment_twitter(self, tweet, classifier=None):

        # Use textblob API to analyze the sentiments from the tweets. Clean the tweets and pass the tweet text
        if classifier=='1':
            analysis = TextBlob(self.preProcess_tweet(tweet))  # Default Pattern Analyzer

        elif classifier=='2':
            analysis = TextBlob(self.preProcess_tweet(tweet), analyzer=NaiveBayesAnalyzer())    # Default NB Analyzer

            if analysis.sentiment.classification == 'pos':
                polarity = (analysis.sentiment.p_pos - analysis.sentiment.p_neg)
                return 'positive', polarity
            elif analysis.sentiment.classification == 'neg':
                polarity = (-1)*(analysis.sentiment.p_neg - analysis.sentiment.p_pos)
                return 'negative', polarity
            else:
                return 'neutral', 0
        elif classifier=='3':
            nbc_classifier = TextBlob_Classifier.getnbc_classifier()                  # Restore the customed trained classifier
            analysis = TextBlob(self.preProcess_tweet(tweet), classifier=nbc_classifier)      # Pass custome classifier
        else:
            analysis = TextBlob(self.preProcess_tweet(tweet))  # Default Pattern Analyzer

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



    def get_online_tweets(self, query, count=10, classifier=None): # Not using now. It was coded for testing

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
                parsed_tweet['sentiment'] = self.get_sentiment_twitter(tweet.text, classifier=classifier)
                if tweet.retweet_count > 0:
                    # Check if it's not duplicate
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))



    def analyze_sentiments(self, filename, tempfile, classifier=None):

        tweets = []
        with open(tempfile, 'w', newline='') as writefile:
            with open(filename, newline='') as readfile:
                fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
                reader = csv.DictReader(readfile)
                writer = csv.DictWriter(writefile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    parsed_tweet = {}
                    parsed_tweet['Date'] = row['Date']
                    parsed_tweet['Tweet'] = row['Tweet']
                    parsed_tweet['Sentiment'], parsed_tweet['Score'] = self.get_sentiment_twitter(row['Tweet'], classifier=classifier)
                    row['Sentiment'] = parsed_tweet['Sentiment']
                    row['Score'] = parsed_tweet['Score']
                    #print(parsed_tweet)
                    writer.writerow(row)
                    tweets.append(parsed_tweet)
            readfile.close()
        writefile.close()

        os.remove(filename)
        os.rename(tempfile, filename)
        return tweets


    def filter_tweets_fromfile_by_date(self, filename, start_date, end_date):

        tweets = []
        with open(filename, newline='') as readfile:
            reader = csv.DictReader(readfile)
            for row in reader:
                row_date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
                if row_date >= start_date and row_date <= end_date:
                    tweets.append(row)
            readfile.close()
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


def calculate_sentiment_numbers(tweets, title=None):
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
    print("Total Tweets legth ", len(tot_tweets))
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tot_tweets)))
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tot_tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(
        100 * (len(tot_tweets) - len(negative_tweets) - len(positive_tweets)) / len(tot_tweets)))

    return positive_tweets, negative_tweets, neutral_tweets
    # Plot the Graph...
    # plot_chart(positive_tweets, negative_tweets, tot_tweets, title)

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

def trend_analysis (filename, start_date, end_date):
    print()


def main(filename, title, source=None, classifier=None):
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

    tempfile = 'temp_data.csv'

    if classifier=='1':
        print("Default - Pattern Analyzer passed for processing.")
        title = title + " : Default Pattern Analyzer"
    elif classifier=='2':
        print("Default - Naive Bayes Analyzer passed for processing.")
        title = title + " : Default Naive Bayes Analyzer"
    elif classifier=='3':
        print("Custom Classifier restored from file. Passed for analysis")
        title = title + " : Custom NB Classifier"


    tweets = twitter_api.analyze_sentiments(filename, tempfile, classifier=classifier)
    positive_tweets, negative_tweets, neutral_tweets = calculate_sentiment_numbers(tweets, title)
    print("Plotting Chart")
    plot_chart(positive_tweets, negative_tweets, (positive_tweets + negative_tweets + neutral_tweets), title)

if __name__ == "__main__":
    # Call the main function. If calling this from same file, we pass source = 'I'
    main(filename='Tweets_Amex.csv', title='Sentiments Analysis in Twitter - American Express', source='I')
