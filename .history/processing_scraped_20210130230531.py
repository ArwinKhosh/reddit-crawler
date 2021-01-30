#processing the scraped json
import json
import pandas

#the name of the file. This should be linked with 
myfile = 'dummy.json'

import json

with open('path_to_file/person.json') as f:
  data = json.load(f)
# read the file
# keep the craeted_utc, 
#build a matrix with existing timestamps as columns