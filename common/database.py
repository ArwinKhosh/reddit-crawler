import sqlite3
import pandas as pd
from .constants import CREATE_COMMENTS_TABLE, CREATE_STOCKS_TABLE, CREATE_PRICE_TABLE


class SQLiteMarket:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)

    def __del__(self):
        self.conn.close()

    def read_db_into_pandas(self, limit=None):
        # Warning this is expensive on the memory
        query = "SELECT * from comments"
        if limit is not None:
            query += f" LIMIT {limit}"
        df = pd.read_sql_query(query, self.conn)
        return df

    def create_tables(self):
        c = self.conn.cursor()
        c.execute(CREATE_STOCKS_TABLE)
        c.execute(CREATE_PRICE_TABLE)
        c.close()
        self.conn.commit()

    def get_stocks(self, table):
        self.conn.row_factory = sqlite3.Row
        c = self.conn.cursor()
        # Get all symbols from market database. Returns list of Row objects.
        c.execute(f"""  SELECT symbol, id FROM {table} """)
        stocks = c.fetchall()
        return stocks
        



    def populate_stocks(self, stock_api):
        self.conn.row_factory = sqlite3.Row
        c = self.conn.cursor()
        # Get all symbols from market database. Returns list of Row objects.
        c.execute("""  SELECT symbol, company FROM stocks """)
        stocks = c.fetchall()
        symbols = [stock['symbol'] for stock in stocks]
        try: 
            if stock_api != [''] and stock_api[0] not in symbols:
                c.execute("INSERT INTO stocks (symbol, company, exchange, asset) VALUES (?, ?, ?, ?)", stock_api)
                print(f"Inserted new stocks into DB: {stock_api[0]} {stock_api[1]}")
            else:
                print("Nothig added")
        except Exception as e:
            print(e)
            print(stock_api)
        c.close()
        self.conn.commit()





    def insert_batch(self, batch, key_tpl):
        """
        Stores batch to database
        :param batch: Batch of comments
        :param key_tpl: ordered tuple of keys that are in the batch and should be stored
        :return:
        """
        c = self.conn.cursor()

        c.executemany(f"INSERT INTO comments {str(key_tpl)} "
                      f"VALUES (:id, :created_utc, :created_date, :score, :author, :body, :subreddit);", batch)
        c.close()
        self.conn.commit()

class SQLiteConnection:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)

    def __del__(self):
        self.conn.close()

    def read_db_into_pandas(self, limit=None):
        # Warning this is expensive on the memory
        query = "SELECT * from comments"
        if limit is not None:
            query += f" LIMIT {limit}"
        df = pd.read_sql_query(query, self.conn)
        return df

    def create_tables(self):
        c = self.conn.cursor()
        c.execute(CREATE_COMMENTS_TABLE)
        # c.execute(CREATE_SQLITE_INDEX)
        c.close()
        self.conn.commit()

    def get_latest_comment(self):
        c = self.conn.cursor()
        c.execute("SELECT created_utc FROM comments ORDER BY created_utc DESC LIMIT 1;")
        item = c.fetchone()
        c.close()
        return item

    def insert_batch(self, batch, key_tpl):
        """
        Stores batch to database
        :param batch: Batch of comments
        :param key_tpl: ordered tuple of keys that are in the batch and should be stored
        :return:
        """
        c = self.conn.cursor()

        c.executemany(f"INSERT INTO comments {str(key_tpl)} "
                      f"VALUES (:id, :created_utc, :created_date, :score, :author, :body, :subreddit);", batch)
        c.close()
        self.conn.commit()


