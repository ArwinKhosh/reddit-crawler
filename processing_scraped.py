#processing the scraped json
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt


#TODO filter out the same-class stocks

##Pre - processing

sp500 = pd.read_csv('tickers/sp500',header =0, delimiter=',',index_col=False)
nyse = pd.read_csv('tickers/nyse',header =0, delimiter=',',index_col=False)
amex = pd.read_csv('tickers/amex',header =0, delimiter=',',index_col=False)
nasdaq = pd.read_csv('tickers/sp500',header =0, delimiter=',',index_col=False)

#put them into one
stocks = pd.concat([sp500,nasdaq,amex,nyse], axis=1)

#filter here the ones that are like this AAC^D
#

tickers = stocks['Symbol'].tolist()

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
