from os import error
import pyupbit
import pandas as pd
import time
import datetime
import telegram
import timeit
import json


#변동성 돌파 & 거래량 급등 종목 단타 - 2021.06.04 

def autotrade_sara():
    try:
        #upbit 로그인 및 객체 생성
        f = open("upbit.txt") #upbit text파일 읽어서 access key, secret key 읽어오기
        lines = f.readlines()
        access = lines[0].strip() #줄바꿈 기호 /n 을 없애기 위해서 strip()
        secret = lines[1].strip()
        f.close()
        upbit = pyupbit.Upbit(access, secret) #Upbit라는 클래스 객체 생성 class instance, object 생성

        #변수 설정
        hold = False
        #op_mode = True
        pd.options.display.float_format = "{:.1f}".format
        value_k = 7
        volatility_k = 0.3
        
        coin_return = 1.01
        
        while True:
            now = datetime.datetime.now()
            krw_balance = upbit.get_balance("KRW")
            print(krw_balance)

            if krw_balance > 0:
                
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
                tickerlist.remove('KRW-STPT')
                tickerlist.remove('KRW-IOST')
                tickerlist.remove('KRW-EMC2')
                tickerlist.remove('KRW-QTUM')
                
                for ticker in tickerlist:
                    print(ticker)
                    #stime = timeit.default_timer()
                    
                    #상승장인지 하락장인지 판별: 오늘고가>어제고가, 오늘저가>어제저가
                    # df_day = pyupbit.get_ohlcv(ticker, interval="day", count=10)
                    # if df_day is None:
                    #     print("df_day_error", ticker)
                    #     continue

                    # Last_close_Value = df_day.iloc[-2]["close"]

                    # Last_High_Value = df_day.iloc[-2]["high"]
                    # Today_High_Value = df_day.iloc[-1]["high"]
                    # Today_Low_Price = df_day.iloc[-1]["low"]
                    # print(Last_High_Value)
                    # print(Today_High_Value)
                    
                    # Last_Low_Value = df_day.iloc[-2]["low"]
                    # Today_Low_Value = df_day.iloc[-1]["low"]
                    # print(Last_Low_Value)
                    # print(Today_Low_Value)

                    #거래대금>직전10개 거래대금평균*value_k
                    df = pyupbit.get_ohlcv(ticker, interval="minute3")
                    if df is None:
                        print("df_error", ticker)
                        continue

                    average_value_10=df.iloc[-10:].mean()["value"]
                    last_value = df.iloc[-1]["value"]
                    last_volume = df.iloc[-1]["volume"]
                  

                    #변동성 돌파 목표값 갱신
                    price = pyupbit.get_current_price(ticker)
                    before = df.iloc[-2]  #iloc는 행을 가져오는 
                    now = df.iloc[-1]
                    minute_range = before['high']-before['low']
                    target = now['open'] + minute_range*volatility_k
                    
                    # #1분봉 고가가 당일고가 대비 5%이상 하락했으면 필터링되도록
                    # min_today_high = df.iloc[-1]["high"]
                    # drop = ((min_today_high / Today_High_Value) - 1) * 100
                    

                    #15분봉 기준 현재종가 > 15분전 종가 : 상승추세인지 판별
                    # df_15m = pyupbit.get_ohlcv(ticker, interval="minute15")
                    # if df_15m is None:
                    #     print("df_15m_error", ticker)
                    #     continue

                    # last_30m_price = df_15m.iloc[-3]["high"]
                    # last_15m_price = df_15m.iloc[-2]["high"]
                    # now_15m_price = pyupbit.get_current_price(ticker)

                    #매수조건 1)오늘고가>=어제고가 3)거래대금>10개거래대금의 평균*value_k 4)변동성돌파(1분)
                    # 5)현재고가가 당일 고가 대비 5%이상 하락했는지 판별 6)현재가is not None
                    now = datetime.datetime.now()
                    if now.hour == 8 and now.minute == 59 and 30 <= now.second <= 59:
                        time.sleep(120)

                    if last_value > average_value_10*value_k and price >= target and price is not None:
                        #price > Last_close_Value*1.01 and 
                        # last_value > average_value_10*value_k and price >= target 
                        #Today_Low_Value > Last_Low_Value
                        #Today_High_Value >= Last_High_Value and 
                        #and now_15m_price > last_30m_price 
                        # drop > -5 and 
                        # now_15m_price > last_15m_price 
                        # and last_volume > 500000 
                        print("value_buy_signal")
                        
                        
                        chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                        telegram_chat_id = 1653560820
                        bot = telegram.Bot(token = chat_token)

                        test_message = [ticker, last_volume, price]
                        bot.sendMessage(chat_id = telegram_chat_id, text = test_message)

                        buy_amount = krw_balance-krw_balance*0.001
                        
                        upbit.buy_market_order(ticker, buy_amount) #시장가 주문 (티커, 매수할 금액)
                        # print(resp_buy_mkt)
                        #uuid = resp_buy_mkt['uuid']
                        #print(uuid)
                        
                        #추가구현: 시간지나도 체결안되면 uuid로 주문 취소하고 다시 시도하기

                        time.sleep(0.5)

                        #업비트 계좌에 잔고가 있으면 가격 조건 걸어서 시장가 매도하기
                        #추가구현: 필요시 i 횟수나 시간으로 손절 조건 추가
                        i = 0
                        while True:
                            i = i + 1
                            #print(i)

                            if upbit.get_balance(ticker) > 0:
                                hold = True
                                # print(hold)

                                bought_coin_balance = upbit.get_balance(ticker)
                                bought_coin_avg_price = upbit.get_avg_buy_price(ticker)
                                sell_price = bought_coin_avg_price*coin_return
                                time.sleep(1)

                                # print(bought_coin_balance)
                                # print(bought_coin_avg_price)
                                # print(sell_price)
                                # print(pyupbit.get_current_price(ticker))
                                
                                #가격 조건 확인
                                if pyupbit.get_current_price(ticker) >= sell_price:   #현재가가 sell price보다 같거나 높으면 시장가로 지금 던지고
                                    upbit.sell_market_order(ticker, bought_coin_balance) 
                                    
                                    time.sleep(1)
                                    if upbit.get_balance(ticker) == 0:
                                        hold = False
                                        krw_result_balance = upbit.get_balance("KRW")
                                        
                                        return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                        return_sold ="{:.2f}".format(return_sold_c)

                                        timenow = datetime.datetime.now()
                                        result = f"현재시간: {timenow} 종목: {ticker} 수익률: {return_sold} Balance: {krw_result_balance}"
                                        print(f"현재시간: {timenow} 종목: {ticker} 수익률: {return_sold} 보유상태: {hold}")
                                        
                                        chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
                                        telegram_chat_id = 1653560820
                                        bot = telegram.Bot(token = chat_token)
                                        bot.sendMessage(chat_id = telegram_chat_id, text = result)
                                        
                                    break
                                else:
                                    #print("unsold")
                                    time.sleep(1)
                            else:
                                
                                break
                        break
                        
            else:
                #슬랙메세지보내기
                print("need more money")
                    
    except:
        print("error")
        chat_token = "1764650725:AAHv775eH290ivG9TAtuaRBVkoxlQBGnqp0"
        chat = telegram.Bot(token = chat_token)

        telegram_chat_id = 1653560820
        
        bot = telegram.Bot(token = chat_token)
        bot.sendMessage(chat_id = telegram_chat_id, text = "error")
        time.sleep(10)
        autotrade_sara()

autotrade_sara()
        

 
