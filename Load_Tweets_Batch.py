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
        tw_access_token = 'xxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxx'
        tw_access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        tw_consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        tw_consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'

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
                print(since_date, start_date)
            for tweet in tweepy.Cursor(self.twitter_api.search, q=query, since=since_date, until=start_date, lang="en").items():
                writer.writerow({'Date': tweet.created_at, 'Tweet': ((tweet.text.strip()).encode('utf-8')), 'Sentiment': '', 'Score': ''})
                #print(tweet.user.name + "   " + ((tweet.text.strip()).encode('utf-8')).decode())
        csvfile.close()


        with open(filename, newline='') as csvfile:
            print("Printing first few tweets...")
            reader = csv.DictReader(csvfile); n=0
            for row in reader:
                if n < 10:
                    print(((row['Tweet']).encode()).decode('utf-8'))
                    n = n+1;
        csvfile.close()


def purge_tweets(filename, from_date, to_date):
    from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()

    with open(filename.strip('.csv') + '_temp.csv', 'w', newline='') as tempfile:
        fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(filename, newline='') as readfile:
            reader = csv.DictReader(readfile)
            for row in reader:
                row_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S").date()
                if (row_date < from_date and row_date > to_date):
                    writer.writerow({'Date': row['Date'], 'Tweet': row['Tweet'], 'Sentiment': row['Sentiment'], 'Score': row['Score']})
        readfile.close()
    tempfile.close()
    os.rename(filename, filename.strip('.csv') + '_data_backup_' + str(datetime.datetime.now().date()) + ".csv")
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


def main(operation, query=None, filename=None, start_date=None, since_date=None, purge_date_from=None, purge_date_to=None):
    # TwitterClient Object
    twitter_api = Load_Tweets_Batch()
    if (operation == '2'):
        query_list = query.split(',')
        for row in query_list:
            query_st = row.strip(' \t\n\r')
            print("Getting fresh tweets for  ", query_st + "  between  " + since_date + "  and  " + start_date)
            twitter_api.get_online_tweets(query_st, filename, start_date, since_date)
    elif (operation == '4'):
        purge_tweets(filename=filename, from_date = purge_date_from, to_date = purge_date_to)
        print("Purged data for ", query + " from " + purge_date_from + "  to  " + purge_date_to)
    else:
        print("No option..Try again")


if __name__ == "__main__":
    # Call the main function
    operation = input("Load/Purge Data ?  (Y/N): ") # Command line user input. Called if this file is executed independently.
    main(operation)
