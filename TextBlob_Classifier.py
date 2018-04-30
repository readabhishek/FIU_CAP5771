import pickle
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier
from CAP5771.Project import PreProcess_Training_Dataset

'''
filename = 'Sentiment Analysis Dataset1.json'
with open(filename, 'r') as fp:
   cl = NaiveBayesClassifier(fp, format="json")
'''

test = [                                        # Sample test data
('the beer was good.', 'pos'),
('I do not enjoy my job', 'neg'),
("I ain't feeling dandy today.", 'neg'),
("I feel amazing!", 'pos'),
('Gary is a friend of mine.', 'pos'),
 ("I can't believe I'm doing this.", 'neg')
]

def train_data():
    start = 1; size = 500; end = start + size -1
    filename = 'Sentiment_Analysis_trained_model.sav'
    for n in range (1,2000):
        train = PreProcess_Training_Dataset.GetTrainTuple('Sentiment Analysis Dataset_temp.csv', start, end)
        if (start <= 1) :
            nbc_classifier = NaiveBayesClassifier(train)
            print("First time create new object")
            pickle.dump(nbc_classifier, open(filename, 'wb'))
        else:
            print("Training for next ", str(end))
            nbc_classifier = pickle.load(open(filename, 'rb'))
            nbc_classifier.update(train)
            pickle.dump(nbc_classifier, open(filename, 'wb'))
        start = end+1
        end = start + size -1

    print("Accuracy: ", nbc_classifier.accuracy(test))
    print(nbc_classifier.classify("I feel amazing!"))
    blob = TextBlob("The beer is good. But the hangover is horrible.", classifier=nbc_classifier)
    print("Custom", blob.sentiment.polarity)
    blob = TextBlob("The beer is good. But the hangover is horrible.", analyzer=NaiveBayesAnalyzer())
    print("NaiveBayesAnalyzer", blob.sentiment.classification)
    print("NaiveBayesAnalyzer", blob.sentiment)
    return nbc_classifier

def getnbc_classifier():
    filename = 'Sentiment_Analysis_trained_model.sav'
    nbc_classifier = pickle.load(open(filename, 'rb'))
    return  nbc_classifier



#train_data()

