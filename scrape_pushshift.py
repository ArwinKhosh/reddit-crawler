import requests
import json
import os
import time
import datetime
import calendar

# TODO
# Understant why changing params to asc makes it work, desc just do one loop
# I Fucked up! e.g a is b checks if their ids are the same. Need to go through
# and fix where I use that. DONE! All good
# Ids are uniqe and is just an incrementing int in base 36. but comments
# can be posted at the same time so not good. 

# Docs: 
# https://www.reddit.com/r/pushshift/comments/8m50un/how_does_pushshift_update_submissions_and/
# https://github.com/pushshift/api  # This seems to be not up to date, but useful
# https://www.osrsbox.com/blog/2019/03/18/watercooler-scraping-an-entire-subreddit-2007scape//


PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"

def increment_time(epoch_time, add_day = 0, add_hour = 0, add_min = 0, add_sec = 0):

    epoch_time_add = epoch_time + \
                     add_day*24*60*60 + \
                     add_hour*60*60 + \
                     add_min*60 + \
                     add_sec

    return epoch_time_add


def epoch_to_gmt(epoch_time):

    gmt_date = time.strftime('%d-%m-%Y', time.gmtime(epoch_time))

    return gmt_date

def gmt_to_epoch(gmt_date, hour = 0, min = 0, sec = 0, add_day = 0, add_sec = 0 ):
    # Convert time in GMT to epoch time.

    gmt_datetime = gmt_date + " " + str(hour) + ":" + str(min)  + ":" + str(sec) 

    epoch_time = calendar.timegm(time.strptime(gmt_datetime, '%d-%m-%Y %H:%M:%S'))

    add_day_sec = add_day*24*60*60 + add_sec

    return epoch_time + add_day_sec

def exist_date(begin_date):
    # Checks if datafile already exists

    file_list = os.listdir("data\comments_by_date")
    
    # Strip JSON
    files = [item.split('.')[0] for item in file_list]

    # Calculate days between input date and today.
    sdate = datetime.datetime.strptime(begin_date, "%d-%m-%Y")
    edate = datetime.datetime.now()  

    delta = edate - sdate       # as timedelta

    delta_days = []
    for i in range(delta.days + 1):
        day = sdate + datetime.timedelta(days=i)
        delta_days.append(day.strftime("%d-%m-%Y"))

    # Compare intersection between files that already exist and the dates we want
    days_exist = list(set(delta_days).intersection(set(files)))

    return days_exist

def fetchObjects(**kwargs):
    # Default paramaters for API query
    params = {
        "sort_type":"created_utc",
        "sort":"asc", # desc gives news first
        "size":100, # apperantly the max size has been limited to 100 past year
        "fields": ["created_utc","id"] #, "body", "subreddit", "score"] 
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
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'],36)) # this default to asc order. So oldest post first
        return sorted_data_by_id

def extract_reddit_data(**kwargs):
    # Speficify the start timestamp

    t_epoch = time.time()
    # 1 week  back. Right now this gives two weeks for some reason
    oldest_created_utc = 1611442800 #  23 January 2021 23:00:00'
    oldest_created_utc_date = epoch_to_gmt(oldest_created_utc)

    print(oldest_created_utc_date)

    days_exist = exist_date(oldest_created_utc_date)

    # Create new start time if date 
    while oldest_created_utc_date in days_exist:
         oldest_created_utc = increment_time(oldest_created_utc,1,0,0,0)
         oldest_created_utc_date = epoch_to_gmt(oldest_created_utc)



        

    # Don'tknow what this is
    max_id = 0

    # Open a file for JSON output
    file = open(f"data/comments_by_date/{oldest_created_utc_date}.json","a")

    # While loop for recursive function
    #while 1:
    while 1:
        nothing_processed = True
        # Call the recursive function. Because of sorted in other function date
        # is oldest to newest
        objects = fetchObjects(**kwargs,after=oldest_created_utc)
        
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
                    oldest_created_utc_date =time.strftime('%d-%m-%Y', time.gmtime(oldest_created_utc))
                    created_utc_date = time.strftime('%d-%m-%Y', time.gmtime(created_utc))

                    # Check if date of new data has passed midnight.
                    # And that new date isn't already saved.  
                    # If yes, create new file with data in name. 
                    if (created_utc_date != oldest_created_utc_date and  
                        created_utc_date not in days_exist):
                        file.close()
                        file = open(f"data/comments_by_date/{created_utc_date}.json","a")
                    elif (created_utc_date != oldest_created_utc_date and  
                          exist_date(created_utc_date)):
                          date_exists = [int(item) for item in created_utc_date.split('-')]
                          timestamp   = datetime.datetime(date_exists[2], \
                              date_exists[1], date_exists[0] + 1,0,0).timestamp()
                          oldest_created_utc = int(timestamp) - 1
                    else:
                        oldest_created_utc = created_utc

                # Output JSON data to the opened file.
                print(json.dumps(object,sort_keys=True,ensure_ascii=True),file=file)

        
        # Exit if nothing happened.
        if nothing_processed: return
        # The newest time of the returned results will for the next request
        # be used as the input for request. 
        oldest_created_utc -= 1

        # Sleep a little before the next recursive function call
        time.sleep(.5)

# Start program by calling function with:
# 1) Subreddit specified
# 2) The type of data required (comment or submission)
extract_reddit_data(subreddit="debian",type="comment")

#print(gmt_to_epoch("28-01-2021", 0, 0, 0, 1, -1))

