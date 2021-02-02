import requests
import json
import re
import time

# TODO
# Understant why changing params to asc makes it work, desc just do one loop
# Need to use id, not time, when fetching new interval of comments.
# Ids are uniqe and is just an incrementing int in base 36. but comments
# can be posted at the same time so not good. 

# Docs: 
# https://www.reddit.com/r/pushshift/comments/8m50un/how_does_pushshift_update_submissions_and/
# https://github.com/pushshift/api  # This seems to be not up to date, but useful
# https://www.osrsbox.com/blog/2019/03/18/watercooler-scraping-an-entire-subreddit-2007scape//


PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"

def fetchObjects(**kwargs):
    # Default paramaters for API query
    params = {
        "sort_type":"created_utc",
        "sort":"asc", # desc gives news first
        "size":1000, # apperantly the max size has been limited to 100 past year
        "fields": ["created_utc","body","id","score","subreddit"] 
        }

    # Add additional paramters based on function arguments
    for key,value in kwargs.items():
        params[key] = value

    # Print API query paramaters
    print(params)

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
        response = json.loads(r.text)
        data = response['data']
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'],36)) # this default to asc order. SO oldest post first
        return sorted_data_by_id

def extract_reddit_data(**kwargs):
    # Speficify the start timestamp

    t_epoch = time.time()
    # 1 week  back. Right now this gives two weeks for some reason
    oldest_created_utc = int(t_epoch) - 50*3600 #1604800

    # DOn'tknow what this is
    max_id = 0

    # Open a file for JSON output
    file = open("submissions.json","a")

    # While loop for recursive function
    while 1:
        nothing_processed = True
        # Call the recursive function. Because of sorted in other function date
        # is oldest to newest
        objects = fetchObjects(**kwargs,after=oldest_created_utc)
        
        # Loop the returned data (max 100), ordered by date (new to old)
        for object in objects:
            id = int(object['id'],36)
            if id > max_id:
                nothing_processed = False
                created_utc = object['created_utc']
                max_id = id
                if created_utc > oldest_created_utc: oldest_created_utc = created_utc
                # Output JSON data to the opened file
                print(json.dumps(object,sort_keys=True,ensure_ascii=True),file=file)
        
        # Exit if nothing happened
        if nothing_processed: return
        # The newest time of the returned results will for the next request
        # be used as the input for request. 
        oldest_created_utc -= 1

        # Sleep a little before the next recursive function call
        time.sleep(.5)

# Start program by calling function with:
# 1) Subreddit specified
# 2) The type of data required (comment or submission)
extract_reddit_data(subreddit="europe",type="comment")