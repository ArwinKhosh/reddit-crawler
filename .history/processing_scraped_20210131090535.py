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

#the 
title_desc = 