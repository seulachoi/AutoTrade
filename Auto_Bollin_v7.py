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


# 볼린저밴드 상단값 돌파 중 과거 10개 봉이 볼밴 중앙값 돌파한 적 있는지 확인
# 볼린저밴드 상단값 돌파 중 과거 10개 봉이 볼밴 중앙값 돌파한 적 있는지 확인
# 하락추세인지 확인하기 위해서 1,10,20,30번째 전 종가 확인
# 그 중에서 거래량 가장 많은 코인 매수

while True:  
    print("start")
    
    # try:
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)

    f = open('/Users/sara/Desktop/AutoTrade/upbit.txt') #upbit text파일 읽어서 access key, secret key 읽어오기
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
        krw_balance = 100100
        # krw_balance = upbit.get_balance("KRW")
        print(krw_balance)

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
            number_21_list=[]

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
            tickerlist.remove('KRW-IOST')
            tickerlist.remove('KRW-EMC2')

            for ticker in tickerlist:
                print(ticker)
                
                #stime = timeit.default_timer()
                #15분 데이터 : 추세 전환 판단을 위해 
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
                low = df_raw.iloc[-1]["low"]
                
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

                #3분 데이터: 단기 상승하고 있는지 판단 위해 5분봉 종가>시가 인지 
                data_3m = pyupbit.get_ohlcv(ticker, "minute3", count = 100)
                if data_3m is None:
                    continue
                df_raw_3m = pd.DataFrame(data_3m)
                open_3m = df_raw_3m.iloc[-1]['open']
                close_3m = df_raw_3m.iloc[-1]['close']
                volume_3m = df_raw_3m.iloc[-1]['volume']

                price = pyupbit.get_current_price(ticker)
                if price is None:
                    print(ticker, "error")
                    continue

                now = datetime.datetime.now()
                if now.hour == 8 and now.minute == 59 and 30 <= now.second <= 59:
                    time.sleep(120)

                #현재가가 볼밴 상단을 1% 돌파하고 있으면서, 과거 5,10, 15, 20, 30번째 종가가 현재가보다 낮아야함 (즉 하락 추세가 아닌)
                if price is not None and ((price/band_high)-1)*100 > 0.5 and body > 0 and close_3m > open_3m and price > close_b5 and price > close_b10 and price > close_b15:
                    # and body > 0 and close_3m > open_3m and price > close_b5 and price > close_b10 and price > close_b15 and price > close_b20 and price > close_b30
                    # price > band_high and and volume_5m > 500000 and open < bb_center and close > bb_center and high_center > 0.0005 
                    print("buyifpass", ticker, high_center, high, price, bb_center)
                                
                    Bollin_tikcer_list.append(ticker)
                time.sleep(2)
                    
            #볼밴상단값 돌파하고 있는 코인들을 for문 돌면서 
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
                                'number21': number_21_list}

                    #-i번째 종가 > -i번째 볼밴 중앙값을 1% 돌파하면
                    if df_1_open < bb_center_df_close and df_1_close > bb_center_df_close and df_1_close/bb_center_df_close > 1.01:
                        #and df_1_close/bb_center_df_close > 0.01
                        number = i
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
                            df_1.apply(pd.to_numeric)
                            df_1.astype(float)
                            df_close=df_1['close']

                            #0번째~-i번째까지 슬라이싱하고 볼밴값 구하기
                            bb_center_df_close=numpy.mean(df_close[len(df_close)-20:len(df_close)])             
                            band1_df_close=unit*numpy.std(df_close[len(df_close)-20:len(df_close)])
                            band_high_df_close=bb_center_df_close+band1_df_close
                            band_low_df_close=bb_center_df_close-band1_df_close

                            #볼밴 하단 값 돌파한 적 있는지 
                            if df_21_close/band_low_df_close < 0.995:
                                Bollin_tikcer_list_buy.append(Bticker)
                                print(Bollin_tikcer_list_buy, "bollinticerlist_buy")
                                number_21 = i #몇번째 봉에 해당되는지 체크
                                
                                open_list.append(open)
                                close_list.append(close)
                                value_list.append(value)
                                number_list.append(number)
                                number_21_list.append(number_21)
                                
                                #돌파하고 있는 코인들의 티커, 돌파%, 시가, 종가, 캔들길이를 저장
                                raw_data = {'ticker': Bollin_tikcer_list_buy,
                                            'open': open_list,
                                            'close': close_list,
                                            'value': value_list,
                                            'number': number_list,
                                            'number21': number_21_list}
                                bollin_data = pd.DataFrame(raw_data)
                                bollin_data.drop_duplicates(['ticker'])
                                
                                break
                    
                        
            raw_data = {'ticker': Bollin_tikcer_list_buy,
                        'open': open_list,
                        'close': close_list,
                        'value': value_list,
                        'number': number_list,
                        'number21': number_21_list}
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
                Bollin_coin_number = bollin_data.loc[(bollin_data['ticker'] == Bollin_coin_name)]['number']
                
                Bollin_coin_price = pyupbit.get_current_price(Bollin_coin_name)
                if Bollin_coin_price is None:
                    continue
                print(Bollin_coin_name)


                result = f"{now}, 티커: {Bollin_coin_name}, {Bollin_coin_number}, 현재가: {Bollin_coin_price}"
                print(f"{now}, 티커: {Bollin_coin_name}, {Bollin_coin_number}, 현재가: {Bollin_coin_price}")
                
                buy_amount = krw_balance-krw_balance*0.01
                resp_buy_mkt = upbit.buy_market_order(Bollin_coin_name, buy_amount)  #시장가 매수 주문 
                time.sleep(1)
                #uuid  = resp_buy_mkt['uuid']
                #print(uuid)
                
                #텔레그램으로 보내요
                
                chat_token = "1827470195:AAGzfwuZtBxbind09ivsdDtcrHfb8tjkAic"
                bot = telegram.Bot(token = chat_token)
                chat_id = 1653560820
                bot.sendMessage(chat_id=chat_id, text=result)
                
                # # print("buylist", buy_list)
                # time.sleep(1)

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
                            time.sleep(2)
                    else:
                        time.sleep(10)
                        break
                        
                    
                
            print("끝")
            time.sleep(5)
                                    
                        
                    
                                
                        
                #print(len(error_list))
                #print(error_list)
    # except:
    #     print("try_except_error_start_again")
    #     chat_token = "1828606791:AAGe1b0czzFnGSuqP6y_d4NDazDq-SuMfwU"
    #     telegram_chat_id = 1653560820
    #     bot = telegram.Bot(token = chat_token)
    #     bot.sendMessage(chat_id = telegram_chat_id, text = "error")
    #     time.sleep(10)
    #     #     # Bollin_sara()
    # # Bollin_sara()