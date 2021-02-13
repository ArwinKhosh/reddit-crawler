#processing the scraped json
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords


#the name of the file. This will be changed with a list of filenames, once they are all downloaded 
myfile = 'data/dummy.json'

# read the file
with open(myfile) as f:
  mydata = json.load(f)

title = mydata[0]

#get the content and the timestamp
#the short title
mytitle = title['data']['children'][0]['data']['title']

#the text, timestamp in the title
title_desc = title['data']['children'][0]['data']['selftext']
timestamp = title['data']['children'][0]['data']['created_utc']

#if it was edited, get that timestamp instead
edited = title['data']['children'][0]['data']['edited']

if len(str(edited)) > 5:
  timestamp = edited

#the dictionary holding stuff
mydict = dict()

#adding the first key:value pair - timestamp: all text combined
mydict[timestamp] = mytitle+' ' + title_desc

#first do some filtering using nltk of the most common english stopwords

#stop words from EN
nltk.download('stopwords')
stop_word_list = stopwords.words('english')

#  to quickly test if a word is not a stop word, use a set:
stop_word_set = set(stop_word_list)

#for every word (in every timestamp - later), check whether it is a stopword or not
word_list = mydict[timestamp].split()

[k for k in word_list if k not in stop]
    
    if word.lower() in stop_word_set:
        
        #filter the list 

