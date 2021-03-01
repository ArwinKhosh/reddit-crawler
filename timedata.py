
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

from common.constants import DB_FILE_MARKET
from common.database import SQLiteMarket

#* Documentation and Resoruces
# https://github.com/ranaroussi/yfinance
# https://www.youtube.com/watch?v=5q6s6n1f8d8


# TODO
# read availbale stocks from database
# Create a dictionary of stock: dbID
# Get data stocs from yahoo (maybe jsut a subset)
# save in DB using id of the stock as foreign key. 


db_connector = SQLiteMarket(DB_FILE_MARKET)
stocks = db_connector.get_stocks('stocks')
stocks_id = dict(stocks)
symbols = list(stocks_id.keys())

conn = sqlite3.connect(DB_FILE_MARKET)
c = conn.cursor()
symbols = symbols[0:30]
chunk_size = 10
chunk = 0 
while chunk < len(symbols):

    symbols_chunk = symbols[chunk:chunk + chunk_size]
    # class 'pandas.core.frame.DataFrame'>
    stock_price = yf.download(symbols_chunk, period = '1mo', group_by = 'ticker')

    chunk += chunk_size

    for symbol in symbols_chunk:
        stock_price_symbol = stock_price[symbol]
        del stock_price_symbol['Adj Close']

        for idx, stock_OHLC in stock_price_symbol.iterrows():

            if not np.isnan(stock_OHLC['Open']):
            
                c.execute("""INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (stocks_id[symbol], idx.date(), stock_OHLC['Open'], stock_OHLC['High'],stock_OHLC['Low'], stock_OHLC['Close'],stock_OHLC['Volume']))
                conn.commit()
                c.close
                

