import praw

reddit = praw.Reddit("user1", user_agent="testscript by u/TeslaS")

print(reddit.user.me())

subreddit = reddit.subreddit("memes")

top = subreddit.top (limit = 5)

for sumbission in top:
    print(submission)