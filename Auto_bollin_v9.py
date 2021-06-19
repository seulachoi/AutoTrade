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


# 볼린저밴드 상단 : 1분봉 1% 돌파 > 3분봉 1% 돌파 + 볼밴 3분봉 기준 직전 5개 중 중앙값 돌파 여부 확인
# 볼밴 너비가 직전 볼밴의 2배 
# 거래량 가장 많은 코인 매수
 #볼밴 for문 삭제 
 #볼밴상중하: 5분봉기준
 
print("start1")
while True:  
    
    # try:
    print("start")
    # cwd = os.getcwd()  # Get the current working directory (cwd)
    # files = os.listdir(cwd)

    f = open('upbit.txt') #upbit text파일 읽어서 access key, secret key 읽어오기
        # /Users/sara/Desktop/AutoTrade/upbit.txt
    lines = f.readlines()
    access = lines[0].strip() #줄바꿈 기호 /n 을 없애기 위해서 strip()
    secret = lines[1].strip()
    f.close()
    upbit = pyupbit.Upbit(access, secret) #Upbit라는 클래스 객체 생성 class instance, object 생성
    coin_return = 1.015
        
    while True:
        pd.options.display.float_format = "{:.1f}".format
        now = datetime.datetime.now()
        krw_balance = upbit.get_balance("KRW")
        
        if (now.hour == 8 and 50 <= now.minute <= 59) or (now.hour == 9 and 00 <= now.minute <= 40):
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

                tickerlist=pyupbit.get_tickers(fiat="KRW")
                tickerlist.remove('KRW-BTC')
                tickerlist.remove('KRW-ETH')
                tickerlist.remove('KRW-XRP')
                tickerlist.remove('KRW-EOS')
                tickerlist.remove('KRW-BTT')
                tickerlist.remove('KRW-ANKR')
                tickerlist.remove('KRW-RFR')
                tickerlist.remove('KRW-MOC')
                tickerlist.remove('KRW-AHT')
                tickerlist.remove('KRW-PUNDIX')
                tickerlist.remove('KRW-DOGE')
                tickerlist.remove('KRW-MED')
                tickerlist.remove('KRW-STRK')
                tickerlist.remove('KRW-IOTA')
                tickerlist.remove('KRW-BCHA')
                tickerlist.remove('KRW-CVC')
                tickerlist.remove('KRW-MFT')
                tickerlist.remove('KRW-ADA')
                tickerlist.remove('KRW-IOST')
                tickerlist.remove('KRW-EMC2')
                tickerlist.remove('KRW-PXL')

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
                    #print(ticker, candle_length)

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
                    band_low_1=bb_center_1-band1  #현재 볼밴 하단값

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
                    df_3_2 = df_raw.iloc[0:-2,] #0번째~-1번째까지 슬라이싱
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

                     #-4번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_4 = df_raw.iloc[0:-4,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_4['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_4=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_4=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_4=bb_center_3_4+band3_4 #현재 볼밴 상단값
                    band_low_3_4=bb_center_3_4-band3_4  #현재 볼밴 하단값
                    band_width_3_4 = band_high_3_4 - band_low_3_4

                    open_3_4 = df_3_4.iloc[-1]["open"]
                    close_3_4 = df_3_4.iloc[-1]["close"]

                     #-5번째 분봉 전 볼린저 밴드 너비 구하기
                    df_3_5 = df_raw.iloc[0:-5,] #0번째~-1번째까지 슬라이싱
                    unit=2
                    df=df_3_5['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_3_5=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    band3_5=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_3_5=bb_center_3_5+band3_5 #현재 볼밴 상단값
                    band_low_3_5=bb_center_3_5-band3_5  #현재 볼밴 하단값
                    band_width_3_5 = band_high_3_5 - band_low_3_5

                    open_3_5 = df_3_5.iloc[-1]["open"]
                    close_3_5 = df_3_5.iloc[-1]["close"]

                    

                    
                    #5분 데이터 : 추세 전환 판단을 위해 
                    data_5 = pyupbit.get_ohlcv(ticker, "minute5", count = 100)
                    if data_5 is None:
                        print(ticker, "error")
                        error_list.append(ticker)
                        continue
                    df_raw = pd.DataFrame(data_5)

                    #현재 시가 종가 캔들상승% 고가
                    open_5 = df_raw.iloc[-1]["open"]
                    close_5 = df_raw.iloc[-1]["close"]
                    high_5 = df_raw.iloc[-1]["high"]
                    value_5 = df_raw.iloc[-1]["value"]
                    low_5 = df_raw.iloc[-1]["low"]
                    #print(ticker, candle_length)

                    #볼린저밴드 변수 
                    unit=2
                    df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                    df_raw.astype(float)
                    df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                    if df is None:
                        continue
                    bb_center_5=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                    #print(bb_center, ticker)
                    band5=unit*numpy.std(df[len(df)-20:len(df)])
                    band_high_5=bb_center_5+band5 #현재 볼밴 상단값
                    band_low_5=bb_center_5-band5  #현재 볼밴 하단값

                    now_price = pyupbit.get_current_price(ticker)
                    if now_price is None:
                        continue

                    if now_price < 10000 and now_price > target_price and (((now_price/band_high_1)-1)*100) > 1 and (((now_price/band_high_1)-1)*100) < 3 and (((now_price/band_high_3)-1)*100) > 0.5 and band_width_3 > band_width_3_2*2 and ((open_3_5 < bb_center_3_5 and close_3_5 > bb_center_3_5 and close_3_5 / bb_center_3_5 > 1.01) or (open_3_4 < bb_center_3_4 and close_3_4 > bb_center_3_4 and close_3_4 / bb_center_3_4 > 1.01) or (open_3_3 < bb_center_3_3 and close_3_3 > bb_center_3_3 and close_3_3 / bb_center_3_3 > 1.01) or (open_3_2 < bb_center_3_2 and close_3_2 > bb_center_3_2 and close_3_2 / bb_center_3_2 > 1.01) or (open_3_1 < bb_center_3_1 and close_3_1 > bb_center_3_1 and close_3_1 / bb_center_3_1 > 1.01)):
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
                                'value': value_list,
                                'bandwidth': bandwidth_list}
                

                    #현재 볼밴 너비 구하기
                    unit=2
                    df_1 = pd.DataFrame(data)
                    df_1.apply(pd.to_numeric)
                    df_1.astype(float)
                    df_close=df_1['close']

                    bb_center_df_close=numpy.mean(df_close[len(df_close)-20:len(df_close)])               
                    band1_df_close=unit*numpy.std(df_close[len(df_close)-20:len(df_close)])
                    band_high_df_close=bb_center_df_close+band1_df_close
                    band_low_df_close=bb_center_df_close-band1_df_close

                    Bticker_band_width_1 = band_high_df_close - band_low_df_close
                    #print(Bticker_band_width_1, "Bticker_band_width_1")

                    #직전 분봉 볼밴 너비 구하기
                    unit=2
                    df_2 = df_1.iloc[0:-1,] #직전 분봉까지 슬라이싱
                    df_2.apply(pd.to_numeric)
                    df_2.astype(float)
                    df_close_2=df_2['close']

                    #0번째~-i번째까지 슬라이싱하고 볼밴값 구하기
                    bb_center_df_close_2=numpy.mean(df_close_2[len(df_close_2)-20:len(df_close_2)])  
                    print(bb_center_df_close_2, "bbcenter_df_close")              
                    band1_df_close_2=unit*numpy.std(df_close_2[len(df_close_2)-20:len(df_close_2)])
                    band_high_df_close_2=bb_center_df_close_2+band1_df_close_2
                    band_low_df_close_2=bb_center_df_close_2-band1_df_close_2

                    Bticker_band_width_2 = band_high_df_close_2 - band_low_df_close_2
                    print(Bticker_band_width_2, "Bticker_band_width_2")

                    Bticker_band = Bticker_band_width_1/Bticker_band_width_2

                    #현재 시가 종가 캔들상승% 고가
                    open = data.iloc[-1]["open"]
                    close = data.iloc[-1]["close"]
                    candle_length = (close/open-1)*100
                    high = data.iloc[-1]["high"]
                    value = data.iloc[-1]["value"]
                    #print(ticker, candle_length)

                    Bollin_tikcer_list_buy.append(Bticker)
                    open_list.append(open)
                    close_list.append(close)
                    value_list.append(value)
                    bandwidth_list.append(Bticker_band)

                    bollin_data = pd.DataFrame(raw_data)
                    bollin_data.drop_duplicates(['ticker'])

                raw_data = {'ticker': Bollin_tikcer_list_buy,
                            'open': open_list,
                            'close': close_list,
                            'value': value_list,
                            'bandwidth': bandwidth_list}
                bollin_data = pd.DataFrame(raw_data)
                
                #bollin_data 중 가장 가장 거래대금 큰 코인 이름
                if len(bollin_data) == 0:
                    print("bollin_data is none")    
                else:
                    print(bollin_data)
                    maxs = bollin_data["value"].max()
                    # print(maxs)

                    Bollin_coin_value = bollin_data.loc[(bollin_data['value'] == maxs)] #가장 거래대금 큰 코인 이름
                    Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                    Bollin_coin_bandwidth = bollin_data.loc[(bollin_data['ticker'] == Bollin_coin_name)]['value']
                    Bollin_coin_value = Bollin_coin_bandwidth.iloc[0]['value']

                    Bollin_coin_price = pyupbit.get_current_price(Bollin_coin_name)
                    if Bollin_coin_price is None:
                        continue
                    print(Bollin_coin_name)

                    
                    buy_amount = krw_balance-krw_balance*0.01
                    resp_buy_mkt = upbit.buy_market_order(Bollin_coin_name, buy_amount)  #시장가 매수 주문 
                    time.sleep(1)
                    uuid  = resp_buy_mkt['uuid']
                    print(uuid)
                    
                    result = f"{now}, 티커: {Bollin_coin_name}, {Bollin_coin_value}, 현재가: {Bollin_coin_price}"
                    print(f"{now}, 티커: {Bollin_coin_name}, {Bollin_coin_value}, 현재가: {Bollin_coin_price}")

                    #텔레그램으로 보내요
                    chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                    bot = telegram.Bot(token = chat_token)
                    chat_id = 1653560820
                    bot.sendMessage(chat_id=chat_id, text=result)

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
                                
                                time.sleep(1)
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
                                    chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                                    telegram_chat_id = 1653560820
                                    bot = telegram.Bot(token = chat_token)
                                    bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                    time.sleep(10)
                                    break
                                
                            else:
                                print("unsold")
                                time.sleep(2)
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
    
                Bollin_tikcer_list_buy=[]
                Bollin_tikcer_list=[]
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
                coin_return = 1.025 ###수정

                tickerlist=pyupbit.get_tickers(fiat="KRW")
                tickerlist.remove('KRW-BTC')
                tickerlist.remove('KRW-ETH')
                tickerlist.remove('KRW-XRP')
                tickerlist.remove('KRW-EOS')
                tickerlist.remove('KRW-BTT')
                tickerlist.remove('KRW-ANKR')
                tickerlist.remove('KRW-RFR')
                tickerlist.remove('KRW-MOC')
                tickerlist.remove('KRW-AHT')
                tickerlist.remove('KRW-PUNDIX')
                tickerlist.remove('KRW-DOGE')
                tickerlist.remove('KRW-MED')
                tickerlist.remove('KRW-STRK')
                tickerlist.remove('KRW-IOTA')
                tickerlist.remove('KRW-BCHA')
                tickerlist.remove('KRW-CVC')
                tickerlist.remove('KRW-MFT')
                tickerlist.remove('KRW-ADA')
                tickerlist.remove('KRW-IOST')
                tickerlist.remove('KRW-EMC2')
                tickerlist.remove('KRW-PXL')

                for ticker in tickerlist:
                    print(ticker)
                    
                    #stime = timeit.default_timer()
                    #10분 데이터 : 추세 전환 판단을 위해 
                    data = pyupbit.get_ohlcv(ticker, "minute5", count = 100)
                    if data is None:
                        print(ticker, "error")
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
                    volume = df_raw.iloc[-1]["volume"]
                    
                    #5개 전 현재 시가 종가 캔들상승% 고가
                    open_b5 = df_raw.iloc[-5]["open"]
                    close_b5 = df_raw.iloc[-5]["close"]
                    candle_length_b5 = (close/open-1)*100
                    high_b5 = df_raw.iloc[-5]["high"]
                    value_b5 = df_raw.iloc[-5]["value"]
                    low_b5 = df_raw.iloc[-5]["low"]

                    #10개 전 현재 시가 종가 캔들상승% 고가
                    open_b10 = df_raw.iloc[-10]["open"]
                    close_b10 = df_raw.iloc[-10]["close"]
                    candle_length_b10 = (close/open-1)*100
                    high_b10 = df_raw.iloc[-10]["high"]
                    value_b10 = df_raw.iloc[-10]["value"]
                    low_b10 = df_raw.iloc[-10]["low"]

                    #15개 전 현재 시가 종가 캔들상승% 고가
                    open_b15 = df_raw.iloc[-15]["open"]
                    close_b15 = df_raw.iloc[-15]["close"]
                    candle_length_b15 = (close/open-1)*100
                    high_b15 = df_raw.iloc[-15]["high"]
                    value_b15 = df_raw.iloc[-15]["value"]
                    low_b15 = df_raw.iloc[-15]["low"]

                    #20개 전 현재 시가 종가 캔들상승% 고가
                    open_b20 = df_raw.iloc[-20]["open"]
                    close_b20 = df_raw.iloc[-20]["close"]
                    candle_length_b20 = (close/open-1)*100
                    high_b20 = df_raw.iloc[-20]["high"]
                    value_b20 = df_raw.iloc[-20]["value"]
                    low_b20 = df_raw.iloc[-20]["low"]

                    #30개 전 현재 시가 종가 캔들상승% 고가
                    open_b30 = df_raw.iloc[-30]["open"]
                    close_b30 = df_raw.iloc[-30]["close"]
                    candle_length_b30 = (close/open-1)*100
                    high_b30 = df_raw.iloc[-30]["high"]
                    value_b30 = df_raw.iloc[-30]["value"]
                    low_b30 = df_raw.iloc[-30]["low"]

                    #40개 전 현재 시가 종가 캔들상승% 고가
                    open_b40 = df_raw.iloc[-40]["open"]
                    close_b40 = df_raw.iloc[-40]["close"]
                    
                    #50개 전 현재 시가 종가 캔들상승% 고가
                    open_b50 = df_raw.iloc[-50]["open"]
                    close_b50 = df_raw.iloc[-50]["close"]


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

                    #3분 데이터: 단기 상승하고 있는지 판단 위해 3분봉 종가>시가 인지 
                    data_3m = pyupbit.get_ohlcv(ticker, "minute3", count = 100)
                    if data_3m is None:
                        continue
                    df_raw_3m = pd.DataFrame(data_3m)
                    open_3m = df_raw_3m.iloc[-1]['open']
                    close_3m = df_raw_3m.iloc[-1]['close']
                    volume_3m = df_raw_3m.iloc[-1]['volume']

                    close_3m_2 = df_raw_3m.iloc[-2]['close']
                    close_3m_4 = df_raw_3m.iloc[-4]['close']
                    close_3m_6 = df_raw_3m.iloc[-6]['close']
                    close_3m_8 = df_raw_3m.iloc[-8]['close']
                    close_3m_9 = df_raw_3m.iloc[-9]['close']

                    price = pyupbit.get_current_price(ticker)
                    if price is None:
                        print(ticker, "error")
                        continue

                    #현재가가 볼밴 상단을 1% 돌파하고 있으면서, 과거 5,10, 15, 20, 30, 40, 50번째 종가가 현재가보다 낮아야함 (즉 하락 추세가 아닌), 3분봉 1,2,3,5,7,9번째 종가보다 현재가가 높아야함 (급락하는 경우 거르기위해)
                    if price is not None and ((price/band_high)-1)*100 > 0.3 and body > 0 and volume_3m > 10000 and close_3m > open_3m and price > close_b10 and price > close_b20 and price > close_b30 and price > close_b40 and price > close_b50 and price > close_3m_2 and price > close_3m_4 and price > close_3m_6 and price > close_3m_8: ###수정

                        print("buyifpass", ticker, high_center, high, price, bb_center)
                                    
                        Bollin_tikcer_list.append(ticker)
                    time.sleep(0.1)  ###수정
                        
                #볼밴상단값 돌파하고 있는 코인들을 for문 돌면서 
                for Bticker in Bollin_tikcer_list:
                    print(Bollin_tikcer_list, "bollintickerlist")
                    print(Bticker)
                    data = pyupbit.get_ohlcv(Bticker, "minute10", count=100)
                    if data is None:
                        error_list.append(Bticker)
                        continue

                    #현재 시가 종가 캔들상승% 고가
                    open = data.iloc[-1]["open"]
                    close = data.iloc[-1]["close"]
                    candle_length = (close/open-1)*100
                    high = data.iloc[-1]["high"]
                    value = data.iloc[-1]["value"]
                    
                    #과거 1-10개 분봉 중 볼밴 중앙값을 돌파한 분봉이 있는지 확인
                    for i in range(1,11):
                        print(i, "for문1-11")
                        df_raw = pd.DataFrame(data) 
                        #print(df_raw)              
                        now = datetime.datetime.now()
                        unit=2

                        df_1 = df_raw.iloc[0:-i,] #0번째~-i번째까지만 슬라이싱, i=2부터니까 [0:-2]번째, 직전 분봉부터 시작
                        # print(df_1)
                        df_1_close = df_1.iloc[-1]['close']
                        df_1_open = df_1.iloc[-1]['open']
                        df_1_low = df_1.iloc[-1]['low']
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
                        
                        #print((df_close.iloc[-1]/band_low_df_close-1)*100)
                        # print((df_1_low/band_low_df_close-1)*100, "low하단돌파값")
                        # print(band_low_df_close)
                        # print(price)
                        # print(df_close.iloc[-1])
                        
                        raw_data = {'ticker': Bollin_tikcer_list_buy,
                                    'open': open_list,
                                    'close': close_list,
                                    'value': value_list,
                                    'number': number_list,
                                    'numbervalue': number_value_list,
                                    'number21': number_21_list,
                                    'number21value': number_21_value_list}

                        #-i번째 종가 > -i번째 볼밴 중앙값을 1% 돌파하면
                        if df_1_open / bb_center_df_close < 0.99 and df_1_close > bb_center_df_close and df_1_close/bb_center_df_close > 1.01: ####수정
                            # and df_1_close > bb_center_df_close and df_1_close/bb_center_df_close > 1.01
                            number = i
                            number_percent = df_1_close/bb_center_df_close

                            #다시 for문을 돌면서 11-20개 분봉 중 볼밴 하단을 돌파한 분봉이 있는지 확인
                            for i in range(i,21):
                                print(i, "for문1-21")
                                # df_raw = pd.DataFrame(data) 
                                # #print(df_raw)              
                                # now = datetime.datetime.now()
                                unit=2
                                df_1 = df_raw.iloc[0:-i,] #0번째~-i번째까지만 슬라이싱, i=2부터니까 [0:-2]번째, 직전 분봉부터 시작
                                # print(df_1)
                                df_21_close = df_1.iloc[-1]['close']
                                df_21_low = df_1.iloc[-1]['low']
                                df_1.apply(pd.to_numeric)
                                df_1.astype(float)
                                df_close=df_1['close']

                                #0번째~-i번째까지 슬라이싱하고 볼밴값 구하기
                                bb_center_df_close=numpy.mean(df_close[len(df_close)-20:len(df_close)])             
                                band1_df_close=unit*numpy.std(df_close[len(df_close)-20:len(df_close)])
                                band_high_df_close=bb_center_df_close+band1_df_close
                                band_low_df_close=bb_center_df_close-band1_df_close

                                #볼밴 하단 값 돌파한 적 있는지 
                                if df_21_low/band_low_df_close < 0.99: ###수정
                                    Bollin_tikcer_list_buy.append(Bticker)
                                    print(Bollin_tikcer_list_buy, "bollinticerlist_buy")
                                    number_21 = i #몇번째 봉에 해당되는지 체크
                                    number_21_percent = df_21_low/band_low_df_close
                                    
                                    open_list.append(open)
                                    close_list.append(close)
                                    value_list.append(value)
                                    number_list.append(number)
                                    number_value_list.append(number_percent)
                                    number_21_list.append(number_21)
                                    number_21_value_list.append(number_21_percent)
                                    
                                    #돌파하고 있는 코인들의 티커, 돌파%, 시가, 종가, 캔들길이를 저장
                                    raw_data = {'ticker': Bollin_tikcer_list_buy,
                                                'open': open_list,
                                                'close': close_list,
                                                'value': value_list,
                                                'number': number_list,
                                                'numbervalue': number_value_list,
                                                'number21': number_21_list,
                                                'number21value': number_21_value_list}
                                    bollin_data = pd.DataFrame(raw_data)
                                    bollin_data.drop_duplicates(['ticker'])
                                    
                                    break
                        
                            
                raw_data = {'ticker': Bollin_tikcer_list_buy,
                            'open': open_list,
                            'close': close_list,
                            'value': value_list,
                            'number': number_list,
                            'numbervalue': number_value_list,
                            'number21': number_21_list,
                            'number21value': number_21_value_list}
                bollin_data = pd.DataFrame(raw_data)
                bollin_data.drop_duplicates()
                
                #bollin_data 형성되었는지 판단. 형성되었으면 그 중 가장 거래량 많은 코인 선택
                if len(bollin_data) == 0:
                    print("bollin_data is none")    
                else:
                    print(bollin_data)
                    maxs = bollin_data["value"].max() #돌파하고 있는 코인들 중 가장 거래량 많은 것을 찾음
                    # print(maxs)

                    Bollin_coin_value = bollin_data.loc[(bollin_data['value'] == maxs)] #가장 거래량 많은 코인 이름
                    Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                    #Bollin_coin_number = bollin_data.loc[(bollin_data['ticker'] == Bollin_coin_name)]['number']
                    Bollin_coin_number = Bollin_coin_value.iloc[0]['number']
                    Bollin_coin_number_value = Bollin_coin_value.iloc[0]['numbervalue']
                    Bollin_coin_number21 = Bollin_coin_value.iloc[0]['number21']
                    Bollin_coin_number21_value = Bollin_coin_value.iloc[0]['number21value']
                    
                    Bollin_coin_price = pyupbit.get_current_price(Bollin_coin_name)
                    if Bollin_coin_price is None:
                        continue
                    print(Bollin_coin_name)

                    buy_amount = krw_balance-krw_balance*0.01
                    resp_buy_mkt = upbit.buy_market_order(Bollin_coin_name, buy_amount)  #시장가 매수 주문 
                    time.sleep(1)
                    uuid  = resp_buy_mkt['uuid']
                    print(uuid)
                    
                    #텔레그램으로 보내요
                    result = f"{now}, 티커: {Bollin_coin_name}, 중앙값 돌파 분봉: {Bollin_coin_number, Bollin_coin_number_value}, 하단값 돌파 분봉: {Bollin_coin_number21, Bollin_coin_number21_value} 현재가: {Bollin_coin_price}"
                    print(f"{now}, 티커: {Bollin_coin_name}, 중앙값 돌파 분봉: {Bollin_coin_number, Bollin_coin_number_value}, 하단값 돌파 분봉: {Bollin_coin_number21, Bollin_coin_number21_value} 현재가: {Bollin_coin_price}")
                    
                    chat_token = "1827470195:AAGzfwuZtBxbind09ivsdDtcrHfb8tjkAic"
                    bot = telegram.Bot(token = chat_token)
                    chat_id = 1653560820
                    bot.sendMessage(chat_id=chat_id, text=result)
                    
                    # # print("buylist", buy_list)
                    time.sleep(30)

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
                            if forsell_price is not None and forsell_price > bought_coin_avg_price*1.04:
                                sell_price = bought_coin_avg_price*1.04
                            elif forsell_price is not None and forsell_price > bought_coin_avg_price*1.03:
                                sell_price = bought_coin_avg_price*1.03
                            else:
                                sell_price = bought_coin_avg_price*coin_return
                            print(sell_price)

                            if forsell_price >= sell_price:   #현재가가 sell price보다 같거나 높으면 시장가로 지금 던지고
                                upbit.sell_market_order(Bollin_coin_name, bought_coin_balance)
                                print("sell주문") 
                                
                                time.sleep(1)
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
                                    time.sleep(10)
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
                                    time.sleep(10)
                                    break
                                
                            else:
                                print("unsold")
                                time.sleep(3)
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