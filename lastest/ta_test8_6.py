import talib
import numpy as np
import pandas as pd
import datetime as dt
from sql2csv import Tocsv

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.dates as mdates
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
style.use('ggplot')


class Figure_Canvas(FigureCanvas):   
#通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        #self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.ax1 = fig.add_subplot(311)
        self.ax2 = fig.add_subplot(312)
        self.ax3 = fig.add_subplot(313)

        Tocsv()
    
    def myMACD(self,price, fastperiod=12, slowperiod=26, signalperiod=9):
        self.ewma12 = pd.ewma(price,span=fastperiod)
        self.ewma60 = pd.ewma(price,span=slowperiod)
        dif = self.ewma12-self.ewma60
        dea = pd.ewma(dif,span=signalperiod)
        bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,bar    
    
    def test(self):
        
        df = pd.read_csv('8-7.csv', parse_dates=True, index_col=0)
        #print(df)
        #print("收到"+str(num))


        df_ohlc = df['Close'].resample("10D").ohlc()
        df_volume = df['Volume'].resample("10D").sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        #self.ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        #self.ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=self.ax1)
        self.ax1.xaxis_date()

        candlestick_ohlc(self.ax1, df_ohlc.values, width=5, colorup='g')
        self.ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        for label in self.ax3.xaxis.get_ticklabels():   
            label.set_rotation(45)

        macd, signal, hist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        mydif,mydea,mybar = self.myMACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        self.ax3.plot(df.index,macd,label='macd dif')
        self.ax3.plot(df.index,signal,label='signal dea')
        """
        self.ax3.plot(df.index,hist,label='hist bar')
        self.ax3.plot(df.index,mydif,label='my dif')
        self.ax3.plot(df.index,mydea,label='my dea')
        self.ax3.plot(df.index,mybar,label='my bar')
        """

        self.ax3.legend(loc='best')
        
