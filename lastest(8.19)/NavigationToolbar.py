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


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: PyQt with matplotlib')
        self.create_menu()
        self.create_main_frame()
        
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        #self.axes = self.fig.add_subplot(111)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        df = pd.read_csv('./cache/8-11.csv', parse_dates=True, index_col=0)

        df_ohlc = df['Close'].resample('10D').ohlc()
        df_volume = df['Volume'].resample('10D').sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date Time'] = df_ohlc['Date Time'].map(mdates.date2num)
        self.ax1.xaxis_date()

        candlestick_ohlc(self.ax1, df_ohlc.values, width=5, colorup='g')
        self.ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        
        hbox = QHBoxLayout()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        #quit_action = self.create_action("&Quit", slot=self.close, 
        #    shortcut="Ctrl+Q", tip="Close the application")
        
        #self.add_actions(self.file_menu, 
        #    ( None, quit_action))
        
"""
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
"""

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()
    
if __name__ == "__main__":
    main()