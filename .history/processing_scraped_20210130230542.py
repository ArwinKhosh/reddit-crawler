#processing the scraped json
import json
import pandas

#the name of the file. This should be linked with 
myfile = 'data/dummy.json'

import json

with open(myfile) as f:
  data = json.load(f)
# read the file
# keep the craeted_utc, 
#build a matrix with existing timestamps as columns