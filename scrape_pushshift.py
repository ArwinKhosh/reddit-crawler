import requests
import time

from common.database import SQLiteConnection
from common.constants import DB_FILE, KEY_LST

# Utilityy functions
from common import util

# TODO:
#  - Understant why changing params to asc makes it work, desc just do one loop
#  - Ids are uniqe and is just an incrementing int in base 36. but comments
#    can be posted at the same time so not good. 
#  - API can sometimes return None, neen to handle that somehow, else, program
#    will crash. If running with Task Scheduler, maybe it doesn't matter?
#    Just create logger and message notification. 

#* Docs: 
# https://www.reddit.com/r/pushshift/comments/8m50un/how_does_pushshift_update_submissions_and/
# https://github.com/pushshift/api  # This seems to be not up to date, but useful
# https://www.osrsbox.com/blog/2019/03/18/watercooler-scraping-an-entire-subreddit-2007scape//


PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"

def fetch_comments(**kwargs):
    # Default paramaters for API query
    params = {
        "sort_type": "created_utc",
        "sort": "asc", # desc gives news first
        "size": 100, # apperantly the max size has been limited to 100 past year
        "fields": ["created_utc","id", "body", "subreddit", "score","author"] 
        }

    # Add additional parameters based on function arguments
    for key,value in kwargs.items():
        params[key] = value


    # Set the type variable based on function input
    # The type can be "comment" or "submission", default is "comment" 
    type = "comment"
    if 'type' in kwargs and kwargs['type'].lower() == "submission":
        type = "submission"
    
    # Perform an API request
    r = requests.get(PUSHSHIFT_REDDIT_URL + "/" + type + "/search/", params=params, timeout=30)

    # Check the status code, if successful, process the data. 200 OK, 404 Not found.
    # Docs: https://www.w3schools.com/python/ref_requests_response.asp
    if r.status_code == 200:
        response = r.json()
        data = response['data']
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'],36)) # this default to asc order. So oldest post first
        return sorted_data_by_id
    if r.status_code == 404:
        print('404')

def extract_reddit_data(**kwargs):

    # Database connection
    db_connector = SQLiteConnection(DB_FILE)
    db_connector.create_tables()
    latest_time_db = db_connector.get_latest_comment()

    if latest_time_db is None:
        latest_time =int(time.time()) - 86400  # (1 day) Later set to X amount of time from now
    else:
        latest_time = latest_time_db[0]

    total_fetched = 0
    
    # While loop for recursive function
    while True:
        nothing_processed = True

        # Returned comments (max 100), ordered by date (old to new) 
        # Returns a list of dictionaries.
        batch = fetch_comments(**kwargs,after=latest_time)
        
        if len(batch) > 0:

            # Insert a human readable date in each comment. 
            for comment in batch:
                comment.update( {"created_date": util.epoch_to_gmt(comment['created_utc'], format='datetime')})

            db_connector.insert_batch(batch, KEY_LST)
            nothing_processed = False
            total_fetched += len(batch)

            # Get most recent time.
            latest_time = max([item['created_utc'] for item in batch])  
                
        # Exit script if nothing happened.
        if nothing_processed: 
            print(f'Total amount of comments fetched: {total_fetched}') 
            return

        # Print API query time and open file.
        print('Retriev data after: ' + util.epoch_to_gmt(latest_time,format='datetime') \
             + '\tComments returned: ' + str(len(batch)) + '\tTotal: ' + str(total_fetched))

        # Sleep a little before the next recursive function call
        time.sleep(.5)


#------------------------------------------------------------------------------
# RUN PROGRAM FROM HERE
#------------------------------------------------------------------------------

# Start program by calling function with:
# 1) Subreddit specified
# 2) The type of data required (comment or submission)
extract_reddit_data(subreddit="wallstreetbets",type="comment")

#print(gmt_to_epoch("28-01-2021", 0, 0, 0, 1, -1))

