#processing the scraped json
import json
import pandas as pd
import time
from collections import Counter
import matplotlib.pyplot as plt
from common.database import SQLiteConnection
from common.constants import DB_FILE
from common.util import epoch_to_gmt
import datetime

#TODO check performance of list vs dictionary value lookup

##Pre - processing

#reading comments 
db_connector = SQLiteConnection(DB_FILE)
df = db_connector.read_db_into_pandas()


#convert to datetime
ttime = df['created_utc']

cur_time = [epoch_to_gmt(elem,format = 'datetime') for elem in ttime]

start = cur_time[0]

df['time'] = cur_time

df.set_index('time',inplace=True)

while start<cur_time[len(ttime)-1]:

  sliced = df['body'].iloc[datetime(start),datetime(start) + datetime.timedelta('5minutes')]
  start = cur_time+300
  text_chunk = sliced.to_list()


#slicing every 5 minutes = 300 sec
cur_time= time[0]
while cur_time<time[-1]:

  sliced = df['created_utc'].iloc[cur_time,cur_time + datetime.timedelta(minutes=5)]
  sliced = sliced.to_list() 

#reading ticker data and words that need to be filtered
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


#lump data for every 5 minutes = 300 sec


#the name of the file with english language words
words_file = 'words_dictionary.json'

# read the file with words you want to 
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
