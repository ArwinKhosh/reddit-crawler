import os

# Ordered list of columns in database.
KEY_LST = ('id','created_utc', 'score','author','body', 'subreddit')

# If file structure changes this will not work
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Database file
DB_FILE = os.path.join(ROOT_DIR,"data/comments_by_date/eur_comments.db")

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