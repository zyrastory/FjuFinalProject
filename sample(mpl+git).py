import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt 
import random
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc


style.use('ggplot')
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500,0)
        button.resize(140,100)
 
        self.show()
 
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)
        #self.ax1 = fig.add_subplot(211)
        #self.ax2 = fig.add_subplot(212)
 
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        """
        df = pd.read_csv('7-25.csv', parse_dates=True, index_col=0)
        print(df)
        df_ohlc = df['Close'].resample('10D').ohlc()
        df_volume = df['Volume'].resample('10D').sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        #ax1 = self.figure.add_subplot(211)
        #ax2 = self.figure.add_subplot(212)

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()

        candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
        self.draw()
        """
        
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        print(data)
        self.draw()
        """

        
        df = pd.read_csv('7-25.csv')
        #df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean()
        
        df.plot()

        #ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        #ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

        #ax1.plot(df.index, df['Close'])
        #ax1.plot(df.index, df['100ma'])
        #ax2.bar(df.index, df['Volume'])
        print(df.head())
        self.draw()
        
"""


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())