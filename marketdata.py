import yfinance
import sqlite3
import requests

from common.constants import CREATE_STOCKS_TABLE, CREATE_PRICE_TABLE, DB_FILE_MARKET
from common.database import SQLiteMarket

# Documentation:
# https://www.alphavantage.co/documentation/#

# r.text.splitlines()[0:4])
# https://stackoverflow.com/questions/3305926/python-csv-string-to-array
# https://stackoverflow.com/questions/31658115/python-csv-dictreader-parse-string
# https://www.google.com/search?newwindow=1&client=firefox-b-d&sxsrf=ALeKk010ZvAXYimL-T-Ur_2LVWytIEDkPA%3A1614396812232&ei=jL05YP3VDeWxrgTNh5_AAQ&q=load+csv+string+to+dictionary+python&oq=load+csv+string+to+dictionary+python&gs_lcp=Cgdnd3Mtd2l6EAM6BwgAEEcQsAM6BwgjELACECdQth5YtSZgpS1oAXACeACAAYYGiAHXFJIBCzAuMy4wLjQuNi0xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwj9y5PkkInvAhXlmIsKHc3DBxgQ4dUDCAw&uact=5

#------------------------------------------------------------------------------
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey=3TREVFBWJ4QDVQKK"


db_connector = SQLiteMarket(DB_FILE_MARKET)
db_connector.create_tables()

r = requests.get(ALPHA_VANTAGE_URL, timeout=30)

# Skip header. -> Generator object
iter_stock = iter(r.iter_lines())
next(iter_stock)

for stock in iter_stock:
    # Go from binary to decoded data. Also remove uneccassary columns. -> List 
    stock_info = stock.decode('utf-8').split(',')[:4]
    db_connector.populate_stocks(stock_info)

