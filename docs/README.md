<!-- Ctrl+K V for preview -->

# TODO
1. Incorporate logger.
2. Create more error checking throughout the chain.
2. collect data from other subreddits (e.g stocks). Either using Task Scheduler or mulithreading.
3. 

2. Incorporate updated metadata (comment score).
3. Setting up Task Scheduler / Cron to run script every X minutes.
4. Making a backtester.
5. Connect to markets API to create a trading bot (or use an existing one).


# Ideas

### Operations
1. Using Pushbullet to notify of certain changes. For example program crash from API request failure. 

2. Pushshift has about 6 hour lag although it tries to be realtime. Does this matter for our project.

### Data storage and retrival
1. Saving data in SQLite or CSV? A CSV is very naive and simple. loading directly from it will be very quick. For massive database with complex structure CSV is not an option. SQL is super fast to select data from table an return that data to you. naturally, if you can select, modify and manipulate data it will add an overhead time cost to your call. If SQL we would be more flexible. 
[SQL for pushshift](https://www.reddit.com/r/pushshift/comments/lgior4/getting_commends_based_on_id_returns_all_scores/)

2. Good resource on memory management in [Python and pandas](https://pythonspeed.com/memory/)

3. There is also a [Beta API](https://beta.pushshift.io/redoc) which gets data in seperate way. And also 

### Backtesting
We need to backtest our stategy to make lower the risk and see if it would work on historical data. We can create our own framework or use an exsisting one. 

1. Backtrader
2. Zipline

### Data Quality
1. Pushshift grabs comments as close to realtime as possible. So score will be always 1. I think there is a way to update the score with reddits API using comments IDs


# Other Projects + resources
## Other stock market projects
1. [Very similar projecton on reddit, with backtesting. Using Quiverquant package in python to get WSB data](https://www.reddit.com/r/Python/comments/lmtf9z/building_an_algorithmic_trading_strategy_with/)
2. [Webisite for most mentioned tickers + sentiment on each ticker for various social media outlets Tickers that are gaining hype and losing momentum](https://swaggystocks.com/dashboard/home)

## Data Retrival Resources

1. [Creating large datasets using a news Pushshift wrapper called PMAW](https://www.reddit.com/r/pushshift/comments/ldp9pl/creating_large_datasets_using_pushshift/)
2. [Older pushhsift wrapper called PSAW](https://github.com/dmarx/psaw)
2. [All available posts and comments from /r/WallStreetBets](https://www.reddit.com/r/pushshift/comments/lfbejb/all_available_posts_and_comments_from/)
3. [Creat Youtube channel for creating trading bots, working with databases, backtesting, creating dashboards and deploying programs with python](https://www.youtube.com/c/parttimelarry/videos)






