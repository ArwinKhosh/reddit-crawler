import praw

# Apperantly you can make 1 request a second. This is probably limiting for us
# Might want to look into Pushshift.

# Getting OAuth IDs from local .ini file. DOn't want to save password here. 
# User1 has user and password, readOnly not. 
reddit = praw.Reddit("readOnly")

# Read only mode is just public information. An authorized reddit instance can
# do anything your user can do on Reddit. 
reddit.read_only = True

# Just checking if we have a connection. Prints username.
print(reddit.user.me())

subreddit = reddit.subreddit("memes")

top = subreddit.top (limit = 5)

print(subreddit.display_name)  # output: redditdev
print(subreddit.title)         # output: reddit development
print(subreddit.description) 

#for sumbission in top:
#    print(submission)