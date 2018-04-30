import csv
import datetime
import matplotlib.pyplot as plt
from CAP5771.Project import Sentiment_Analysis_Twitter as sa


# Sort data
def sort_data_by_dates(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sortedlist = sorted(reader, key=lambda row: (row['Date']), reverse=False)
    csvfile.close()

    # Write sorted list back into file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)
    csvfile.close()


# Write a new document for trend analysis. Pull data from main file.
def collect_data_for_trendReporting(filename, filename_temp, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    with open(filename_temp, 'w', newline='') as writefile:  # Open in append mode to append data.
        fieldnames = ['Date', 'Tweet', 'Sentiment', 'Score']
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        with open(filename, newline='') as readfile:
            reader = csv.DictReader(readfile)
            for row in reader:
                row_date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
                if row_date >= start_date and row_date <= end_date:
                    row_add = row
                    writer.writerow(row_add)
        readfile.close()
    writefile.close()


# Sort data based on dates
def display_trends(masterfile, trendfile, title):
    with open(masterfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sortedlist = sorted(reader, key=lambda row: (row['Date']), reverse=False)
    csvfile.close()
    print("Sorting Done")
    min_date, max_date = (sortedlist[0])['Date'], sortedlist[len(sortedlist) - 1]['Date']
    print("Min Date: ", (sortedlist[0])['Date'] + "  Max Date:  ", sortedlist[len(sortedlist) - 1]['Date'])
    diff = datetime.datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(min_date,'%Y-%m-%d %H:%M:%S')
    duration = diff.total_seconds()
    split_by = "n"
    split_durations, pos_trend, neg_trend = [], [], []
    duration_in_days = duration / (60 * 60 * 24)
    duration_in_hours = duration / (60 * 60)
    duration_in_minutes = duration / (60)
    duration_in_secs = duration


    if duration < 0:
        print("Incorrect values: Start Date can't be later than To Date")
        split_by = 'n'
    elif duration_in_hours >= 240:
        split_by = 'd'
    else:
        split_by = 'h'

    split_diff = duration_in_hours / 10
    next_time_end = datetime.datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S')
    split_durations.append(next_time_end)
    print("Time difference in each split: ", split_diff)

    for n in range(10):
        next_time_end = next_time_end + datetime.timedelta(hours=split_diff)
        split_durations.append(next_time_end)

    sat = sa.TwitterClient()  # Calculate from total
    tweets = sat.analyze_sentiments(filename=masterfile, tempfile=trendfile.strip('.csv') + '_temp.csv')
    positive_tweets_initial, negative_tweets_initial, neutral_tweets_initial = sa.calculate_sentiment_numbers(tweets)
    positive_per_initial = 100 * len(positive_tweets_initial) / (len(positive_tweets_initial) + len(negative_tweets_initial) + len(neutral_tweets_initial))
    negative_per_initial = 100 * len(negative_tweets_initial) / (len(positive_tweets_initial) + len(negative_tweets_initial) + len(neutral_tweets_initial))
    pos_trend.append(positive_per_initial)
    neg_trend.append(negative_per_initial)

    # Calculate for the time period now
    sat.analyze_sentiments(filename=trendfile, tempfile=trendfile.strip('.csv') + '_temp.csv')

    for n in range(10):
        tweets = sat.filter_tweets_fromfile_by_date(filename=trendfile, start_date=split_durations[n], end_date=split_durations[n + 1])
        if not tweets:
            pos_trend.append(positive_per_initial)
            neg_trend.append(negative_per_initial)

        else:
            positive_tweets, negative_tweets, neutral_tweets = sa.calculate_sentiment_numbers(tweets)
            positive_adj_len = len(positive_tweets) + len(positive_tweets_initial)
            negative_adj_len = len(negative_tweets) + len(negative_tweets_initial)
            total_adj_len = positive_adj_len + negative_adj_len + len(neutral_tweets) + len(neutral_tweets_initial)

            positive_per = 100 * positive_adj_len / total_adj_len
            negative_per = 100 * negative_adj_len / total_adj_len
            pos_trend.append(positive_per)
            neg_trend.append(negative_per)


    #Convert split_durations based on hours or days to limit the display
    split_durations_simplefied = []
    for row in split_durations:

        if split_by == 'h':
            split_durations_simplefied.append(str(row.day) + " " + str(row.hour) + ":" + str(row.minute))
        if split_by == 'd':
            split_durations_simplefied.append(str(row.month) + "-" + str(row.day))

    plt.plot(split_durations_simplefied, pos_trend, color='g')
    #plt.figure(figsize=(20, 10))
    #plt.axis([split_durations[0], split_durations[10], 75, 80])
    plt.xlabel('Time period')
    plt.ylabel('Positive Sentiment Trends in Percentage')
    plt.title(title)
    plt.show()

    # Plot negative trend
    '''
    plt.plot(split_durations, neg_trend, color='orange')
    plt.xlabel('Time period')
    plt.ylabel('Negative Sentiment Trends in Percentage')
    plt.title('Twitter Sentiments Trend for the given time period')
    plt.show()
    '''

