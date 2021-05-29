from os import error
import pyupbit
import pandas as pd
import time
import datetime
import telegram
import timeit


#변동성 돌파
# def cal_target(ticker):
#     before = df.iloc[-2]  #iloc는 행을 가져오는 
#     now = df.iloc[-1]
#     fiveminute_range = before['high']-before['low']
#     target = now['open'] + fiveminute_range*volatility_k
#     return target

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
        op_mode = False #프로그램을 처음 시작한 당일에는 매매가 실행되지 않고, 다음날 09시부터 실행되도록 op_mode를 설정
        hold = False
        pd.options.display.float_format = "{:.1f}".format
        value_k = 7
        volatility_k = 0.3
        
        coin_return = 1.02
        
        while True:
            now = datetime.datetime.now()
            krw_balance = upbit.get_balance("KRW")
            print(krw_balance)


            op_mode = True

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
                
                for ticker in tickerlist:
                    #print(ticker)
                    #stime = timeit.default_timer()
                    
                    #거래대금>직전10개 거래대금*value_k
                    df = pyupbit.get_ohlcv(ticker, interval="minute1")
                    average_value_10=df.iloc[-10:].mean()["value"]
                    last_value = df.iloc[-1]["value"]


                    #변동성 돌파 목표값 갱신
                    price = pyupbit.get_current_price(ticker)
                    before = df.iloc[-2]  #iloc는 행을 가져오는 
                    now = df.iloc[-1]
                    minute_range = before['high']-before['low']
                    target = now['open'] + minute_range*volatility_k
                    

                    if last_value > average_value_10*value_k and price >= target and price is not None:
                        print("value_buy_signal")
                        buy_amount = krw_balance-krw_balance*0.001
                        
                        resp_buy_mkt = upbit.buy_market_order(ticker, buy_amount) #시장가 주문 (티커, 매수할 금액)
                        # print(resp_buy_mkt)
                        uuid = resp_buy_mkt['uuid']
                        #print(uuid)
                        
                        #시간지나도 체결안되면 uuid로 주문 취소하고 다시 시도하기

                        time.sleep(0.5)

                        #업비트 계좌에 잔고가 있으면 가격 조건 걸어서 시장가 매도하기
                        i = 0
                        while True:
                            i = i + 1
                            #print(i)

                            if upbit.get_balance(ticker) >= 0:
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
                                if pyupbit.get_current_price(ticker) >= sell_price:
                                    upbit.sell_market_order(ticker, bought_coin_balance)
                                    
                                    time.sleep(1)
                                    if upbit.get_balance(ticker) == 0:
                                        hold = False
                                        krw_result_balance = upbit.get_balance("KRW")
                                        
                                        return_sold_c = ((krw_result_balance / krw_balance)- 1)*100
                                        return_sold ="{:.2f}".format(return_sold_c)

                                        result = f"현재시간: {now} 종목: {ticker} 수익률: {return_sold} Balance: {krw_result_balance}"
                                        print(f"현재시간: {now} 종목: {ticker} 수익률: {return_sold} 보유상태: {hold}")
                                        
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
        

 