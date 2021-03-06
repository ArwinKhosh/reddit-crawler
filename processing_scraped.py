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
import seaborn as sns

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
#stopwords = stopwords + capital_stopwords

#turning it into a set for better performance
stop_word_set = set(stopwords)

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
counts = 0
################################################################################################
check = False
while start<df.loc[len(df)-1,'time']:

  #slice it
  df_sliced = df[(df.time>start) & (df.time<start+ datetime.timedelta(minutes=5))]
  df_sliced.reset_index(inplace=True)

  #transform it to a list
  text_chunk = df_sliced['body'].to_list()
  
  #get individual words
  text_chunk2 = [x.split(' ') for x in text_chunk]
  
  #flatten
  text_chunk = [a for x in text_chunk2 for a in x]

  #filter for tickers
  filtered_tickers = [k for k in text_chunk if k in tickers]

  #simple ticker frequency per given timeframe
  counter_obj = Counter(filtered_tickers)
  count = counter_obj.most_common(len(counter_obj))

  #turn the tuple into a series and rename it with the timestamp
  a = pd.DataFrame(count).set_index(0)[1]
  a.name = start

  #if second round, then the series gets joined df
  if check == True:

    #results_df = results_df.merge(a,how= 'outer')
    results_df = results_df.join(a, how='outer')

  #if the first time, series is the dataframe
  else:
    results_df = pd.DataFrame(a)
    check =True
  
  #move the start to the end of the current sliced block
  start = df_sliced.loc[len(df_sliced)-1,'time']

  counts = counts + len(df_sliced)

#once it's complete, turn NANs into 0s and cast to int
results_df = results_df.fillna(0)
results_df.astype(int)

results_df = results_df.cumsum(axis=1)
results_df.to_excel('results/freq5min.xls')

fig = results_df.T.plot()
fig.legend(bbox_to_anchor=[1.05, 0.05], loc='right')
plt.show()
plt.savefig('results/trends.jpg')