#processing the scraped json
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt

##Pre - processing

#download the list (just do it once)               ####
#nltk.download('stopwords')

stopwords = stopwords.words('english')

#here to always update the list of stopwords
#stopwords = stopwords + ....

#capitalize the list
capital_stopwords = [k.capitalize() for k in stopwords]

#add it to the original list
stopwords = stopwords + capital_stopwords

#to quickly test if a word is not a stop word, use a set:
stop_word_set = set(stopwords)

##Processing

#the name of the file. This will be changed with a list of filenames, once they are all downloaded 
words_file = 'words_dictionary.json'

# read the file
with open(words_file) as f:
  words = json.load(f)

#something

filtered_words = [k for k in word_list if k not in stop_word_set]

#simple word frequency
counter_obj = Counter(filtered_words)
count = counter_obj.most_common(len(counter_obj))
