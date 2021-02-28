import yfinance
import sqlite3
import requests

from common.constants import CREATE_STOCKS_TABLE, CREATE_PRICE_TABLE, DB_FILE_MARKET

# Documentation:
# https://www.alphavantage.co/documentation/#

# r.text.splitlines()[0:4])
# https://stackoverflow.com/questions/3305926/python-csv-string-to-array
# https://stackoverflow.com/questions/31658115/python-csv-dictreader-parse-string
# https://www.google.com/search?newwindow=1&client=firefox-b-d&sxsrf=ALeKk010ZvAXYimL-T-Ur_2LVWytIEDkPA%3A1614396812232&ei=jL05YP3VDeWxrgTNh5_AAQ&q=load+csv+string+to+dictionary+python&oq=load+csv+string+to+dictionary+python&gs_lcp=Cgdnd3Mtd2l6EAM6BwgAEEcQsAM6BwgjELACECdQth5YtSZgpS1oAXACeACAAYYGiAHXFJIBCzAuMy4wLjQuNi0xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwj9y5PkkInvAhXlmIsKHc3DBxgQ4dUDCAw&uact=5

#------------------------------------------------------------------------------
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey=3TREVFBWJ4QDVQKK"

conn = sqlite3.connect(DB_FILE_MARKET)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute(CREATE_STOCKS_TABLE)
c.execute(CREATE_PRICE_TABLE)


#------------------------------------------------------------------------------
# Get all symbols from market database.

c.execute("""  SELECT symbol, company FROM stocks """)

# Returns list of Row objects.
stocks = c.fetchall()

symbols = [ stock['symbol'] for stock in stocks]

#------------------------------------------------------------------------------

r = requests.get(ALPHA_VANTAGE_URL, timeout=30)

# Skip header. 
iter_stock = iter(r.iter_lines())
next(iter_stock)

for line in iter_stock:
    # Go from binary to decoded data. Also remove uneccassary columns. 
    stock_info = line.decode('utf-8').split(',')[:4]
    try:
        if stock_info != [''] and stock_info[0] not in symbols:
            c.execute("INSERT INTO stocks (symbol, company, exchange, asset) VALUES (?, ?, ?, ?);", stock_info)
            print(f"Inserted new stocks {stock_info[0]} {stock_info[1]}")
    except Exception as e:
        print(e)
        print(stock_info)
c.close()
conn.commit()