import requests
import time # to handle post time and request pausing

# TODO
# Possible scrape filters:
#    - self, picture, video post
#    - based on time compared to last update
# Save data with date in title and possible other reavling things
# Limit rate of request
# autenticate reuqest: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
#   - because you are suppsed to and then you will for sure get 1 call per sec


# IDEAS
#  - Two scripts? One to scrape historic data and one to scrape from last scrape?
#  - For now just want the words so don't need points. Assume edits are unimportant
#    so just look at when post was created.
#  - use cron to deploy script every X minutes


# Interesting parameters posts:
# created_utc
# num_comments
# name (which is the fullname uniqe ID)

headers = {
    'authority': 'www.reddit.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56 by u/TeslaS',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,no;q=0.7',
    'cookie': 'csv=1; edgebucket=PoBrCYPmOlUDYePXEu; reddaid=UPVMLYXZT6E7HAIB; __gads=ID=20a9e1e231db2933:T=1586714846:S=ALNI_MYo-pjd3eeMQIF7PYefObCkKj7hxQ; eu_cookie_v2=3; loid=0000000000672uvug0.2.1586714779982.Z0FBQUFBQmVvX3RYSFZfaDdEZWJfeHN5TGZOSmR4MkxBd3RhLXNveXNIN3Fycm5RVU96cmszWmRHMy1TS19NS2JtclZtQ2xlX0lXMGJMVjFmWlFDVkxxekcyeHk0b0xnYW5DeUY3UkZ6a0FER3VhNWtabjBfUk1ZU0lJeWZCYlh0ZDdYTnFYWUc5cDg; d2_token=3.1f7524bf19ae24d3fc68ad516c2740bb56d5423cbce7081812ed29a3f04bd728.eyJhY2Nlc3NUb2tlbiI6Ii1zamxwVHBJNzJ4YXIyTHI4TXhjM3hDNlVReDQiLCJleHBpcmVzIjoiMjAyMC0wNC0yNVQxMjozNjoyNC4wMDBaIiwibG9nZ2VkT3V0Ijp0cnVlLCJzY29wZXMiOlsiKiIsImVtYWlsIl19; recent_srs=t5_32g5k^%^2Ct5_2vlls^%^2Ct5_2u3sb^%^2Ct5_2revo^%^2Ct5_2sjey^%^2Ct5_2r36m^%^2Ct5_2qh4p^%^2Ct5_2u9xs^%^2Ct5_2rmj5^%^2C; session_tracker=RWgPV1TxwIAJXtFpEf.0.1612049072721.Z0FBQUFBQmdGZXF4VVd4Rmp0a01LVUZpMGZxWVB3dmRuRDc3RGZxWkM5RHFkeGdxdHh0RlZ4dlcwQXpYcTd0MjYxb2I3OVNvcjg2WndHR3pESTlZQVluZ0xtMHNLRW5LNlphYjlSZ1JSWUlKM29iSDJUSlBJWDBOSEtwLUQ2QURRai0weWtaX2ZQNy0',
}


def get_post_url():
    #while after != None:
    # API limit to 100 post per api call. Default 25.
    base_url = 'https://www.reddit.com/r/europe/top/.json?limit=5'
    response = requests.get(base_url, headers=headers)

    json_response = response.json()

    json_entries = json_response['data']['children']

    submission_url = [item['data']['permalink'] for item in json_entries]
    return submission_url


def get_post_comments():

    data_extension = '.json'
    submission_url = get_post_url()
    base_url = 'https://www.reddit.com'
    

    request_url = [base_url + item + data_extension for item in submission_url]

    response =[]
    for item in request_url:
        resp = requests.get(item, headers=headers)
        response.append(resp)
        time.sleep(1)
        

    return response


def save_post_comment():
    #Docs:
    # https://stackoverflow.com/questions/17518937/saving-a-json-file-to-computer-python

    
    json_comment = get_post_comments()

    for item in json_comment:
        jason_data = item.content


    with open('data/data.json', 'wb') as f:
        f.write(jason_data)




save_post_comment()