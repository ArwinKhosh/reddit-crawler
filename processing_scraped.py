#processing the scraped json
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt

#TODO check performance of list vs dictionary value lookup

##Pre - processing

sp500 = pd.read_csv('tickers/sp500.csv',header =0, delimiter=',',index_col=False)
nyse = pd.read_csv('tickers/nyse.csv',header =0, delimiter=',',index_col=False)
amex = pd.read_csv('tickers/amex.csv',header =0, delimiter=',',index_col=False)
nasdaq = pd.read_csv('tickers/nasdaq.csv',header =0, delimiter=',',index_col=False)

#put them into one dataframe
stocks = pd.DataFrame(pd.concat([sp500['Symbol'],nasdaq['Symbol'],amex['Symbol'],nyse['Symbol']], axis=0))
stocks.reset_index(inplace=True)

#turn it into a list 
tickers =stocks['Symbol'].tolist()

#remove duplicates
tickers = set(tickers)

#filter out those who are same stock but Class A,B or C
ss = [x for x in tickers if not "^" in x]

#sort them
tickers = sorted(ss)

#the name of the file with english language words
words_file = 'words_dictionary.json'

# read the file
with open(words_file) as f:
  words = json.load(f)

#capitalize the list
capital_stopwords = [k.capitalize() for k in stopwords]

#add it to the original list
stopwords = stopwords + capital_stopwords

#to quickly test if a word is not a stop word, use a set:
stop_word_set = set(stopwords)

##Processing

filtered_words = [k for k in word_list if k not in stop_word_set]

#simple word frequency
counter_obj = Counter(filtered_words)
count = counter_obj.most_common(len(counter_obj))
