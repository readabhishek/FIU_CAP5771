import os
import json
import csv
from builtins import print
import tweepy
import datetime
from tweepy import OAuthHandler


class Load_Tweets_Batch(object):

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
            self.twitter_api = tweepy.API(self.auth_twitter, wait_on_rate_limit=True)
            print("Successful Authentication ", self.twitter_api)
        except:
            print("Error: Authentication Failed")

    def get_online_tweets(self, query, filename, start_date, since_date):
        file_exists = False
        if os.path.isfile('./'+filename):
            file_exists = True

        with open(filename, 'a', newline='') as csvfile:  # Open in append mode to append data.
            fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            for tweet in tweepy.Cursor(self.twitter_api.search, q=query, since=since_date, until=start_date, lang="en").items():
                writer.writerow({'Date': tweet.created_at, 'Tweet': ((tweet.text.strip()).encode('utf-8')), 'Sentiment': '', 'Score': ''})

        csvfile.close()

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(((row['Tweet']).encode()).decode('utf-8'))
        csvfile.close()


def purge_tweets(filename, purge_date, end_date):
    purge_date = datetime.datetime.strptime(purge_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    with open(filename.strip('.csv') + '_temp.csv', 'w', newline='') as tempfile:
        fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(filename, newline='') as readfile:
            reader = csv.DictReader(readfile)
            for row in reader:
                row_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S").date()
                if (row_date != purge_date):
                    writer.writerow({'Date': row['Date'], 'Tweet': row['Tweet'], 'Sentiment': row['Sentiment'], 'Score': row['Score']})
        readfile.close()
    tempfile.close()
    os.remove(filename)
    os.rename(filename.strip('.csv') + '_temp.csv', filename)


def load_JSON_file(filename, entity):
    query = [];
    data = json.load(open(filename))
    raw_keys = data[entity]["keys"].split(",")
    title = data[entity]["title"].split(",")
    for keys in raw_keys:
        query.append(keys.strip(' \t\n\r'))
    return query, title


def test():
    print("Inside other file")


def main():
    # TwitterClient Object
    twitter_api = Load_Tweets_Batch()
    twitter_api.get_online_tweets('@AmericanExpress', 'Tweets_Amex.csv', '2018-04-23', '2018-04-22')
    #purge_tweets(filename='Tweets_Amex.csv', purge_date='2018-04-21', end_date='2018-04-21')


if __name__ == "__main__":
    # Call the main function
    main()
