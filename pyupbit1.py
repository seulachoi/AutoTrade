#REST API에서 데이터 가져오기
from pandas.io.formats.format import format_percentiles
import requests
import pyupbit
import pandas as pd
import pprint

pd.options.display.float_format = "{:.1f}".format
krw_tickers = pyupbit.get_tickers(fiat="KRW")

prices = pyupbit.get_current_price(krw_tickers)
#print(prices)

orderbooks = pyupbit.get_orderbook("KRW-BTC") #15호가까지 매도/매수호가 제공
orderbook = orderbooks[0]

total_ask_size = orderbook['total_ask_size']
pprint.pprint(orderbooks)
pprint.pprint(total_ask_size)
