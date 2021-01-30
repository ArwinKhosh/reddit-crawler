#processing the scraped json
import json
import pandas

#the name of the file. This will be changed with a list of filenames, once they are all downloaded 
myfile = 'data/dummy.json'

# read the file
with open(myfile) as f:
  data = json.load(f)

print('stop')
# keep the craeted_utc, 
#build a matrix with existing timestamps as columns