from os import error
import os
from pandas.core.frame import DataFrame
import pyupbit
import pandas as pd
import time
import datetime
import telegram
import timeit
import matplotlib.pyplot as plt
import pandas_datareader.data
import numpy
import json


# <전략1> : 8시 50분부터 9시 15분까지만
# 볼린저밴드 상단 : 1분봉 1% 돌파 > 3분봉 1% 돌파 + 볼밴 3분봉 기준 직전 5개 중 중앙값 돌파 여부 확인
# 볼밴 너비가 직전 볼밴의 2배 
# 거래량 가장 많은 코인 매수

#<전략2>
#전날 x% 이상 하락하여 볼밴 하단을 넘은 코인리스트 중에서 
#15분봉 기준 : 볼밴 하단>중앙값 x% 돌파하는 코인들 중 
#가장 거래량 많은 코인 매수 
#볼밴 상단 터치하거나 % 상승하면 매도 

#<전략3>
# 볼밴상중하
# 5분봉기준으로 볼밴 상단 돌파 & 하락 추세 아닌 코인들 & 3분봉으로도 상승 추세인 코인들
# 그중에서 과거 20개 동안 볼밴 하단 > 중앙값 돌파한 코인들 중 
# 가장 거래량 많은 코인 매수
# 2.5% 상승하면 매도
 
