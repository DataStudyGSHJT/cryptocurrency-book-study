# CH10 나만의 HTS 만들기
## shift+alt+e로 특정 라인만 실행 가능

## PyQt-Chart로 PyQt에 차트 생성
## pip install PyQtChart

###################################
# 10-1. 실시간 현재가 차트
###################################
## 10.1.1. UI레이아웃 설정

## 10.1.2 파이썬에서 기능 연결
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())

## priceView 변수로 QWidget 객체에 접근해서 간단한 라인 차트 그리기
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
# ----------------- 추 가 ------------------
from PyQt5.QtChart import QLineSeries, QChart
# ------------------------------------------

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker
        # ----------------- 추 가 ------------------
        # 라인 차트로 그릴 데이터의 수 정의
        self.viewLimit = 128

        # QLineSeries 객체의 append 메서도로 출력할 데이터의 좌표를 x, y 순서대로 입력
        self.priceData = QLineSeries()
        self.priceData.append(0, 10)
        self.priceData.append(1, 20)
        self.priceData.append(2, 10)

        # 데이터를 차트 객체로 전달해서 시각화
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)

        # 차트를 ui에서 그려놨던 priceView로 출력
        self.priceView.setChart(self.priceChart)
        # ------------------------------------------

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())


## 범례를 제거하고 아티팩트를 제거하기 위한 anti-aliasing을 차트에 적용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QLineSeries, QChart
# ----------------- 추 가 ------------------
from PyQt5.QtGui import QPainter
# ------------------------------------------

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceData.append(0, 10)
        self.priceData.append(1, 20)
        self.priceData.append(2, 10)

        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)

        self.priceView.setChart(self.priceChart)
        # ----------------- 추 가 ------------------
        self.priceChart.legend().hide()
        self.priceView.setRenderHints(QPainter.Antialiasing)
        # ------------------------------------------

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())


## 차트는 X축과 Y축을 명확히 기술해 줘야 올바른 데이터를 출력
## 위 코드는 옵션을 지정하지 않아 기본적으로 생성된 정수형 데이터를 X, Y축에 저장
## 가격 차트는 시간대별로 값이 저장되므로 X축을 날자 객체로 저장하는 것이 시각적인 측면뿐만 아니라 관리 측면에서도 좋음
## 데이터를 append 하느느 코드를 제거하고 X축의 단위를 시간으로 변경
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
# ----------------- 추 가 ------------------
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
# ------------------------------------------

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()

        # ----------------- 추 가 ------------------
        axisX = QDateTimeAxis() # PyChart에서 날짜 축을 관리하는 QDateTimeAxis 객체 생성
        axisX.setFormat("hh:mm:ss") # 날짜는 "시:분:초" 형태로 차트에 표시
        axisX.setTickCount(4) # 차트에 표시할 날짜의 개수 = 4
        dt = QDateTime.currentDateTime() # 현재 시간 정보를 QDateTime 객체로 얻음
        axisX.setRange(dt, dt.addSecs(self.viewLimit)) # X축에 출력될 값의 범위를 현재 시간부터 viewLimit(120)초 이후까지 설정

        # 정수를 저장하는 축을 생성하고 축을 레이브르 차트에 표시하지 않음
        axisY = QValueAxis()
        axisY.setVisible(False)

        # 생성한 X, Y축을 차트와 연결
        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)
        # ------------------------------------------

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())


## 차트에 그릴 데이터를 입력받는 appendData 메서드 추가
## 데이터는 QLineSeries에 viewLimit(120)개까지 저장
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()

        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm:ss")
        axisX.setTickCount(4)
        dt = QDateTime.currentDateTime()
        axisX.setRange(dt, dt.addSecs(self.viewLimit))
        axisY = QValueAxis()
        axisY.setVisible(False)

        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

    # ----------------- 추 가 ------------------
    def appendData(self, currPirce):
        # 정해진 데이터 개수만큼 저장되어 있다면 오래된 0번 인덱스의 데이터를 삭제
        if len(self.priceData) == self.viewLimit :
            self.priceData.remove(0)
        # 현재 시간 정보를 얻어와서 시간과 현재가 (currPrice)를 함께 저장
        # append 메서드는 millisecond (ms)를 입력받기 때문에 MSecsSinceEpoch() 메서드로 QDateTime 객체를 milliesecond로 변환
        dt = QDateTime.currentDateTime()
        self.priceData.append(dt.toMSecsSinceEpoch(), currPirce)
        # 차트의 측정보를 업데이트 하는 __updateAxis() 메서드 호출, 실시간으로 추가되는 데이터의 위치를 지정
        self.__updateAxis()

    def __updateAxis(self):
        # pointsVector 메서드로 QLineSeries 객체에 저장된 데이터를 리스트로 얻어옴
        # pvs에 저장된 리스트 안에는 QPointF 객체로 위치 정보가 저장됨
        pvs = self.priceData.pointsVector()
        # 가장 오래된 0번 인덱스의 객체를 하나 선택해서 x 좌표에 지정된 값을 가져옴
        # x 좌표 데이터가 ms라서 fromMSecsSinceEpoch 메서드로 QDateTime 객체로 변환
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))

        # QLineSeries에 viewLimit(120)만큼 데이터가 꽉 차 있다면 마지막 데이터는 119번인덱스에 저장됨
        if len(self.priceData) == self.viewLimit :
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
        else:
            # 데이터의 개수가 viewLimit 보다 작다면 시작 위치 0번을 기준을 viewLimit 초 이후까지 출력
            dtLast = dtStart.addSecs(self.viewLimit)

        # 앞서 얻어온 위치 정보를 보여줄 수 있도록 X 축 범위 설정
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        # QPointF 객체에서 y좌표를 가져와서 최솟값, 최댓값으로 Y축에 표시될 범위 지정
        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))
    # ------------------------------------------

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.appendData(10)
    import time

    time.sleep(1)
    cw.appendData(20)
    cw.show()
    exit(app.exec_())


## 빗썸 API를 사용해서 1초에 한 번식 현재가를 조회하는 QThread 추가
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
# ----------------- 추 가 ------------------
import time
import pybithumb
from PyQt5.QtCore import QThread, pyqtSignal

# QThread를 상속받으느 PriceWorker 클래스 정의
class PriceWorker(QThread):
    # 메인 스레드에 데이터를 전달하기 위한 dataSent 시그널 정의
    dataSent = pyqtSignal(float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True # QThread를 안전하게 종료하기 위해 인스턴스 변수 사용

    def run(self):
        # 반복해서 현재가를 조회하고 시그널을 메인 스레드에 알림
        while self.alive:
            data  = pybithumb.get_current_price(self.ticker)
            time.sleep(1)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False
# ------------------------------------------

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("D:/Git Repository/cryptocurrency-book-study/CH10/YHS/resource/chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()

        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm:ss")
        axisX.setTickCount(4)
        dt = QDateTime.currentDateTime()
        axisX.setRange(dt, dt.addSecs(self.viewLimit))
        axisY = QValueAxis()
        axisY.setVisible(False)

        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

        # ----------------- 추 가 ------------------
        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()
        # ------------------------------------------

    def appendData(self, currPirce):
        if len(self.priceData) == self.viewLimit :
            self.priceData.remove(0)
        dt = QDateTime.currentDateTime()
        self.priceData.append(dt.toMSecsSinceEpoch(), currPirce)
        self.__updateAxis()

    def __updateAxis(self):
        pvs = self.priceData.pointsVector()
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))
        if len(self.priceData) == self.viewLimit :
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
        else:
            dtLast = dtStart.addSecs(self.viewLimit)
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())