<!-- Ctrl+K V for preview -->

# Useful links Pushhsift

[Creating large datasets using Pushshift](https://www.reddit.com/r/pushshift/comments/ldp9pl/creating_large_datasets_using_pushshift/)


[All available posts and comments from /r/WallStreetBets](https://www.reddit.com/r/pushshift/comments/lfbejb/all_available_posts_and_comments_from/)


# Ideas

### Operations
1. Using Pushbullet to notify of certain changes. For example program crash from API request failure. 

2. Pushshift has about 6 hour lag although it tries to be realtime. Does this matter for our project.

### Data storage and retrival
1. Saving data in SQLite or CSV? A CSV is very naive and simple. loading directly from it will be very quick. For massive database with complex structure CSV is not an option. SQL is super fast to select data from table an return that data to you. naturally, if you can select, modify and manipulate data it will add an overhead time cost to your call. If SQL we would be more flexible. 
[SQL for pushshift](https://www.reddit.com/r/pushshift/comments/lgior4/getting_commends_based_on_id_returns_all_scores/)

2. Good resource on memory management in [Python and pandas](https://pythonspeed.com/memory/)

3. For the first version I will do this:
    1. Get JSON from API
    2. Convert to CSV
    3. save in CSV format
    4. Usaage: keywords: chunking and indexing. Check point 2. 


### Data Quality
1. Pushshift grabs comments as close to realtime as possible. So score will be always 1. I think there is a way to update the score with reddits API using comments IDs



