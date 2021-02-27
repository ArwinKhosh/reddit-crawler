import yfinance
import sqlite3
import requests

from common.constants import CREATE_STOCKS_TABLE, CREATE_PRICE_TABLE, DB_FILE_MARKET

# Documentation:
# https://www.alphavantage.co/documentation/#

#------------------------------------------------------------------------------
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey=3TREVFBWJ4QDVQKK"

r = requests.get(ALPHA_VANTAGE_URL, timeout=30)

conn = sqlite3.connect(DB_FILE_MARKET)
c = conn.cursor()
c.execute(CREATE_STOCKS_TABLE)
c.execute(CREATE_PRICE_TABLE)

# Skip header. 
iter_stock = iter(r.iter_lines())
next(iter_stock)

for line in iter_stock:
    # Go from binary to decoded data. Also remove uneccassary columns. 
    stock_info = line.decode('utf-8').split(',')[:4]
    if stock_info == ['']:
        print ("Empty stock info")
        continue
    try:
        c.execute("INSERT INTO stocks (symbol, company, exchange, asset) VALUES (?, ?, ?, ?);", stock_info)
    except Exception as e:
        print(e)
        print(stock_info)
c.close()
conn.commit()

for line in r.iter_lines():
    print(line.decode('utf-8'))
    break