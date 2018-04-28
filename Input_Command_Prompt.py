import datetime
from colorama import init, Fore, Back, Style
from termcolor import colored
from CAP5771.Project import Load_Tweets_Batch
from CAP5771.Project import Sentiment_Analysis_Twitter
from CAP5771.Project import Trend_Analysis_Tweets
from CAP5771.Project import Get_Company_Configuration


# Initializing the variables.
operation = '0'
now = datetime.datetime.now()
from_date = now - (datetime.timedelta(days=1))
to_date, from_date = str(now.date()), str(from_date.date())
companyList, count = Get_Company_Configuration.getCompanyDetailsList()    # Read from configuration file and get company names and number dynamically.


while (operation != 'E'):
    #print(Style.BRIGHT + Fore.BLUE);print(Style.RESET_ALL)
    print("\n\nSelect options from below menu: (To exit, type E)-------- ")
    if (operation == 'E'):
        print("Exiting the Menu. Bye...")
        break

    print("Select an Operation: (1) Twitter: Analyze Sentiments  (2) Load Tweets (On-demand)  (3) Sentiment Trends (4) Purge Old data/tweets.")
    operation = input("To select, type  1  2  3  or 4 : \n")

    print("Select company for the operation:")         # Loop and update company name at run time.
    company_choice = ""
    for n in range(count):
        company_choice = company_choice + str(n+1) + ") " + companyList[n+1]["name"] + "   "
    company_choice = company_choice + str(count+2) + ") " + "All of them  "
    print(company_choice)
    company = input("Select your options, enter the number (1  2  3 so on):\n")  # Select options for company name
    company = int(company)  # Convert this to compare with number

    # For (1) Twitter: Analyze Sentiments:
    if  operation == '1' and company < (count+2):
        filename, title = companyList[int(company)]["twitter_data_file"], companyList[int(company)]["sentiment_title"]
        Sentiment_Analysis_Twitter.main(filename=filename, title=title)
    if  operation == '1' and company == (count+2):
        for n in range(count):
            filename, title = companyList[n+1]["twitter_data_file"], companyList[n+1]["sentiment_title"]
            Sentiment_Analysis_Twitter.main(filename=filename, title=title)


    # For (2) Load Tweets (On-demand)
    if  operation == '2':
        print("Select (1) To load today's tweets  (2) To load tweets from custom date")
        load_option = input("To select, type  1  or 2 : \n")
        if (load_option == '2'):
            from_date = input("Load tweets: Input, From date (in YYYY-MM-DD): \n")
            to_date = input("Load tweets: Input, To date   (in YYYY-MM-DD): \n")

        if company < (count+2):
            filename, query = companyList[int(company)]["twitter_data_file"], companyList[int(company)]["keys"]
            Load_Tweets_Batch.main(operation='2', query=query, filename=filename, start_date=to_date, since_date=from_date)
        else:
            for n in range(count):
                filename, query = companyList[n+1]["twitter_data_file"], companyList[n+1]["keys"]
                Load_Tweets_Batch.main(operation='2', query=query, filename=filename, start_date=to_date, since_date=from_date)


    # For (3) Sentiment Trends

    if operation == '3':
        print("Select (1) See trends from last 24 hrs  (2) See trends from custom date")
        trend_option = input("To select, type  1  or 2 : \n")
        twitter_data_file, twitter_trend_file, title = companyList[int(company)]["twitter_data_file"], companyList[int(company)]["twitter_trend_file"], companyList[int(company)]["trend_title"]
        if (trend_option == '2'):
            from_date = input("Sentiments Trend: Input, From date (in YYYY-MM-DD): \n")
            to_date = input("Sentiments Trend: Input, To date   (in YYYY-MM-DD): \n")

        if company < (count + 2):
            Trend_Analysis_Tweets.sort_data_by_dates(twitter_data_file)
            Trend_Analysis_Tweets.collect_data_for_trendReporting(twitter_data_file, twitter_trend_file, from_date, to_date)
            Trend_Analysis_Tweets.display_trends(twitter_data_file, twitter_trend_file, title)
        else:
            for n in range(count):
                twitter_data_file, twitter_trend_file, title = companyList[n+1]["twitter_data_file"], companyList[n+1]["twitter_trend_file"], companyList[n+1]["trend_title"]
                Trend_Analysis_Tweets.sort_data_by_dates(twitter_data_file)
                Trend_Analysis_Tweets.collect_data_for_trendReporting(twitter_data_file, twitter_trend_file, from_date, to_date)
                Trend_Analysis_Tweets.display_trends(twitter_data_file, twitter_trend_file, title)


    # For (4) Purge Old data/tweets.

    if operation == '4':
        print("Select (1) Purge data from last 24 hrs  (2) Purge data from custom date")
        purge_option = input("To select, type  1  or 2 : \n")
        if (purge_option == '2'):
            from_date = input("Purge data: Input, From date (in YYYY-MM-DD): \n")
            to_date = input("Purge data: Input, To date   (in YYYY-MM-DD): \n")
            twitter_data_file = companyList[int(company)]["twitter_data_file"]

        if company < (count + 2):
            Load_Tweets_Batch.main(operation='4', filename=twitter_data_file, purge_date_from=from_date, purge_date_to=to_date)
        else:
            for n in range(count):
                twitter_data_file = companyList[n+1]["twitter_data_file"]
                Load_Tweets_Batch.main(operation='4', filename=twitter_data_file, purge_date_from=from_date, purge_date_to=to_date)








