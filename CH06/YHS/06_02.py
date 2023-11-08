# CH06 번동성 돌파전략 구현
## shift+alt+e로 특정 라인만 실행 가능

# 6-2. 변동성 돌파 전략 구현
###################################
## 6-2-1. 변동성 돌파 전략
###################################
'''
- 변동성 돌파 전략
1. 가격 변동폭 계산: 투자하려는 가상화폐의 전일 고가(high)에서 전일 저가(low)를 빼서 가상화폐의 가격 변동폭을 구함
2. 매수 기준: 당일 시간에서 (변동폭 * 0.5) 이상 상승하면 해당 가격에 바로 매수
3. 매도 기준: 당일 종가에 매도
'''

###################################
## 6-2-2 단계-1: 주기적으로 현재가 얻어오기
###################################
import pybithumb
import time

while True:
    price = pybithumb.get_current_price("BTC")
    print(price)
    time.sleep(0.2)


###################################
## 6-2-3 단계-2: 목표가 계산하기
###################################
import pybithumb

df = pybithumb.get_ohlcv("BTC")
print(df.tail())
yesterday = df.iloc[-2]

today_open = yesterday['close'] # 당일 시가
yesterday_high = yesterday['high'] # 전일 고가
yesterday_low = yesterday['low'] # 전일 저가
target = today_open + (yesterday_high - yesterday_low) * 0.5
print(target)

## 함수화
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']  # 당일 시가
    yesterday_high = yesterday['high']  # 전일 고가
    yesterday_low = yesterday['low']  # 전일 저가
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


###################################
## 6-2-3 단계-3: 자정에 목표가 갱신하기
###################################
## 매일 자정마자 "자정입니다" 문자열을 화면 출력
import time
import datetime

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

while True:
    now = datetime.datetime.now()
    if now == mid:
        print("정각입니다")
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1) # 1일의 시간을 더해 다음 날 자정으로 만듦

    print(now, "vs", mid) # [문제] 1초 차이로 "정각입니다" 문자열이 출력되지 않을 수 있음
    time.sleep(1)


## [솔루션] 구간을 비교해서 목표가까지 계산
import time
import datetime

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.timedelta(seconds=10) :
        print("정각입니다")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    time.sleep(1)

## 목표가 계산까지 포함된 전체 코드
import time
import pybithumb
import datetime

def get_target_price(ticker):
    df = pybithumb.get_ohlcv("BTC")
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(seconds=10) :
        target_price = get_target_price("BTC")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    current_price = pybithumb.get_current_price("BTC")
    print(current_price)

    time.sleep(1)


###################################
## 6-2-4 단계-4: 매수 시도
###################################
import os
import yaml
import time
import pybithumb
import datetime

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)
bithumb = pybithumb.Bithumb(con_key, sec_key)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(seconds=10):
        target_price = get_target_price("BTC")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    current_price = pybithumb.get_current_price("BTC")
    if current_price > target_price:
        krw = bithumb.get_balance("BTC")[2]
        orderbook = pybithumb.get_orderbook("BTC")
        sell_price = orderbook['asks'][0]['price']
        unit = krw/float(sell_price)
        bithumb.buy_market_order("BTC", unit)

    time.sleep(1)

## 매수와 관련된 코드 함수화
def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price)
    bithumb.buy_market_order(ticker, unit)


###################################
## 6-2-5 단계-5: 매도 시도
###################################
'''
변동성 돌파 전략에서는 보유 중인 비트코인을 다음 날 시초가에 전량매도
1. 보유한 비트코인이 있다면(당일 매수 조건에 따라 매수가 됐다면) 해당 비트코인을 시장가로 매매
2. 전일 시가, 고가, 저가, 종가 기준으로 래리 월리엄스의 변동성 돌파 전략 기반 목표가 재계산
3. 해당 일 기준으로 다음날의 00:00:00 초 시간 계산
'''
## 매도/매수 기능까지 함수로 정리한 전체 코드
import os
import yaml
import time
import pybithumb
import datetime

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)
bithumb = pybithumb.Bithumb(con_key, sec_key)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(seconds=10): 
        target_price = get_target_price("BTC")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        sell_crypto_currency("BTC")

    current_price = pybithumb.get_current_price("BTC")
    if current_price > target_price:
        buy_crypto_currency("BTC")

    time.sleep(1)

###################################
## 6-2-6 단계-6: 보안 및 예외처리
###################################
import time
import pybithumb
import datetime

with open("D:/Git Repository/cryptocurrency-book-study/Key/bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price)
    bithumb.buy_market_order(ticker, unit)


def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)


now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")

while True:
    # API 호출 실패
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10):
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            sell_crypto_currency("BTC")

        current_price = pybithumb.get_current_price("BTC")
        if current_price > target_price:
            buy_crypto_currency("BTC")
    except:
        print("에러 발생")
    time.sleep(1)
