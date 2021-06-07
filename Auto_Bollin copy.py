from os import error
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

pd.options.display.float_format = "{:.1f}".format

while True:  
    try:
        f = open("upbit.txt") #upbit text파일 읽어서 access key, secret key 읽어오기
        lines = f.readlines()
        access = lines[0].strip() #줄바꿈 기호 /n 을 없애기 위해서 strip()
        secret = lines[1].strip()
        f.close()
        upbit = pyupbit.Upbit(access, secret) #Upbit라는 클래스 객체 생성 class instance, object 생성
        coin_return = 1.015

        while True:
            now = datetime.datetime.now()
            krw_balance = upbit.get_balance("KRW")
            print(krw_balance)

            Bollin_tikcer_list=[]
            Price_bb_list=[]
            open_list=[]
            close_list=[]
            candle_length_list=[]
            error_list=[]
            value_list=[]

            tickerlist=pyupbit.get_tickers(fiat="KRW")
            tickerlist.remove('KRW-BTC')
            tickerlist.remove('KRW-ETH')
            tickerlist.remove('KRW-XRP')
            tickerlist.remove('KRW-EOS')
            tickerlist.remove('KRW-BTT')
            tickerlist.remove('KRW-ANKR')
            tickerlist.remove('KRW-RFR')
            tickerlist.remove('KRW-MOC')
            tickerlist.remove('KRW-IGNIS')
            tickerlist.remove('KRW-AHT')
            tickerlist.remove('KRW-PUNDIX')
            tickerlist.remove('KRW-DOGE')
            tickerlist.remove('KRW-MED')
            tickerlist.remove('KRW-MFT')
            tickerlist.remove('KRW-ADA')
            tickerlist.remove('KRW-STPT')
            tickerlist.remove('KRW-IOST')
            tickerlist.remove('KRW-EMC2')

            for ticker in tickerlist:
                print(ticker)
                
                
                #stime = timeit.default_timer()
                data = pyupbit.get_ohlcv(ticker, "minute15", count = 100)
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
                #print(ticker, candle_length)

                #볼린저밴드 변수 
                unit=2
                df_raw.apply(pd.to_numeric) #close를 float으로 변환, 볼린저밴드 계산위해 변환시켜줌
                df_raw.astype(float)
                df=df_raw['close'] #Ohlcv에서 close 종가만 추출
                if df is None:
                    continue
                bb_center=numpy.mean(df[len(df)-20:len(df)]) #현재 볼밴 중간값
                band1=unit*numpy.std(df[len(df)-20:len(df)])
                band_high=bb_center+band1 #현재 볼밴 상단값
                band_low=bb_center-band1  #현재 볼밴 하단값
                high_center = ((high/bb_center)-1)*100
                print(high_center)

                price = pyupbit.get_current_price(ticker)
                if price is None:
                    print(ticker, "error")
                    continue

                now = datetime.datetime.now()
                if now.hour == 8 and now.minute == 59 and 30 <= now.second <= 59:
                    time.sleep(120)
                    
                #현재가>볼밴 중간값이고 현재 시가<볼밴 중간값이고 현재 종가>볼밴 중간값이면 (즉 현재가가 볼밴 중간값 돌파하고 있으면)
                if price is not None and price > bb_center and open < bb_center and close > bb_center: 
                    print("buyifpass", ticker, high_center, high, price, bb_center)
                    # and high_center > 0.25
                    # and open < bb_center and close > bb_center and high_center > 0.005
                    # print(ticker)
                    # print(price)
                    # print(band_low)
                    # print(bb_center)
                    # print(band_high)
                    # print(open)
                    # print(close)
                    
                    Bollin_tikcer_list.append(ticker)
                    # price_bb = (price/bb_center-1)*100 #현재가가 볼밴중간값 몇%돌파하고 있는지
                    # Price_bb_list.append(price_bb)
                    # open_list.append(open)
                    # close_list.append(close)
                    # candle_length_list.append(candle_length)
                    # value_list.append(value)

                    print(Bollin_tikcer_list, "for문 들어가기 전")
                    #돌파하고 있는 코인들의 티커, 돌파%, 시가, 종가, 캔들길이를 저장
                    # raw_data = {'ticker': Bollin_tikcer_list,
                    #             'price/bb_center': Price_bb_list,
                    #             'open': open_list,
                    #             'close': close_list,
                    #             'candle_length': candle_length_list}
                    # bollin_data = DataFrame(raw_data)

                    #print(bollin_data.sort_values(by=['price/bb_center'], ascending=False)) 

                    # maxs = bollin_data["price/bb_center"].max() #돌파하고 있는 코인들 중 가장 크게 돌파하고 있는 것을 찾음
                    # # print(maxs)

                    # # print(len(Bollin_tikcer_list))
                    # print(Bollin_tikcer_list)
                    

                    # Bollin_coin_value = bollin_data.loc[(bollin_data['price/bb_center'] == maxs)] #가장 크게 돌파하고 있는 코인 이름
                    # Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                    # #print(Bollin_coin_name)

                    # buy_list=[]

            #볼밴중간값 돌파하고 있는 코인들을 for문 돌면서 과거 10개 분봉 중 볼밴 하단값을 돌파한 분봉이 있는지 확인
            for Bticker in Bollin_tikcer_list:
                print(Bollin_tikcer_list, "bollintickerlist")
                print(Bticker)
                data = pyupbit.get_ohlcv(Bticker, "minute15", count=100)
                if data is None:
                    error_list.append(Bticker)
                    continue

                #현재 시가 종가 캔들상승% 고가
                open = data.iloc[-1]["open"]
                close = data.iloc[-1]["close"]
                candle_length = (close/open-1)*100
                high = data.iloc[-1]["high"]
                value = data.iloc[-1]["value"]
                #print(ticker, candle_length)
                
                
                for i in range(1,11):
                    print(i)
                    df_raw = pd.DataFrame(data) 
                    #print(df_raw)              
                    now = datetime.datetime.now()
                    unit=2
                    #print(i)

                    df_1 = df_raw.iloc[0:-i,] #0번째~-i번째까지만 슬라이싱, i=2부터니까 [0:-2]번째, 직전 분봉부터 시작
                    #print(df_1)
                    df_1_low = df_1.iloc[-1]['low']
                    #print(df_1_low, "LOW값")
                    df_1.apply(pd.to_numeric)
                    df_1.astype(float)
                    df_close=df_1['close']
                    #print(df_close)
                    #print(df_close.iloc[-1])

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
                    print("if 문 직전 df_1_low < band_low_df_close")
                    raw_data={}
                    #-i번째 종가 < -i번째 볼밴 하단값이면 매수
                    if df_1_low < band_low_df_close:
                        print("df_1_low < band_low_df_close")
                        # Bollin_tikcer_list.append(Bticker)
                        price_bb = (price/bb_center-1)*100 #현재가가 볼밴중간값 몇%돌파하고 있는지
                        Price_bb_list.append(price_bb)
                        open_list.append(open)
                        close_list.append(close)
                        candle_length_list.append(candle_length)
                        value_list.append(value)

                        #돌파하고 있는 코인들의 티커, 돌파%, 시가, 종가, 캔들길이를 저장
                        raw_data = {'ticker': Bollin_tikcer_list,
                                    'price/bb_center': Price_bb_list,
                                    'open': open_list,
                                    'close': close_list,
                                    'value': value_list}
                        bollin_data = DataFrame(raw_data)
                        print(bollin_data)
                        print(len(bollin_data))

                        #print(bollin_data.sort_values(by=['price/bb_center'], ascending=False)) 
            bollin_data = DataFrame(raw_data)
            print(len(bollin_data))
            print("bollindata오류")

            if len(bollin_data) == 0:
                print("bollin_data is none")    
            else:
                print(bollin_data)
                maxs = bollin_data["value"].max() #돌파하고 있는 코인들 중 가장 크게 돌파하고 있는 것을 찾음
                # print(maxs)

                Bollin_coin_value = bollin_data.loc[(bollin_data['value'] == maxs)] #가장 크게 돌파하고 있는 코인 이름
                Bollin_coin_name = Bollin_coin_value.iloc[0]['ticker']
                print(Bollin_coin_name)

                # # print("buy_signal")
                # buy_list.append(Bollin_coin_name)

                result = f"{now}, 티커: {Bollin_coin_name}, {i}, 현재종가: {price}, {i}번째 볼밴중간값: {bb_center_df_close_str}, {i}번째 볼밴하단값: {band_low_df_close_str}, {i}번째 하단돌파%: {((df_close.iloc[-1]/band_low_df_close)-1)*100}"
                print(f"{now}, 티커: {Bollin_coin_name}, {i}, 현재종가: {price}, {i}번째 볼밴중간값: {bb_center_df_close_str}, {i}번째 볼밴하단값: {band_low_df_close_str}, {i}번째 하단돌파%: {((df_close.iloc[-1]/band_low_df_close)-1)*100}")
                
                buy_amount = krw_balance-krw_balance*0.001
                #upbit.buy_market_order(Bollin_coin_name, buy_amount)   
                
                #텔레그램으로 보내요
                chat_token = "1828606791:AAGe1b0czzFnGSuqP6y_d4NDazDq-SuMfwU"
                bot = telegram.Bot(token = chat_token)
                chat_id = 1653560820
                bot.sendMessage(chat_id=chat_id, text=result)
                
                # print("buylist", buy_list)
                time.sleep(1)

                i = 0
                while True:
                    i = i + 1
                    print(i)

                    if upbit.get_balance(Bollin_coin_name) > 0:
                        hold = True
                        # print(hold)

                        bought_coin_balance = upbit.get_balance(Bollin_coin_name)
                        bought_coin_avg_price = upbit.get_avg_buy_price(Bollin_coin_name)
                        sell_price = bought_coin_avg_price*coin_return
                        time.sleep(1)                    
                        if pyupbit.get_current_price(Bollin_coin_name) >= sell_price:   #현재가가 sell price보다 같거나 높으면 시장가로 지금 던지고
                            upbit.sell_market_order(Bollin_coin_name, bought_coin_balance) 
                            
                            time.sleep(1)
                            if upbit.get_balance(Bollin_coin_name) == 0:
                                hold = False
                                krw_result_balance = upbit.get_balance("KRW")
                                
                                return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                return_sold ="{:.2f}".format(return_sold_c)

                                timenow = datetime.datetime.now()
                                result = f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} Balance: {krw_result_balance}"
                                print(f"현재시간: {timenow} 종목: {Bollin_coin_name} 수익률: {return_sold} 보유상태: {hold}")
                                
                                chat_token = "1828606791:AAGe1b0czzFnGSuqP6y_d4NDazDq-SuMfwU"
                                telegram_chat_id = 1653560820
                                bot = telegram.Bot(token = chat_token)
                                bot.sendMessage(chat_id = telegram_chat_id, text = result)
                            break
                    else:
                        print("unsold")
                        
                break
            print("끝")
                                
                    
                
                            
                    
            #print(len(error_list))
            #print(error_list)
    except:
        print("try_except_error_start_again")
        chat_token = "1828606791:AAGe1b0czzFnGSuqP6y_d4NDazDq-SuMfwU"
        telegram_chat_id = 1653560820
        bot = telegram.Bot(token = chat_token)
        bot.sendMessage(chat_id = telegram_chat_id, text = "error")
        time.sleep(10)
        # Bollin_sara()
# Bollin_sara()
