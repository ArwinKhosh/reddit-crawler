#processing the scraped json
import json
import pandas

#the name of the file. This will be changed with a list of filenames, once they are all downloaded 
myfile = 'data/dummy.json'

# read the file
with open(myfile) as f:
  mydata = json.load(f)

title = data[0]

#get the content and the timestamp

title['data']['children']['data']