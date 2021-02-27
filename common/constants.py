# Ordered list of columns in database.
KEY_LST = ('id','created_utc','created_date', 'score','author','body', 'subreddit')

# Database files
DB_FILE = "data/comments_by_date/comments.db"
DB_FILE_MARKET = "tickers/market.db"

# Create the table to store the comment data
CREATE_COMMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    created_utc INTEGER NOT NULL,
    created_date TEXT NOT NULL,
    score INTEGER NOT NULL,
    author TEXT NOT NULL,
    body TEXT NOT NULL,
    subreddit TEXT NOT NULL
);
"""

CREATE_STOCKS_TABLE = """
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    company TEXT,
    exchange text NOT NULL,
    asset text NOT NULL
);
"""
CREATE_PRICE_TABLE = """
CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY, 
    stock_id INTEGER,
    date NOT NULL,
    open NOT NULL, 
    high NOT NULL, 
    low NOT NULL, 
    close NOT NULL, 
    volume NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock (id)
);
"""

# Index for sorting on the time column
CREATE_SQLITE_INDEX = """
CREATE INDEX IF NOT EXISTS time_sort ON submissions(created_utc);
"""