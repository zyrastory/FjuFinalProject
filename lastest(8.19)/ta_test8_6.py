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

import sys, os, random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
import matplotlib.pyplot as plt
import datetime as dt

style.use('ggplot')


class Figure_Canvas(QMainWindow):   
#通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None):
        #fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: PyQt with matplotlib')
        
    
    def myMACD(self,price, fastperiod=12, slowperiod=26, signalperiod=9):
        self.ewma12 = pd.ewma(price,span=fastperiod)
        self.ewma60 = pd.ewma(price,span=slowperiod)
        dif = self.ewma12-self.ewma60
        dea = pd.ewma(dif,span=signalperiod)
        bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,bar    
    
    def test(self,num,a,b,tc):

        Tocsv(num,a,b) #連接到sql2csv
        if num=="中石化":
            c='bbb'
        if num=="台泥":
            c='aaa'
        csvname = "0_"+c+"_"+a+"_"+b
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312,sharex=self.ax1)
        self.ax3 = self.fig.add_subplot(313,sharex=self.ax1)
        
        df = pd.read_csv('./cache/'+csvname+".csv", parse_dates=True, index_col=0)
        #print("收到"+str(num))

        #df_ohlc = df['Close'].resample("10D").ohlc()
        #df_volume = df['Volume'].resample("10D").sum()

        df_ohlc = df['Close'].resample(str(tc)+"D").ohlc()
        df_volume = df['Volume'].resample(str(tc)+"D").sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date Time'] = df_ohlc['Date Time'].map(mdates.date2num)

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
        
        #self.ax3.plot(df.index,hist,label='hist bar')
        #self.ax3.plot(df.index,mydif,label='my dif')
        #self.ax3.plot(df.index,mydea,label='my dea')
        #self.ax3.plot(df.index,mybar,label='my bar')
        

        self.ax3.legend(loc='best')
        
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        hbox = QHBoxLayout()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)


        