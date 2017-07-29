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
        self.ax1 = fig.add_subplot(211)
        self.ax2 = fig.add_subplot(212)
        

    def test(self,num):
        df = pd.read_csv('7-25.csv', parse_dates=True, index_col=0)
        #print(df)
        print("收到"+str(num))


        df_ohlc = df['Close'].resample(str(num)+"D").ohlc()
        df_volume = df['Volume'].resample(str(num)+"D").sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        #self.ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        #self.ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=self.ax1)
        self.ax1.xaxis_date()

        candlestick_ohlc(self.ax1, df_ohlc.values, width=5, colorup='g')
        self.ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


