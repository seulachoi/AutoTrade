from datetime import datetime
from pandas.io.formats.format import format_percentiles
from os import error
import pyupbit
import pandas as pd
import time
import datetime
import telegram
import timeit
import numpy
pd.options.display.float_format = "{:.1f}".format


# tickerlist = ["KRW-ONG"]
# for ticker in tickerlist:
#     df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1000)
#     df.to_excel(f"{ticker}1.xlsx")

#     df = pyupbit.get_ohlcv(ticker, interval="minute3", count=1000)
#     df.to_excel(f"{ticker}3.xlsx")

#     df = pyupbit.get_ohlcv(ticker, interval="minute5", count=500)
#     df.to_excel(f"{ticker}5.xlsx")

#     df = pyupbit.get_ohlcv(ticker, interval="minute15", count=500)
#     df.to_excel(f"{ticker}15.xlsx")

#     df = pyupbit.get_ohlcv(ticker, "day")
#     df.to_excel(f"{ticker}day.xlsx")
data = pyupbit.get_ohlcv(ticker, "day", count = 50)
df_raw = pd.DataFrame(data)
print(df_raw)

df_3_1 = df_raw.iloc[0:-1,]
df_3_2 = df_raw.iloc[0:-2,]
print(df_3_1)
print(df_3_2)

# tickerlist_A =[]
# tickerlist_B =[]

# tickerlist=pyupbit.get_tickers(fiat="KRW")

# for ticker in tickerlist:
#     data = pyupbit.get_ohlcv(ticker, "day", count = 50)
#     if data is None:
#         continue
#     change = (((data.iloc[-1]['close']/data.iloc[-2]['close'])-1)*100)
    
#     df_raw = pd.DataFrame(data) 
#     df_1 = df_raw.iloc[0:-1,]   
#     df_1_close = df_1.iloc[-1]['close']
#     now = datetime.datetime.now()
#     unit=2
#     df_close=df_1['close']
#     df_close.apply(pd.to_numeric)
#     df_close.astype(float)

#     #0번째~-i번째까지 슬라이싱하고 볼밴값 구하기
#     bb_center_df_close=numpy.mean(df_close[len(df_close)-20:len(df_close)])             
#     band1_df_close=unit*numpy.std(df_close[len(df_close)-20:len(df_close)])
#     band_high_df_close=bb_center_df_close+band1_df_close
#     band_low_df_close=bb_center_df_close-band1_df_close
#     close_band_yesterday = ((df_1_close/band_low_df_close)-1)*100

#     if change < -5 and close_band_yesterday < -2:
#         tickerlist_A.append(ticker)
        
#     else:
#         tickerlist_B.append(ticker)
#     time.sleep(0.1)
# print(tickerlist_A)
# print(tickerlist_B)
# print(len(tickerlist_A))
# print(len(tickerlist_B))