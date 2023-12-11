## shift+alt+e로 특정 라인만 실행 가능

###################################
# 10-4. 통합 화면
###################################

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
sys.path.append(r'D:\Git Repository\cryptocurrency-book-study\CH10\YHS')

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Home Trading System")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## 버튼 이벤트를 연결해서 매매 알고리즘을 싲가하는 이벤트 정의
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Home Trading System")

    # ----------------- 추 가 ------------------
        self.ticker = "BTC"           # 추후 사용
        self.button.clicked.connect(self.clickBtn)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            text = "매매중지"
        else:
            text = "매매시작"
        self.button.setText(text)
    # ------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## API Key와 Sercret key 입력 후 매매시작 버튼을 눌렀을 대 로그인 처리 추가
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
# ----------------- 추 가 ------------------
from pybithumb import Bithumb
# ------------------------------------------

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

    def clickBtn(self):
        # ----------------- 수 정 ------------------
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")
        else:
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")
        # ------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## 로그인 처리 추가
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
# ----------------- 추 가 ------------------
from pybithumb import Bithumb
# ------------------------------------------

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

    def clickBtn(self):
        # ----------------- 수 정 ------------------
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")
        else:
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")
        # ------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## 텍스트 파일에서 불러오기
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
# ----------------- 추 가 ------------------
from pybithumb import Bithumb
# ------------------------------------------

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

        # ----------------- 추 가 ------------------
        with open("D:/Git Repository/cryptocurrency-book-study/Key/bithumb.txt") as f:
            lines = f.readlines()
            apikey = lines[0].strip()
            seckey = lines[1].strip()
            self.apiKey.setText(apikey)
            self.secKey.setText(seckey)
        # ------------------------------------------

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")
        else:
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## 변동성 돌파 전략을 GUI와 연결
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pybithumb import Bithumb
# ----------------- 추 가 ------------------
import pybithumb
import datetime
import time
from PyQt5.QtCore import QThread, pyqtSignal

class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, bithumb):
        super().__init__()
        self.ticker = ticker
        self.bithumb = bithumb
        self.alive = True

    def run(self):
        while self.alive:
            self.tradingSent.emit("2021/03/04 12:11:41", "매수", "0.001")
            time.sleep(1)

    def close(self):
        self.alive = False
# ------------------------------------------

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

        with open("D:/Git Repository/cryptocurrency-book-study/Key/bithumb.txt") as f:
            lines = f.readlines()
            apikey = lines[0].strip()
            seckey = lines[1].strip()
            self.apiKey.setText(apikey)
            self.secKey.setText(seckey)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")
            # ----------------- 추 가 ------------------
            self.vw = VolatilityWorker(self.ticker, self.bithumb)
            self.vw.tradingSent.connect(self.receiveTradingSignal)
            self.vw.start()
            # ------------------------------------------
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")

    # ----------------- 추 가 ------------------
    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")
    # ------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())


## VolatiltyWorder에서 변동성 돌파 전략을 수행하도록 수정
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pybithumb import Bithumb
import pybithumb
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from volatility import *

class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, bithumb):
        super().__init__()
        self.ticker = ticker
        self.bithumb = bithumb
        self.alive = True

    # ----------------- 수 정 ------------------
    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False

        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)
                    desc = sell_crypto_currency(self.bithumb, self.ticker)

                    result = self.bithumb.get_order_completed(desc)
                    timestamp = result['data']['order_date']
                    dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pybithumb.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma5):
                        desc = buy_crypto_currency(self.bithumb, self.ticker)
                        result = self.bithumb.get_order_completed(desc)
                        timestamp = result['data']['order_date']
                        dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(tstring, "매수", result['data']['order_qty'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)
    # ------------------------------------------

    def close(self):
        self.alive = False

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

        with open("D:/Git Repository/cryptocurrency-book-study/Key/bithumb.txt") as f:
            lines = f.readlines()
            apikey = lines[0].strip()
            seckey = lines[1].strip()
            self.apiKey.setText(apikey)
            self.secKey.setText(seckey)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")

            self.vw = VolatilityWorker(self.ticker, self.bithumb)
            self.vw.tradingSent.connect(self.receiveTradingSignal)
            self.vw.start()
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")

    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())

## 프로그램이 종료될 때 각 서브 위젯들의 정상 종료를 위한 이벤트 처리
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pybithumb import Bithumb
import pybithumb
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from volatility import *

class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, bithumb):
        super().__init__()
        self.ticker = ticker
        self.bithumb = bithumb
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False
        print("target price :", target_price)
        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)
                    desc = sell_crypto_currency(self.bithumb, self.ticker)

                    result = self.bithumb.get_order_completed(desc)
                    timestamp = result['data']['order_date']
                    dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pybithumb.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma5):
                        desc = buy_crypto_currency(self.bithumb, self.ticker)
                        result = self.bithumb.get_order_completed(desc)
                        timestamp = result['data']['order_date']
                        dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(tstring, "매수", result['data']['order_qty'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)

    def close(self):
        self.alive = False

form_class = uic.loadUiType("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.button.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

        with open("D:/Git Repository/cryptocurrency-book-study/Key/bithumb.txt") as f:
            lines = f.readlines()
            apikey = lines[0].strip()
            seckey = lines[1].strip()
            self.apiKey.setText(apikey)
            self.secKey.setText(seckey)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.bithumb = Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return

            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")

            self.vw = VolatilityWorker(self.ticker, self.bithumb)
            self.vw.tradingSent.connect(self.receiveTradingSignal)
            self.vw.start()
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")

    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")

    # ----------------- 추 가 ------------------
    def closeEvent(self, event):
        self.vw.close()
        self.widget.closeEvent(event)
        self.widget_2.closeEvent(event)
        self.widget_3.closeEvent(event)
    # ------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())
