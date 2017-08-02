import talib
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.figure import Figure

style.use('ggplot')

def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = pd.ewma(price,span=fastperiod)
    ewma60 = pd.ewma(price,span=slowperiod)
    dif = ewma12-ewma60
    dea = pd.ewma(dif,span=signalperiod)
    bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


df = pd.read_csv('7-25.csv', parse_dates=True, index_col=0)

df_ohlc = df['Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)


ax1.xaxis_date()
ax2.xaxis_date()

#ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
for label in ax3.xaxis.get_ticklabels():   
	label.set_rotation(45)

candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='r',colordown='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0,color='#0080FF')

macd, signal, hist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
mydif,mydea,mybar = myMACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
#fig = plt.figure(figsize=[18,5])
plt.plot(df.index,macd,label='macd dif')
plt.plot(df.index,signal,label='signal dea')
#plt.plot(df.index,hist,label='hist bar')
#plt.plot(df.index,mydif,label='my dif')
#plt.plot(df.index,mydea,label='my dea')
#plt.plot(df.index,mybar,label='my bar')
#plt.legend(loc='best')

plt.show()
