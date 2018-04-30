import re
import os
import csv
import json
import math


def preProcess_tweet(tweet):
    # Utility function to clean tweet text by removing links, special characters using simple regex statements.
    # print(tweet)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                "
               "| (\w +:\ / \ / \S +)", " ", tweet).split())

def PreProcess_training_dataset(filename, headerName_text, headerName_opinion):
    filename_temp = filename.strip('.csv') + '_temp.csv'
    with open(filename_temp, 'a', newline='', encoding='utf8') as writefile:
        fieldnames = ['Text', 'Sentiment']
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        with open(filename, newline='', encoding='utf8') as readfile:
            reader = csv.DictReader(readfile)
            for row in reader:
                parsed_tweet = {}
                str = (preProcess_tweet(row[headerName_text]))
                parsed_tweet['Text'] = str.strip()
                parsed_tweet['Sentiment'] = row[headerName_opinion]
                writer.writerow(parsed_tweet)
        readfile.close()
    writefile.close()



def SetFormatInJSON1(fromfile, jsonfile):
    current_line = 1
    num_lines = sum(1 for line in open(fromfile, encoding='utf8'))
    # num_lines = 1000
    start_split = 1
    split = math.ceil(num_lines / 2)
    end_split = start_split + split;
    for i in range(0, 10):

        if end_split >= num_lines + split + 1:
            break
        for j in range(start_split, end_split):
            if (j <= num_lines):
                n=0
                i=i+1
                jsonfile1 = jsonfile.strip('.json') + str(i)+".json"
                with open(jsonfile1, 'w', newline='') as outfile:
                    with open(fromfile, newline='', encoding='utf8') as readfile:
                        k=0
                        prev, last = None, None
                        reader = csv.DictReader(readfile)
                        outfile.write("[")
                        print("Inside 2")
                        for row in reader:
                            n=n+1
                            prev = last
                            last = row
                            if (n>=start_split and n<=end_split):
                                if k > 1:
                                    row_jason = {}
                                    row_jason["text"] = prev["Text"]
                                    if prev["Sentiment"] == '1':
                                        row_jason["label"] = "pos"

                                    if prev["Sentiment"] == '0':
                                        row_jason["label"] = "neg"

                                    str1 = json.dumps(row_jason)
                                    outfile.write(str1 + ",")
                            k = k + 1
                    row_jason = {}

                    row_jason["text"] = last["Text"]
                    if last["Sentiment"] == '1':
                        row_jason["label"] = "pos"

                    if last["Sentiment"] == '0':
                        row_jason["label"] = "neg"

                    str1 = json.dumps(row_jason)
                    outfile.write(str1)
                    outfile.write("]")

            start_split = end_split;
            end_split = end_split + split
        readfile.close()
        outfile.close()



def GetTrainTuple(filename, start, end):   # Function to format the training tuple to be fed into classifier
    train = []
    with open(filename, newline='', encoding='utf8') as readfile:

        reader = csv.DictReader(readfile)

        for row in reader:
            if start >= end:
                break
            text =""
            label = ""
            text = row["Text"]
            if row["Sentiment"] == '1':
               label = "pos"
            if row["Sentiment"] == '0':
                label = "neg"
            str1 = text + "," + label
            tup = (text, label)
            train.append(tuple(tup))
            start = start + 1
    readfile.close()
    return train




def SetFormatInJSON(fromfile, jsonfile):

    with open(jsonfile, 'w', newline='') as outfile:

            with open(fromfile, newline='', encoding='utf8') as readfile:
                i=0
                print("Inside 1")
                prev, last = None, None
                reader = csv.DictReader(readfile)
                outfile.write("[")
                print("Inside 2")
                for row in reader:
                    prev = last
                    last = row
                    if i>1:
                        row_jason = {}
                        label = ""
                        row_jason["text"] = prev["Text"]
                        if prev["Sentiment"] == '1':
                            row_jason["label"] = "pos"


                        if prev["Sentiment"] == '0':
                            row_jason["label"] = "neg"

                        str1 = json.dumps(row_jason)
                        outfile.write(str1 + ",")


                    i = i+1
            row_jason = {}

            row_jason["text"] = last["Text"]
            if last["Sentiment"] == '1':
                row_jason["label"] = "pos"

            if last["Sentiment"] == '0':
                row_jason["label"] = "neg"

            str1 = json.dumps(row_jason)
            outfile.write(str1)
            outfile.write("]")
    outfile.close()



#PreProcess_training_dataset('Sentiment Analysis Dataset.csv', 'SentimentText', 'Sentiment')
#st = os.path.getsize('Sentiment Analysis Dataset_temp.csv') / (1024*1024)  # Get size of file in MB
#SetFormatInJSON('Sentiment Analysis Dataset_temp.csv', 'Sentiment Analysis Dataset.json')

#SetFormatInJSON1('Sentiment Analysis Dataset_temp.csv', 'Sentiment Analysis Dataset.json')

#setTrainingData('Sentiment Analysis Dataset1_train.csv')
GetTrainTuple('Sentiment Analysis Dataset_temp.csv', 1, 60000)