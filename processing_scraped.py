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

#the name of the file with english language words
words_file = 'words_dictionary.json'

# read the file with words you want to 
with open(words_file) as f:
  stopwords = json.load(f)

#capitalize the list
capital_stopwords = [k.capitalize() for k in stopwords]

#add it to the original list
stopwords = stopwords + capital_stopwords

#turning it into a set for better performance
stop_word_set = set(stopwords)

##Processing

filtered_words = [k for k in word_list if k not in stop_word_set]

#reading comments 
db_connector = SQLiteConnection(DB_FILE)
df = db_connector.read_db_into_pandas()


#convert to datetime format
ttime = df['created_utc']

cur_time = [epoch_to_gmt(elem,format = 'datetime') for elem in ttime]
df['time'] = cur_time
#convert to datetime object type
df['time'] =pd.to_datetime(df['time'],format = '%Y-%m-%d-%H-%M-%S')

start = df.loc[0,'time']

#loop while we have not gone to the end of the dataframe
while start<df.index[-1]:

  df_sliced = df[(df.time>start) & (df.time<start+ datetime.timedelta(minutes=5))]
  start = df_sliced.loc[len(df_sliced)-1,'time']
  text_chunk = df_sliced['body'].to_list()




#simple word frequency
counter_obj = Counter(filtered_words)
count = counter_obj.most_common(len(counter_obj))
