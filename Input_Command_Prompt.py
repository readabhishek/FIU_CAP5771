import datetime
from CAP5771.Project import Load_Tweets_Batch
from CAP5771.Project import Sentiment_Analysis_Twitter
from CAP5771.Project import Trend_Analysis_Tweets


operation = '0'

while (operation != 'E'):
    print("\n\nSelect options from below menu: (To exit, type E)-------- ")
    print("Select an operation: (1) Analyze sentiment  (2) Load tweets from yesterday  (3) Watch the sentiments trend (4) Purge old data.")
    operation = input("To select, type  1  2  3  or 4 : \n")
    print("Select company for the operation: (1) American Express  (2) Chase   (3) Capital One. ")
    company = input("To select, type 1  2 or 3 :\n")

    now = datetime.datetime.now()
    from_date = now - (datetime.timedelta(days=1))
    to_date, from_date = str(now.date()), str(from_date.date())

    if (operation == '4'):
        print("Select (1) To purge yesterday/'s data  (2) To purge data for custom date")
        purge_option = input("To select, type  1  or 2 : \n")
        if (purge_option == '2'):
            from_date = input("Data purge: Input, From date : \n")
            to_date = input("Data purge: Input, To date : \n")
            # Here call - Purge function.



    if (operation == 'E'):
        print("Ok no update.. Exiting the program. Bye...")

    elif (operation == '1' and company == '1'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_Amex.csv', title='Sentiments Analysis in Twitter - American Express')
    elif (operation == '1' and company == '2'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_Chase.csv', title='Sentiments Analysis in Twitter - Chase Bank')
    elif (operation == '1' and company == '3'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_CapOne.csv', title='Sentiments Analysis in Twitter - Capital One Bank')


    elif (operation == '2' and company == '1'):
        Load_Tweets_Batch.main(operation ='2', query='@AmericanExpress', filename='Tweets_Amex.csv', start_date=to_date, since_date=from_date)
    elif (operation == '2' and company == '2'):
        Load_Tweets_Batch.main(operation='B', query='@Chase', filename='Tweets_Chase.csv', start_date=to_date, since_date=from_date)
    elif (operation == '2' and company == '3'):
        Load_Tweets_Batch.main(operation = '2', query='@CapitalOne', filename='Tweets_CapOne.csv', start_date=to_date, since_date=from_date)

    elif (operation == '3' and company == '1'):
        Trend_Analysis_Tweets.sort_data_by_dates("Tweets_Amex.csv");
        Trend_Analysis_Tweets.collect_data_for_trendReporting("Tweets_Amex.csv", "Tweets_Amex_for_Trend.csv", from_date, to_date)
        Trend_Analysis_Tweets.display_trends("Tweets_Amex.csv", "Tweets_Amex_for_Trend.csv")

    elif (operation == '3' and company == '2'):
        Trend_Analysis_Tweets.sort_data_by_dates("Tweets_Chase.csv");
        Trend_Analysis_Tweets.collect_data_for_trendReporting("Tweets_Chase.csv", "Tweets_Chase_for_Trend.csv", from_date, to_date)
        Trend_Analysis_Tweets.display_trends("Tweets_Chase.csv", "Tweets_Chase_for_Trend.csv")

    elif (operation == '3' and company == '3'):
        Trend_Analysis_Tweets.sort_data_by_dates("Tweets_CapOne.csv");
        Trend_Analysis_Tweets.collect_data_for_trendReporting("Tweets_CapOne.csv", "Tweets_CapOne_for_Trend.csv", from_date, to_date)
        Trend_Analysis_Tweets.display_trends("Tweets_CapOne.csv", "Tweets_CapOne_for_Trend.csv")

    elif (operation == '4' and company == '1'):
        Load_Tweets_Batch.main(operation = '4',query='@AmericanExpress', filename='Tweets_Amex.csv', purge_date_from = from_date, purge_date_to = to_date)
    elif (operation == '4' and company == '2'):
        Load_Tweets_Batch.main(operation = '4',query='@Chase', filename='Tweets_Chase.csv', purge_date_from = from_date, purge_date_to = to_date)
    elif (operation == '4' and company == '3'):
        Load_Tweets_Batch.main(operation = '4',query='@CapitalOne', filename='Tweets_CapOne.csv', purge_date_from = from_date, purge_date_to = to_date)
