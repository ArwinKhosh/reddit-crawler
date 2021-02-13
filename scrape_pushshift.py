import requests
import json
import time

# Utilityy functions
from common import util



# TODO:
# Understant why changing params to asc makes it work, desc just do one loop
# I Fucked up! e.g a is b checks if their ids are the same. Need to go through
# and fix where I use that. DONE! All good
# Ids are uniqe and is just an incrementing int in base 36. but comments
# can be posted at the same time so not good. 

#* Docs: 
# https://www.reddit.com/r/pushshift/comments/8m50un/how_does_pushshift_update_submissions_and/
# https://github.com/pushshift/api  # This seems to be not up to date, but useful
# https://www.osrsbox.com/blog/2019/03/18/watercooler-scraping-an-entire-subreddit-2007scape//


PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"


def fetchObjects(**kwargs):
    # Default paramaters for API query
    params = {
        "sort_type":"created_utc",
        "sort":"asc", # desc gives news first
        "size":100, # apperantly the max size has been limited to 100 past year
        "fields": ["created_utc","id"] #, "body", "subreddit", "score"] 
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
    # Specify the start timestamp

    t_epoch = time.time()
    # 1 week  back. Right now this gives two weeks for some reason
    oldest_created_utc = 1612130836 #  31 January 2021 22:07:00'
    oldest_created_utc_date = util.epoch_to_gmt(oldest_created_utc)


    days_exist = util.exist_date(oldest_created_utc_date)

    # Create new start time if date 
    while oldest_created_utc_date in days_exist:
         oldest_created_utc = util.increment_time(oldest_created_utc,1,0,0,0)
         oldest_created_utc_date = util.epoch_to_gmt(oldest_created_utc)


    max_id = 0

    # Open a file for JSON output
    file = open(f"data/comments_by_date/{oldest_created_utc_date}.json","a")

    # While loop for recursive function
    while 1:
        nothing_processed = True
        # Call the recursive function. Because of sorted in other function date
        # is oldest to newest
        objects = fetchObjects(**kwargs,after=oldest_created_utc)

        # Print API query time and open file
        print('Retriev data from after: ' + util.epoch_to_gmt(oldest_created_utc,format='datetime') + '\tOpen file: ' + file.name)
        
        # Loop the returned data (max 100), ordered by date (old to new) 
        for object in objects:
            id = int(object['id'],36)

            if id > max_id:
                nothing_processed = False
                created_utc = object['created_utc']
                max_id = id


                # This line is confusing. What if two posts have same timestamp? 
                # Maybe doesn't matter. THey are being saved by ID anyways.
                # This is really just set odlest time and close/open new file. 
                if created_utc > oldest_created_utc:


                    # Convert Epoch time to human readable date
                    oldest_created_utc_date = util.epoch_to_gmt(oldest_created_utc)
                    created_utc_date        = util.epoch_to_gmt(created_utc)
                    
                        
                    # Check if date of new data has passed midnight.
                    # And that new date isn't already saved.  
                    # If yes, create new file with data in name. 
                    if created_utc_date != oldest_created_utc_date:   

                        if created_utc_date not in days_exist:
                            file.close()
                            file = open(f"data/comments_by_date/{created_utc_date}.json","a")

                    

                    # Necessary to request newer comments
                    oldest_created_utc = created_utc       
                
                # Output JSON data to the opened file.
                print(json.dumps(object,sort_keys=True,ensure_ascii=True),file=file)

        
        # Exit if nothing happened.
        if nothing_processed: return
        # The newest time of the returned results will for the next request
        # be used as the input for request. 
        # oldest_created_utc -= 1

        # Sleep a little before the next recursive function call
        time.sleep(.5)



#------------------------------------------------------------------------------
# RUN PROGRAM FROM HERE
#------------------------------------------------------------------------------

# Start program by calling function with:
# 1) Subreddit specified
# 2) The type of data required (comment or submission)
extract_reddit_data(subreddit="europe",type="comment")

#print(gmt_to_epoch("28-01-2021", 0, 0, 0, 1, -1))

