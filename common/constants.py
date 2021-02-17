
KEY_LST = ('id','created_utc', 'score','author','body', 'subreddit')
# Check these keys match the ones given in utils.constants

DB_FILE = "db_test.db"


# NULL
# INTEGER
# REAL
# TEXT 
# BLOB 

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