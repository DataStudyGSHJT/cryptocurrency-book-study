# CH06 번동성 돌파전략 구현
## shift+alt+e로 특정 라인만 실행 가능

###################################
# 6-1. 빗썸 Private API
###################################
## 6-1-2. Bithumb 클래스 생성
import pybithumb


con_key = "81dd5f25e5daa70b2fff603901d2c09c"
# con_key = open("../../Key/con_key").read().strip()
sec_key = "82333efegeg9eg3e77c573weg34af17a"
# sec_key = open("../../Key/sec_key").read().strip()

bithumb = pybithumb.Bithumb(con_key, sec_key)


###################################
## 6-1-3. 잔고조회
###################################
## 비트코인 잔고 조회
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)
# balance = bithumb.get_balance("BTC")
balance = bithumb.get_balance("XRP")
print(balance) # (총 잔고, 거래 중인 비트코인 수량, 보유 중인 총원화, 주문에 사용된 원화)
print(format(balance[0], 'f')) # 실수 형태로 총 잔고 출력

## 모든 가상화폐 잔고 출력
import os
import yaml
import time
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

for ticker in pybithumb.get_tickers() :
    balance = bithumb.get_balance(ticker)
    print(ticker, ":", balance)
    time.sleep(0.1)


###################################
## 6-1-4. 매수
###################################
## 지정가 매수
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.buy_limit_order("BTC", 3900000, 0.001) # 주문 종류, 티커, 주문 번호
print(order) # ('bid', 'BTC', 'C0101000000918570681', 'KRW')

## 지정가 매수시 유의사항
## 최소 주문 수량 / 유효 자릿수 / 호가단위

## 비트코인은 1,000원 단위 호가를 지정해야 함
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.buy_limit_order("BTC", 4693100, 0.001) # 주문 종류, 티커, 주문 번호
print(order) # {'status': '5600', 'message': '입력값을 확인해주세요.'}

## 시장가 매수
## 최우선 매도호가에 거래되는 시장가 매수는 buy_market_order() 메서드 사용
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.buy_market_order("BTC", 1)
print(order)  # {'status': '5600', 'message': '주문량이 사용가능 KRW을 초과하였습니다.'}


## 매수 가능한 수량 확인하기
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

krw = bithumb.get_balance("BTC")[2] # 원화 잔고
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks'] # 매수 호가 내역
sell_price = asks[0]['price'] # 메도 금액
unit = krw/sell_price # 원화 잔고/최우선 매도 호가 금액 = 매수 수량
print(unit)


## 주문할 비트코인 수를 계산 후 시장가 주문을 발행 -> 실행하면 실제로 체결됨
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

krw = bithumb.get_balance("BTC")[2]
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/float(sell_price)

order = bithumb.buy_market_order("BTC", unit)
print(order) # 주문 ID를 리턴


###################################
## 6-1-5 매도
###################################
## 지정가 매도
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.sell_limit_order("BTC", 4000000, 1)
print(order) ## {'status': '5600', 'message': '회원 자산을 가져올수없습니다. 잠시후 이용 부탁드립니다.'}

## 잔고를 조회해서 보유 중인 비트코인 수량만큼 지정가 매도 주문
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

unit = bithumb.get_balance("BTC")[0] # 보유 중인 비트코인의 잔고
print(unit)
order = bithumb.sell_limit_order("BTC", 4000000, unit) # 지정가 매도도 1,000원 단위 호가를 지정해야 함
print(order)


## 시장가 매도
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

unit = bithumb.get_balance("BTC")[0]
order = bithumb.sell_market_order("BTC", unit)
print(order)


###################################
## 6-1-6 주문 취소
###################################
import os
import yaml
import pybithumb

with open(os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'cryptocurrency-book-study', 'Key', 'key.yaml'), 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

con_key = config.get('con_key', None)
sec_key = config.get('sec_key', None)

bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.buy_limit_order("BTC", 3000000, 0.001 )
print(order)

time.sleep(10)
cancel = bithumb.cancel_order(order) # order = ('bid', 'BTC', '주문번호')
print(cancel)
