## shift+alt+e로 특정 라인만 실행 가능

###################################
# 10-3. 실시간 개요창
###################################

## 10.3.1. UI레이아웃 설정

## 10.3.2. 파이썬에서 기능 연결
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/overview.ui", self)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())

## 가상화폐 거래소 API를 사용해서 실제 데이터로 변경
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pybithumb import WebSocketManager

class OverViewWorker(QThread):
    # OverViewworker의 웹소켓에서 메인 스레드로 데이터를 전송하기 위한 시그널 정의
    dataSent = pyqtSignal(int, float, float, int, float, int, float, int)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        # 24H를 기준으로 비트코인 가격정보(ticker)를 요청하는 웹소켓 정의
        wm = WebSocketManager("ticker", [f"{self.ticker}_KRW"], ["24H"])
        while self.alive:
            data = wm.get() # 웹 서버가 보내온 정보를 얻어옴
            # 전송된 데이터에서 필요한 값들을 인덱싱
            self.dataSent.emit(int  (data['content']['closePrice'    ]),
                               float(data['content']['chgRate'       ]),
                               float(data['content']['volume'        ]),
                               int  (data['content']['highPrice'     ]),
                               float(data['content']['value'         ]),
                               int  (data['content']['lowPrice'      ]),
                               float(data['content']['volumePower'   ]),
                               int  (data['content']['prevClosePrice']))


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/overview.ui", self)

        self.ticker = ticker
        # OverViewWorker를 생성하고 시그널을 연결할 슬롯 정의
        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()

    def fillData(self, currPrice, chgRate, volume, highPrice, value, lowPrice, volumePower, PrevClosePrice):
        # 슬롯으로 전달된 데이터를 Label에 출력
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_4.setText(f"{volume:,.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value/100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_12.setText(f"{volumePower:.2f}%")
        self.label_14.setText(f"{PrevClosePrice:,}")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())


## 빗썸 웹페이지와 동일한 상승폭과 체결강도를 나타내려면, 웹소켓의 ticktype 파라미터를 수정해서 ["24H", "MID"]를 모두 구독하고, 각각 별도의 시그널로 처리
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pybithumb import WebSocketManager

class OverViewWorker(QThread):
    # ----------------- 수 정 ------------------
    data24Sent = pyqtSignal(int, float, int, float, int, int)
    dataMidSent = pyqtSignal(int, float, float)
    # ------------------------------------------

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        # ----------------- 수 정 ------------------
        wm = WebSocketManager("ticker", [f"{self.ticker}_KRW"], ["24H", "MID"])
        while self.alive:
            data = wm.get()

            if data['content']['tickType'] == "MID":
                self.dataMidSent.emit(int  (data['content']['closePrice'    ]),
                                      float(data['content']['chgRate'       ]),
                                      float(data['content']['volumePower'   ]))
            else:
                self.data24Sent.emit(int  (data['content']['closePrice'    ]),
                                     float(data['content']['volume'        ]),
                                     int  (data['content']['highPrice'     ]),
                                     float(data['content']['value'         ]),
                                     int  (data['content']['lowPrice'      ]),
                                     int  (data['content']['prevClosePrice']))
        # ------------------------------------------

        wm.terminate()

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/overview.ui", self)

        self.ticker = ticker
        self.ovw = OverViewWorker(ticker)
        # ----------------- 수 정 ------------------
        self.ovw.data24Sent.connect(self.fill24Data)
        self.ovw.dataMidSent.connect(self.fillMidData)
        # ------------------------------------------
        self.ovw.start()

    def closeEvent(self, event):
        self.ovw.close()

    # ----------------- 수 정 ------------------
    def fill24Data(self, currPrice, volume, highPrice, value, lowPrice, PrevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_4.setText(f"{volume:,.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value/100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_14.setText(f"{PrevClosePrice:,}")

    def fillMidData(self, currPrice, chgRate, volumePower):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_12.setText(f"{volumePower:.2f}%")
    # ------------------------------------------


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())

## 가격에 따라 등락률 색상 변경
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pybithumb import WebSocketManager

class OverViewWorker(QThread):
    data24Sent = pyqtSignal(int, float, int, float, int, int)
    dataMidSent = pyqtSignal(int, float, float)

    def __init__(self, ticker="BTC"):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        wm = WebSocketManager("ticker", [f"{self.ticker}_KRW"], ["24H", "MID"])
        while self.alive:
            data = wm.get()

            if data['content']['tickType'] == "MID":
                self.dataMidSent.emit(int  (data['content']['closePrice'    ]),
                                      float(data['content']['chgRate'       ]),
                                      float(data['content']['volumePower'   ]))
            else:
                self.data24Sent.emit(int  (data['content']['closePrice'    ]),
                                     float(data['content']['volume'        ]),
                                     int  (data['content']['highPrice'     ]),
                                     float(data['content']['value'         ]),
                                     int  (data['content']['lowPrice'      ]),
                                     int  (data['content']['prevClosePrice']))

        wm.terminate()

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/overview.ui", self)

        self.ticker = ticker
        self.ovw = OverViewWorker(ticker)
        self.ovw.data24Sent.connect(self.fill24Data)
        self.ovw.dataMidSent.connect(self.fillMidData)
        self.ovw.start()

    def closeEvent(self, event):
        self.ovw.close()

    def fill24Data(self, currPrice, volume, highPrice, value, lowPrice, PrevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_4.setText(f"{volume:,.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value/100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_14.setText(f"{PrevClosePrice:,}")
        # ----------------- 추 가 ------------------
        self.__updateStyle()
        # ------------------------------------------

    def fillMidData(self, currPrice, chgRate, volumePower):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_12.setText(f"{volumePower:.2f}%")
        # ----------------- 추 가 ------------------
        self.__updateStyle()
        # ------------------------------------------

    # ----------------- 추 가 ------------------
    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")
    # ------------------------------------------


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())

