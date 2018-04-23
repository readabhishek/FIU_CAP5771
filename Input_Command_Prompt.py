
from CAP5771.Project.project_modules import Load_Tweets_Batch
from CAP5771.Project import Sentiment_Analysis_Twitter



operation = '0'

while (operation != 'E'):
    print("\n\nSelect options from below menu: (To exit, type E)-------- ")
    print("Select an operation: (A) Analyze Sentiment  (B) Load today's tweet  (C) Purge old data.")
    operation = input("Choose A  B or C : \n")
    print("Choose company: (A) American Express  (B) Chase   (C) Capital One. ")
    company = input("Type A  B or C :\n")


    if (operation == 'E'):
        print("Ok no update.. Exiting the program. Bye...")
    elif (operation == 'A' and company == 'A'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_Amex.csv', title='Sentiments Analysis in Twitter - American Express')
    elif (operation == 'A' and company == 'B'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_Chase.csv', title='Sentiments Analysis in Twitter - Chase Bank')
    elif (operation == 'A' and company == 'C'):
        Sentiment_Analysis_Twitter.main(filename='Tweets_CapOne.csv', title='Sentiments Analysis in Twitter - Capital One Bank')

    elif (operation == 'B' and company == 'A'):
        Load_Tweets_Batch.main(operation='B', query='@AmericanExpress', filename='Tweets_Amex.csv', start_date='2018-04-23', since_date='2018-04-22')
    elif (operation == 'B' and company == 'B'):
        Load_Tweets_Batch.main(operation='B', query='@Chase', filename='Tweets_Chase.csv', start_date='2018-04-23', since_date='2018-04-22')
    elif (operation == 'B' and company == 'C'):
        Load_Tweets_Batch.main(operation='B', query='@CapitalOne', filename='Tweets_CapOne.csv', start_date='2018-04-23', since_date='2018-04-22')

    elif (operation == 'C' and company == 'A'):
        Load_Tweets_Batch.main(operation='C',query='@AmericanExpress', filename='Tweets_Amex.csv', purge_date_from ='2018-04-23', purge_date_to ='2018-04-22')
    elif (operation == 'C' and company == 'B'):
        Load_Tweets_Batch.main(operation='C',query='@Chase', filename='Tweets_Chase.csv', purge_date_from ='2018-04-23', purge_date_to ='2018-04-22')
    elif (operation == 'C' and company == 'C'):
        Load_Tweets_Batch.main(operation='C',query='@CapitalOne', filename='Tweets_CapOne.csv', purge_date_from ='2018-04-23', purge_date_to ='2018-04-22')