print("start1")
while True:  
    
    # try:
    print("start")
    # cwd = os.getcwd()  # Get the current working directory (cwd)
    # files = os.listdir(cwd)

    access = 'rxpmtSs1KMsiMVQE7NHaS3thYQA2t4LMOjrNFLIq' #줄바꿈 기호 /n 을 없애기 위해서 strip()
    secret = 'dx9PxuEUf7j5lPiZ14qBVI0RSkD1DiAfOr544LqD'
    upbit = pyupbit.Upbit(access, secret) #Upbit라는 클래스 객체 생성 class instance, object 생성
    coin_return = 1.02
        
    while True:
        pd.options.display.float_format = "{:.1f}".format
        now = datetime.datetime.now()
        krw_balance = upbit.get_balance("KRW")
        
        

        if (now.hour == 8 and 00 <= now.minute <= 59) or (now.hour == 9 and 00 <= now.minute <= 30):
            if krw_balance is not None and krw_balance > 0:

                Bollin_tikcer_list_buy=[]
                Bollin_tikcer_list=[]
                Price_bb_list=[]
                open_list=[]
                close_list=[]
                candle_length_list=[]
                error_list=[]
                value_list=[]
                bandwidth_list=[]
                volume_list=[]

                tickerlist=pyupbit.get_tickers(fiat="KRW")
                tickerlist.remove('KRW-BTC')
                tickerlist.remove('KRW-ETH')
                tickerlist.remove('KRW-XRP')
                tickerlist.remove('KRW-EOS')
                tickerlist.remove('KRW-BTT')
                tickerlist.remove('KRW-ANKR')
                tickerlist.remove('KRW-MOC')
                tickerlist.remove('KRW-AHT')
                tickerlist.remove('KRW-PUNDIX')
                tickerlist.remove('KRW-DOGE')
                tickerlist.remove('KRW-MED')
                tickerlist.remove('KRW-STRK')
                tickerlist.remove('KRW-MFT')
                tickerlist.remove('KRW-IOST')
                tickerlist.remove('KRW-ETC')  


                for ticker in tickerlist:
                    print(ticker)
                    
                    #stime = timeit.default_timer()
                    #1분 데이터 : 추세 전환 판단을 위해 
                    data_1 = pyupbit.get_ohlcv(ticker, "minute1", count = 100)
                    if data_1 is None:
                        print(ticker, "error")
                        error_list.append(ticker)
                        continue
                    df_raw = pd.DataFrame(data_1)

                    #현재 시가 종가 캔들상승% 고가
                    open_1 = df_raw.iloc[-1]["open"]
                    close_1 = df_raw.iloc[-1]["close"]
                    high_1 = df_raw.iloc[-1]["high"]
                    value_1 = df_raw.iloc[-1]["value"]
                    low_1 = df_raw.iloc[-1]["low"]

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_1=bb_center_1+band1 #현재 볼밴 상단값
                    band_low_1=bb_center_1-band1  #현재 볼밴 하단값\
                    band_width_1 = band_high_1 - band_low_1


                    #1분봉 1번째 전 분봉
                    df_1_1 = df_raw.iloc[0:-1,]
                    open_1_1 = df_1_1.iloc[-1]["open"]
                    close_1_1 = df_1_1.iloc[-1]["close"]
                    high_1_1 = df_1_1.iloc[-1]["high"]
                    head = high_1_1 - close_1_1
                    body = close_1_1 - open_1_1


                    #-1번째 분봉 전 볼린저 밴드 너비 구하
                    unit=2
                    df=df_1_1['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_1_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band1_1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_1_1=bb_center_1_1+band1_1 #현재 볼밴 상단값
                    band_low_1_1=bb_center_1_1-band1_1  #현재 볼밴 하단값
                    band_width_1_1 = band_high_1_1 - band_low_1_1


                    #3분 데이터 : 추세 전환 판단을 위해 
                    data_3 = pyupbit.get_ohlcv(ticker, "minute3", count = 100)
                    if data_3 is None:
                        print(ticker, "error")
                        error_list.append(ticker)
                        continue
                    df_raw = pd.DataFrame(data_3)

                    #현재 시가 종가 캔들상승% 고가
                    open_3 = df_raw.iloc[-1]["open"]
                    close_3 = df_raw.iloc[-1]["close"]
                    high_3 = df_raw.iloc[-1]["high"]
                    value_3 = df_raw.iloc[-1]["value"]
                    low_3 = df_raw.iloc[-1]["low"]
                    #print(ticker, candle_length)

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band3=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3=bb_center_3+band3 #현재 볼밴 상단값
                    band_low_3=bb_center_3-band3  #현재 볼밴 하단값
                    band_width_3 = band_high_3 - band_low_3

                    #-1번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_1 = df_raw.iloc[0:-1,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_1['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_1=bb_center_3_1+band3_1 #현재 볼밴 상단값
                    band_low_3_1=bb_center_3_1-band3_1  #현재 볼밴 하단값
                    band_width_3_1 = band_high_3_1 - band_low_3_1

                    open_3_1 = df_3_1.iloc[-1]["open"]
                    close_3_1 = df_3_1.iloc[-1]["close"]
                    body_3_1 = close_3_1 - open_3_1
                    target_price = open_3 + body_3_1*0.5

                    #-2번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_2 = df_raw.iloc[0:-2,] #0번째~-2번째까지 슬라이싱
                    unit=2
                    df=df_3_2['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_2=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_2=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_2=bb_center_3_2+band3_2 #현재 볼밴 상단값
                    band_low_3_2=bb_center_3_2-band3_2  #현재 볼밴 하단값
                    band_width_3_2 = band_high_3_2 - band_low_3_2

                    open_3_2 = df_3_2.iloc[-1]["open"]
                    close_3_2 = df_3_2.iloc[-1]["close"]

                    #-3번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_3 = df_raw.iloc[0:-3,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_3['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_3=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_3=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_3=bb_center_3_3+band3_3 #현재 볼밴 상단값
                    band_low_3_3=bb_center_3_3-band3_3  #현재 볼밴 하단값
                    band_width_3_3 = band_high_3_3 - band_low_3_3

                    open_3_3 = df_3_3.iloc[-1]["open"]
                    close_3_3 = df_3_3.iloc[-1]["close"]


                    now_price = pyupbit.get_current_price(ticker)
                    if now_price is None:
                        continue
                    
                    # data_morning = pyupbit.get_ohlcv(ticker, "day", count = 50)
                    # if data_morning is None:
                    #     continue
                    # change = (((data_morning.iloc[-1]['close']/data_morning.iloc[-2]['close'])-1)*100)

                    #단기 급등 종목: 1분봉 1%이상, 3%미만 상승종목 중 이전 
                    if open_1 < band_high_1 and close_1 > open_1 and head < body*2 and (((now_price/band_high_1)-1)*100) > 0.5 and (((now_price/band_high_1)-1)*100) < 3 and band_width_1 > band_width_1_1*2 and close_3 > open_3 and close_3 > close_3_1 and ((close_3 / bb_center_3 > 1.01) or (close_3_3 / bb_center_3_3 > 1.01) or (close_3_2 / bb_center_3_2 > 1.01) or (close_3_1 / bb_center_3_1 > 1.01)):
                        # now_price > target_price and 
                        # and (((close_3/band_high_3)-1)*100) and ((()close_5/band_high_5)-1)*100) and (((close_15/band_high_15)-1)*100) and band_width_3 > band_width_3_2*2
                        print("buyifpass", ticker)
                        Bollin_tikcer_list.append(ticker)
                    time.sleep(0.2)


                #볼밴상단값 돌파하고 있는 코인들을 for문 돌면서 
                for Bticker in Bollin_tikcer_list:
                    print(Bollin_tikcer_list, "bollintickerlist")
                    print(Bticker)
                    data = pyupbit.get_ohlcv(Bticker, "minute3", count=100)
                    

                    if data is None:
                        error_list.append(Bticker)
                        print("for문error")
                        continue

                    raw_data = {'ticker': Bollin_tikcer_list_buy,
                                'open': open_list,
                                'close': close_list,
                                'volume': volume_list}
                
                    #현재 시가 종가 캔들상승% 고가
                    open = data.iloc[-1]["open"]
                    close = data.iloc[-1]["close"]
                    high = data.iloc[-1]["high"]
                    value = data.iloc[-1]["value"]
                    volume = data.iloc[-1]["volume"]
                    #print(ticker, candle_length)

                    Bollin_tikcer_list_buy.append(Bticker)
                    open_list.append(open)
                    close_list.append(close)
                    volume_list.append(volume)

                    bollin_data = pd.DataFrame(raw_data)
                    bollin_data.drop_duplicates(['ticker'])

                raw_data = {'ticker': Bollin_tikcer_list_buy,
                            'open': open_list,
                            'close': close_list,
                            'volume': volume_list}
                bollin_data = pd.DataFrame(raw_data)
                
                #bollin_data 중 가장 가장 거래대금 큰 코인 이름
                if len(bollin_data) == 0:
                    print("bollin_data is none")    
                else:
                    print(bollin_data)
                    maxs = bollin_data["volume"].max()
                    # print(maxs)

                    Bollin_coin_value = bollin_data.loc[(bollin_data['volume'] == maxs)] #가장 거래대금 큰 코인 이름
                    Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                    Bollin_coin_bandwidth = bollin_data.loc[(bollin_data['ticker'] == Bollin_coin_name)]['volume']
                    #Bollin_coin_value = Bollin_coin_bandwidth.iloc[0]['value']

                    Bollin_coin_price = pyupbit.get_current_price(Bollin_coin_name)
                    if Bollin_coin_price is None:
                        continue
                    print(Bollin_coin_name)

                    data_1 = pyupbit.get_ohlcv(Bollin_coin_name, "minute1", count = 100)
                    if data_1 is None:
                        print(Bollin_coin_name, "error")
                        continue
                    df_raw = pd.DataFrame(data_1)

                    #현재 시가 종가 캔들상승% 고가
                    open_1 = df_raw.iloc[-1]["open"]
                    close_1 = df_raw.iloc[-1]["close"]
                    high_1 = df_raw.iloc[-1]["high"]
                    value_1 = df_raw.iloc[-1]["value"]
                    low_1 = df_raw.iloc[-1]["low"]

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_1=bb_center_1+band1 #현재 볼밴 상단값
                    band_low_1=bb_center_1-band1  #현재 볼밴 하단값\
                    band_width_1 = band_high_1 - band_low_1


                    #1분봉 1번째 전 분봉
                    df_1_1 = df_raw.iloc[0:-1,]
                    open_1_1 = df_1_1.iloc[-1]["open"]
                    close_1_1 = df_1_1.iloc[-1]["close"]
                    high_1_1 = df_1_1.iloc[-1]["high"]
                    head = high_1_1 - close_1_1
                    body = close_1_1 - open_1_1


                    #-1번째 분봉 전 볼린저 밴드 너비 구하
                    unit=2
                    df=df_1_1['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_1_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band1_1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_1_1=bb_center_1_1+band1_1 #현재 볼밴 상단값
                    band_low_1_1=bb_center_1_1-band1_1  #현재 볼밴 하단값
                    band_width_1_1 = band_high_1_1 - band_low_1_1


                    #3분 데이터 : 추세 전환 판단을 위해 
                    data_3 = pyupbit.get_ohlcv(Bollin_coin_name, "minute3", count = 100)
                    if data_3 is None:
                        continue
                    df_raw = pd.DataFrame(data_3)

                    #현재 시가 종가 캔들상승% 고가
                    open_3 = df_raw.iloc[-1]["open"]
                    close_3 = df_raw.iloc[-1]["close"]
                    high_3 = df_raw.iloc[-1]["high"]
                    value_3 = df_raw.iloc[-1]["value"]
                    low_3 = df_raw.iloc[-1]["low"]
                    #print(ticker, candle_length)

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band3=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3=bb_center_3+band3 #현재 볼밴 상단값
                    band_low_3=bb_center_3-band3  #현재 볼밴 하단값
                    band_width_3 = band_high_3 - band_low_3

                    #-1번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_1 = df_raw.iloc[0:-1,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_1['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_1=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_1=bb_center_3_1+band3_1 #현재 볼밴 상단값
                    band_low_3_1=bb_center_3_1-band3_1  #현재 볼밴 하단값
                    band_width_3_1 = band_high_3_1 - band_low_3_1

                    open_3_1 = df_3_1.iloc[-1]["open"]
                    close_3_1 = df_3_1.iloc[-1]["close"]
                    body_3_1 = close_3_1 - open_3_1
                    target_price = open_3 + body_3_1*0.5

                    #-2번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_2 = df_raw.iloc[0:-2,] #0번째~-2번째까지 슬라이싱
                    unit=2
                    df=df_3_2['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_2=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_2=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_2=bb_center_3_2+band3_2 #현재 볼밴 상단값
                    band_low_3_2=bb_center_3_2-band3_2  #현재 볼밴 하단값
                    band_width_3_2 = band_high_3_2 - band_low_3_2

                    open_3_2 = df_3_2.iloc[-1]["open"]
                    close_3_2 = df_3_2.iloc[-1]["close"]

                    #-3번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_3 = df_raw.iloc[0:-3,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_3['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_3=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_3=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_3=bb_center_3_3+band3_3 #현재 볼밴 상단값
                    band_low_3_3=bb_center_3_3-band3_3  #현재 볼밴 하단값
                    band_width_3_3 = band_high_3_3 - band_low_3_3

                    open_3_3 = df_3_3.iloc[-1]["open"]
                    close_3_3 = df_3_3.iloc[-1]["close"]


                    now_price = pyupbit.get_current_price(Bollin_coin_name)
                    if now_price is None:
                        continue

                    #단기 급등 종목: 1분봉 1%이상, 3%미만 상승종목 중 이전 
                    if open_1 < band_high_1 and close_1 > open_1 and head < body*2 and (((now_price/band_high_1)-1)*100) > 0.5 and (((now_price/band_high_1)-1)*100) < 3 and band_width_1 > band_width_1_1*2 and close_3 > open_3 and close_3 > close_3_1 and ((close_3 / bb_center_3 > 1.01) or (close_3_3 / bb_center_3_3 > 1.01) or (close_3_2 / bb_center_3_2 > 1.01) or (close_3_1 / bb_center_3_1 > 1.01)):

                        buy_amount = krw_balance-krw_balance*0.01
                        resp_buy_mkt = upbit.buy_market_order(Bollin_coin_name, buy_amount)  #시장가 매수 주문 
                        time.sleep(1)
                        uuid  = resp_buy_mkt['uuid']
                        print(uuid)
                        
                        result = f"{now}, 티커: {Bollin_coin_name}, 현재가: {Bollin_coin_price}"
                        print(f"{now}, 티커: {Bollin_coin_name}, 현재가: {Bollin_coin_price}")

                        #텔레그램으로 보내요
                        chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                        bot = telegram.Bot(token = chat_token)
                        chat_id = 1653560820
                        bot.sendMessage(chat_id=chat_id, text=result)
                    else:
                        time.sleep(5)

                    i = 0
                    while True:
                        
                        if upbit.get_balance(Bollin_coin_name) > 0:
                            i = i + 1
                            print(i, "매도시도")

                            hold = True

                            bought_coin_balance = upbit.get_balance(Bollin_coin_name)
                            bought_coin_avg_price = upbit.get_avg_buy_price(Bollin_coin_name)
                            
                            forsell_price = pyupbit.get_current_price(Bollin_coin_name)
                            if forsell_price is None:
                                continue
                            
                            #bollin coin name의 현재가가 볼밴 상단 값보다 % 높으면, return target을 높임
                            if forsell_price > bought_coin_avg_price*1.05:
                                sell_price = bought_coin_avg_price*1.05
                            elif forsell_price > bought_coin_avg_price*1.04:
                                sell_price = bought_coin_avg_price*1.04
                            elif forsell_price > bought_coin_avg_price*1.03:
                                sell_price = bought_coin_avg_price*1.03
                            else:
                                sell_price = bought_coin_avg_price*coin_return
                            print(sell_price)


                            if pyupbit.get_current_price(Bollin_coin_name) >= sell_price:   #현재가가 sell price보다 같거나 높으면 시장가로 지금 던지고
                                upbit.sell_market_order(Bollin_coin_name, bought_coin_balance)
                                print("sell주문") 
                                
                                time.sleep(0.5)
                                if upbit.get_balance(Bollin_coin_name) == 0:
                                    hold = False
                                    krw_result_balance = upbit.get_balance("KRW")
                                    print("팔림")
                                    
                                    return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                    return_sold ="{:.2f}".format(return_sold_c)

                                    timenow = datetime.datetime.now()
                                    result = f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} Balance: {krw_result_balance} sellprice: {round(sell_price,2)}"
                                    print(f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} 보유상태: {hold}")
                                    
                                    #수익률 텔레그램으로 보내요
                                    chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                                    telegram_chat_id = 1653560820
                                    bot = telegram.Bot(token = chat_token)
                                    bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                    time.sleep(10)
                                    break
                            elif pyupbit.get_current_price(Bollin_coin_name) < bought_coin_avg_price*0.95: #5%이상 손실이면 시장가 손절
                                upbit.sell_market_order(Bollin_coin_name, bought_coin_balance)
                                time.sleep(0.5)

                                if upbit.get_balance(Bollin_coin_name) == 0:

                                    hold = False
                                    krw_result_balance = upbit.get_balance("KRW")
                                    print("손절")
                                    
                                    return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                    return_sold ="{:.2f}".format(return_sold_c)

                                    timenow = datetime.datetime.now()
                                    result = f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} Balance: {krw_result_balance} 손절"
                                    print(f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} 보유상태: {hold} 손절")
                                    
                                    #수익률 텔레그램으로 보내요
                                    chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                                    telegram_chat_id = 1653560820
                                    bot = telegram.Bot(token = chat_token)
                                    bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                    time.sleep(10)
                                    break
                                
                            else:
                                print("unsold")
                                time.sleep(0.5)
                        else:
                            time.sleep(10)
                            break
                        
                            
                        
                    
                print("끝")
                print(len(error_list))
                time.sleep(2)
                                            
                                     
                                
                        #print(len(error_list))
                        #print(error_list)
        else:
            if krw_balance is not None and krw_balance > 0:
    
                tickerlist_A =[]
                tickerlist_B =[]
                Bollin_tikcer_list_buy=[]
                Bollin_tikcer_list_A=[]
                Bollin_tikcer_list_B=[]

                Price_bb_list=[]
                open_list=[]
                close_list=[]
                candle_length_list=[]
                error_list=[]
                value_list=[]
                number_list=[]
                number_value_list=[]
                number_21_list=[]
                number_21_value_list=[]
                volume_list=[]
                coin_return = 1.03 ###수정

                tickerlist=pyupbit.get_tickers(fiat="KRW")
                tickerlist.remove('KRW-BTC')
                tickerlist.remove('KRW-ETH')
                tickerlist.remove('KRW-XRP')
                tickerlist.remove('KRW-EOS')
                tickerlist.remove('KRW-BTT')
                tickerlist.remove('KRW-ANKR')
                tickerlist.remove('KRW-MOC')
                tickerlist.remove('KRW-AHT')
                tickerlist.remove('KRW-PUNDIX')
                tickerlist.remove('KRW-DOGE')
                tickerlist.remove('KRW-MED')
                tickerlist.remove('KRW-STRK')
                tickerlist.remove('KRW-MFT')
                tickerlist.remove('KRW-IOST')
                tickerlist.remove('KRW-ETC')  


                change_d=pd.Series() #k는 상승률을 받아서 저장할 시리즈 변수

                # value_d=pd.Series() 

                for ticker in tickerlist:
                    c=pyupbit.get_ohlcv(ticker, "day", count=2) #c에 ohlcv를 저장
                    if c is None:
                        continue

                    today_close=c.iloc[-1]['close'] #d는 전종가만 받아온다
                    yesterday_close = c.iloc[-2]['close']
                    change = format(((today_close / yesterday_close - 1)*100), '.2f')

                    change_d[ticker] = float(change)

                    # today_value=c.iloc[-1]['value']
                    # value_d[ticker] = float(today_value)
                    time.sleep(0.2)

                result_change = change_d.sort_values(ascending=False)
                result_change_list = []
                for i in range(1,11):
                    result_change_list.append(result_change.index[i])
                print(result_change_list)

                #전략 2
                for ticker in result_change_list:
                    print(ticker)
                    data = pyupbit.get_ohlcv(ticker, "minute5", count = 100)
                    if data is None:
                        error_list.append(ticker)
                        continue
                    df_raw = pd.DataFrame(data)
                    
                    #현재 시가 종가 캔들상승% 고가
                    open = df_raw.iloc[-1]["open"]
                    close = df_raw.iloc[-1]["close"]
                    candle_length = (close/open-1)*100
                    high = df_raw.iloc[-1]["high"]
                    value = df_raw.iloc[-1]["value"]
                    low = df_raw.iloc[-1]["low"]
                    
                    #1개 전 현재 시가 종가 캔들상승% 고가
                    close_b2 = df_raw.iloc[-2]["close"]
                    low_b2 = df_raw.iloc[-2]["low"]
                    high_b2 = df_raw.iloc[-2]["high"]
                    body_b2 = high_b2 - low_b2
                    head_b2 = high_b2 - close_b2

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high=bb_center+band1 #현재 볼밴 상단값
                    band_low=bb_center-band1  #현재 볼밴 하단값

                    high_center = ((high/bb_center)-1)*100  #고가에서 볼밴 중앙값까지
                    close_center = ((close/bb_center)-1)*100  #종가에서 볼밴 중앙값까지
                    body = close-open
                    print(ticker, close, band_high)

                    price = pyupbit.get_current_price(ticker)
                    if price is None:
                        print(ticker, "error")
                        continue

                    #1분봉으로 확인하기
                    data_b1 = pyupbit.get_ohlcv(ticker, "minute1", count = 50)
                    if data_b1 is None:
                        continue
                    df_raw_b1 = pd.DataFrame(data_b1)

                    open_b1_1 = df_raw_b1.iloc[-1]["open"]
                    close_b1_1 = df_raw_b1.iloc[-1]["close"]
             

                    #1개 전 현재 시가 종가 캔들상승% 고가
                    close_b1_2 = df_raw_b1.iloc[-2]["close"]
                    

                    df_b1 = df_raw_b1.iloc[0:-1,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df_b1_close=df_b1['close'] #Ohlcv에서 close 종가만 추출
                    if df_b1_close is None:
                        continue
                    bb_center_b1=numpy.mean(df_b1_close[len(df_b1_close)-20:len(df_b1_close)]) #볼밴 중간값
                    band_b1=unit*numpy.std(df_b1_close[len(df_b1_close)-20:len(df_b1_close)])
                    band_high_b1=bb_center_b1+band_b1 #볼밴 상단값
                    band_low_b1=bb_center_b1-band_b1  #볼밴 하단값

                    print(ticker, close_b1_2, band_high_b1)

                    #15분봉 기준 : 1개전~5개전 분봉의 고점 < 현재가
                    trend_true_list = []
                    trend_false_list = []
                    for i in range(2,6):
                        if price > df_raw.iloc[-i]["high"]:
                            trend = True
                            trend_true_list.append(trend)
                        else:
                            trend = False
                            trend_false_list.append(trend)

                    #현재가가 볼밴 상단 돌파(open은 볼밴 상단보다 아래 위치) + 직전 1분봉 종가 > 밴드 상단 + 15분봉 기준 : 1개전~5개전 분봉의 고점 < 현재가
                    if price is not None and close_b1_2 > band_high_b1 and close_b1_1 > open_b1_1 and open < band_high and ((price/band_high)-1)*100 > 0.2 and ((price/band_high)-1)*100 < 3 and body > 0 and price > close_b2 and len(trend_false_list) == 0 and head_b2 < body_b2:
                    # price is not None and price > (open + body_b2*0.5) and open <= bb_center and ((price/bb_center)-1)*100 > 1 and body > 0: ###수정       
                        Bollin_tikcer_list_A.append(ticker)
                        print(ticker, close_b1_2, band_high_b1)
                    time.sleep(0.1)
                        
                ##전략 2 - 볼밴상단값 돌파하고 있는 코인들을 for문 돌면서 
                for Bticker in Bollin_tikcer_list_A:
                    data_c15 = pyupbit.get_ohlcv(Bticker, "minute5", count=100)
                    if data_c15 is None:
                        error_list.append(Bticker)
                        continue

                    #현재 시가 종가 캔들상승% 고가
                    open = data_c15.iloc[-1]["open"]
                    close = data_c15.iloc[-1]["close"]
                    candle_length = (close/open-1)*100
                    high = data_c15.iloc[-1]["high"]
                    value = data_c15.iloc[-1]["value"]
                    volume = data_c15.iloc[-1]["volume"]
                    volume = round(volume, 2)
                    
                    #과거 1-5개 분봉 중 볼밴 중앙값을 돌파한 분봉이 있는지 확인
                    for i in range(1,6):
                        df_raw = pd.DataFrame(data_c15) 
                        #print(df_raw)              
                        now = datetime.datetime.now()
                        unit=2

                        df_1 = df_raw.iloc[0:-i,] #0번째~-i번째까지만 슬라이싱, i=2부터니까 [0:-2]번째, 직전 분봉부터 시작
                        df_1_close = df_1.iloc[-1]['close']
                        df_1_open = df_1.iloc[-1]['open']
                        df_1_low = df_1.iloc[-1]['low']
                        df_1_high = df_1.iloc[-1]['high']
                        
                        df_1.apply(pd.to_numeric)
                        df_1.astype(float)
                        df_close=df_1['close']

                        #0번째~-i번째까지 슬라이싱하고 볼밴값 구하기
                        bb_center_df_close=numpy.mean(df_close[len(df_close)-20:len(df_close)])             
                        band1_df_close=unit*numpy.std(df_close[len(df_close)-20:len(df_close)])
                        band_high_df_close=bb_center_df_close+band1_df_close
                        band_low_df_close=bb_center_df_close-band1_df_close
                        
                        bb_center_df_close_str = "{:.2f}".format(bb_center_df_close)
                        band1_df_close_str = "{:.2f}".format(band1_df_close)
                        band_high_df_close_str = "{:.2f}".format(band_high_df_close)
                        band_low_df_close_str = "{:.2f}".format(band_low_df_close)

                        #-i번째 볼밴 중앙값을 1% 돌파했으면 매수 시그널
                        if df_1_low <= bb_center_df_close and (df_1_close / bb_center_df_close) > 1.01: ###수정 0.98
                            #and df_1_close/bb_center_df_close > 0.01
                            number = i
                                                            
                            Bollin_tikcer_list_buy.append(Bticker)
                            open_list.append(open)
                            close_list.append(close)
                            volume_list.append(volume)
                            number_list.append(number)
                            value_list.append(value)

                            raw_data = {'ticker': Bollin_tikcer_list_buy,
                                        'open': open_list,
                                        'close': close_list,
                                        'value': value_list,
                                        'volume': volume_list}
                            
                            bollin_data = pd.DataFrame(raw_data)
                            bollin_data.drop_duplicates(['ticker'])
                            
                            break      
                        
                            
                raw_data = {'ticker': Bollin_tikcer_list_buy,
                            'open': open_list,
                            'close': close_list,
                            'value': value_list,
                            'volume': volume_list}
                bollin_data = pd.DataFrame(raw_data)
                bollin_data.drop_duplicates()
                len_bollin_data = len(bollin_data)
                name_bollin_data = bollin_data['ticker']
                
                #bollin_data 형성되었는지 판단. 형성되었으면 그 중 가장 거래량 많은 코인 선택
                if len(bollin_data) == 0:
                    print("bollin_data is none") 
                    time.sleep(10)   
                else:
                    print(bollin_data)
                    maxs = bollin_data["volume"].max() #돌파하고 있는 코인들 중 가장 거래량 많은 것을 찾음
                    # print(maxs)

                    Bollin_coin_value = bollin_data.loc[(bollin_data['volume'] == maxs)] #가장 거래량 많은 코인 이름
                    Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                    
                    Bollin_coin_price = pyupbit.get_current_price(Bollin_coin_name)
                    if Bollin_coin_price is None:
                        continue

                    data = pyupbit.get_ohlcv(Bollin_coin_name, "minute5", count = 100)
                    if data is None:
                        continue
                    df_raw = pd.DataFrame(data)
                    
                    #현재 시가 종가 캔들상승% 고가
                    open = df_raw.iloc[-1]["open"]
                    close = df_raw.iloc[-1]["close"]
                    candle_length = (close/open-1)*100
                    high = df_raw.iloc[-1]["high"]
                    value = df_raw.iloc[-1]["value"]
                    low = df_raw.iloc[-1]["low"]
                    
                    #1개 전 현재 시가 종가 캔들상승% 고가
                    close_b2 = df_raw.iloc[-2]["close"]
                    low_b2 = df_raw.iloc[-2]["low"]
                    high_b2 = df_raw.iloc[-2]["high"]
                    body_b2 = high_b2 - low_b2

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band1=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high=bb_center+band1 #현재 볼밴 상단값
                    band_low=bb_center-band1  #현재 볼밴 하단값

                    high_center = ((high/bb_center)-1)*100  #고가에서 볼밴 중앙값까지
                    close_center = ((close/bb_center)-1)*100  #종가에서 볼밴 중앙값까지
                    body = close-open

                    price = pyupbit.get_current_price(Bollin_coin_name)
                    if price is None:
                        continue

                    #1분봉으로 확인하기
                    data_b1 = pyupbit.get_ohlcv(Bollin_coin_name, "minute1", count = 50)
                    if data_b1 is None:
                        continue
                    df_raw_b1 = pd.DataFrame(data_b1)

                    #1개 전 현재 시가 종가 캔들상승% 고가
                    close_b1_2 = df_raw_b1.iloc[-2]["close"]

                    df_b1 = df_raw_b1.iloc[0:-1,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df_b1_close=df_b1['close'] #Ohlcv에서 close 종가만 추출
                    if df_b1_close is None:
                        continue
                    bb_center_b1=numpy.mean(df_b1_close[len(df_b1_close)-20:len(df_b1_close)]) #볼밴 중간값
                    band_b1=unit*numpy.std(df_b1_close[len(df_b1_close)-20:len(df_b1_close)])
                    band_high_b1=bb_center_b1+band_b1 #볼밴 상단값
                    band_low_b1=bb_center_b1-band_b1  #볼밴 하단값
                    
                    if price is not None and close_b1_2 > band_high_b1 and close_b1_1 > open_b1_1 and open < band_high and ((price/band_high)-1)*100 > 0.2 and ((price/band_high)-1)*100 < 3 and body > 0 and price > close_b2:
                        buy_amount = krw_balance-krw_balance*0.01
                        resp_buy_mkt = upbit.buy_market_order(Bollin_coin_name, buy_amount)  #시장가 매수 주문 
                        time.sleep(0.5)
                        uuid  = resp_buy_mkt['uuid']


                        #텔레그램으로 보내요
                        result = f"{now}, 티커: {Bollin_coin_name}, 거래량:{maxs:,.2f}, 현재가: {Bollin_coin_price}, 매수: {buy_amount}, 전략: 볼밴하단-중앙돌파, 검토대상: {name_bollin_data}"
                        print(result)
                        
                        chat_token = "1827470195:AAGzfwuZtBxbind09ivsdDtcrHfb8tjkAic"
                        bot = telegram.Bot(token = chat_token)
                        chat_id = 1653560820
                        bot.sendMessage(chat_id=chat_id, text=result)
                        time.sleep(3)
                    else:
                        time.sleep(10)

                    i = 0
                    while True:
                        
                        if upbit.get_balance(Bollin_coin_name) > 0:
                            i = i + 1
                            print(i, "매도시도")

                            hold = True

                            bought_coin_balance = upbit.get_balance(Bollin_coin_name)
                            bought_coin_avg_price = upbit.get_avg_buy_price(Bollin_coin_name)
                            
                            forsell_price = pyupbit.get_current_price(Bollin_coin_name)
                            if forsell_price is None:
                                continue

                            #bollin coin name의 현재가가 매수가보다 % 높으면, return target을 높임
                            if forsell_price is not None and forsell_price > bought_coin_avg_price*1.05:
                                sell_price = bought_coin_avg_price*1.05
                            elif forsell_price is not None and forsell_price > bought_coin_avg_price*1.04:
                                sell_price = bought_coin_avg_price*1.04
                            else:
                                sell_price = bought_coin_avg_price*coin_return
                            print(sell_price)

                            if forsell_price >= sell_price:   #현재가가 sell price보다 같거나 높으면 시장가로 지금 던지고
                                upbit.sell_market_order(Bollin_coin_name, bought_coin_balance)
                                print("sell주문") 
                                
                                time.sleep(2)
                                if upbit.get_balance(Bollin_coin_name) == 0:
                                    hold = False
                                    krw_result_balance = upbit.get_balance("KRW")
                                    print("팔림")
                                    
                                    return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                    return_sold ="{:.2f}".format(return_sold_c)

                                    timenow = datetime.datetime.now()
                                    result = f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} Balance: {krw_result_balance} sellprice: {round(sell_price,2)}"
                                    print(f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} 보유상태: {hold}")
                                    
                                    #수익률 텔레그램으로 보내요
                                    chat_token = "1827470195:AAGzfwuZtBxbind09ivsdDtcrHfb8tjkAic"
                                    telegram_chat_id = 1653560820
                                    bot = telegram.Bot(token = chat_token)
                                    bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                    time.sleep(90)
                                    break
                            elif ((pyupbit.get_current_price(Bollin_coin_name) / bought_coin_avg_price)-1)*100 <= -5: #5%이상 손실이면 시장가 손절
                                upbit.sell_market_order(Bollin_coin_name, bought_coin_balance)
                                time.sleep(1)

                                if upbit.get_balance(Bollin_coin_name) == 0:

                                    hold = False
                                    krw_result_balance = upbit.get_balance("KRW")
                                    print("손절")
                                    
                                    return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                    return_sold ="{:.2f}".format(return_sold_c)

                                    timenow = datetime.datetime.now()
                                    result = f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} Balance: {krw_result_balance} 손절"
                                    print(f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} 보유상태: {hold} 손절")
                                    
                                    #수익률 텔레그램으로 보내요
                                    chat_token = "1827470195:AAGzfwuZtBxbind09ivsdDtcrHfb8tjkAic"
                                    telegram_chat_id = 1653560820
                                    bot = telegram.Bot(token = chat_token)
                                    bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                    time.sleep(90)
                                    break
                                
                            else:
                                #print("unsold")
                                time.sleep(0.5)
                        else:
                            time.sleep(60)
                            break
                        
                    
                print("끝")
                time.sleep(5)

    # except:
    # print("try_except_error_start_again")
    # chat_token = "1828606791:AAGe1b0czzFnGSuqP6y_d4NDazDq-SuMfwU"
    # telegram_chat_id = 1653560820
    # bot = telegram.Bot(token = chat_token)
    # bot.sendMessage(chat_id = telegram_chat_id, text = "error")
    # time.sleep(10)