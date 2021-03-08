# Ordered list of columns in database.
KEY_LST = ('id','created_utc', 'score','author','body', 'subreddit')

# Database file
DB_FILE = "data/comments_by_date/eur_comments.db"

# Create the table to store the submission data
CREATE_COMMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    created_utc INTEGER NOT NULL,
    score INTEGER NOT NULL,
    author TEXT NOT NULL,
    body TEXT NOT NULL,
    subreddit TEXT NOT NULL
);
"""

# Index for sorting on the time column
CREATE_SQLITE_INDEX = """
CREATE INDEX IF NOT EXISTS time_sort ON submissions(created_utc);
"""