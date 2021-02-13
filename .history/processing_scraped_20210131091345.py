#processing the scraped json
import json
import pandas

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

print('stop')

#the dictionary holding stuff
mydict = dict()
mydict[timestamp] = mytitle+' ' + title_desc