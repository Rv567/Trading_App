import talib as ta


#Momentum Indicators (7)

def ADX(dataFrame): #Average Directional Movement Index
    dataFrame['ADX'] = ta.ADX(dataFrame.High, dataFrame.Low, dataFrame.Close, timeperiod=14)

def MACD(dataFrame):#Moving Average Convergence Divergence
    """
    MACD = fast_MA(12) - slow_MA(26)
    Signal = EMA9(MACD)
    Hist = MACD - Signal
    """
    dataFrame['MACD'],dataFrame['MACD_Signal'],dataFrame['MACD_Hist'] = ta.MACD(dataFrame.Close, fastperiod=12, slowperiod=26, signalperiod=9)

def RSI(dataFrame):#RSI(14)
    dataFrame['RSI'] = ta.RSI(dataFrame.Close,timeperiod=14)

def CCI(dataFrame):#Commodity Channel Index
    dataFrame['CCI'] = ta.CCI(dataFrame.High, dataFrame.Low, dataFrame.Close, timeperiod=14)

def STOCH(dataFrame):#Stochastic
    dataFrame["slowk"], dataFrame["slowd"]= ta.STOCH(dataFrame.High, dataFrame.Low, dataFrame.Close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

def ROC(dataFrame):#((price/prevPrice)-1)*100
    dataFrame["ROC"] = ta.ROC(dataFrame.Close, timeperiod=10)

def WR(dataFrame):#Williams' %R
    dataFrame['WilliamsR'] = ta.WILLR(dataFrame.High,dataFrame.Low,dataFrame.Close,timeperiod=14)


#Overlap Indicators (6)

def BBANDS(dataFrame):#Bollinger Bands
    dataFrame["upperband"], dataFrame["middleband"], dataFrame["lowerband"] = ta.BBANDS(dataFrame.Close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

def DEMA(dataFrame,period):#Double Exponential Moving Average 
    dataFrame["DEMA"]= ta.DEMA(dataFrame.Close, timeperiod=period)

def EMA(dataFrame,period):#Exponential Moving Average
    dataFrame[f"EMA{period}"]= ta.EMA(dataFrame.Close, timeperiod=period)

def MA(dataFrame,period):#Moving Average
    dataFrame[f"MA{period}"]= ta.MA(dataFrame.Close, timeperiod=period, matype=0)

def SAR(dataFrame):#Parabolic SAR
    dataFrame["SAR"]= ta.SAR(dataFrame.High, dataFrame.Low, acceleration=0, maximum=0)

def SMA(dataFrame,period):#Simple Moving Average
    dataFrame[f"SMA{period}"]=ta.SMA(dataFrame.Close, timeperiod=period)

#Volatility Indicators (2)

def ATR(dataFrame):#Average True Range
    dataFrame["ATR"]= ta.ATR(dataFrame.High, dataFrame.Low, dataFrame.Close, timeperiod=14)

def NATR(dataFrame):#Normalized Average True Range
    dataFrame["NATR"]= ta.NATR(dataFrame.High, dataFrame.Low, dataFrame.Close, timeperiod=14)


#Volume Indicators (3)

def AD(dataFrame):#Chaikin A/D Line
    dataFrame["AD"]= ta.AD(dataFrame.High, dataFrame.Low, dataFrame.Close, dataFrame.Volume)

def ADOSC (dataFrame):#Chaikin A/D Oscillator
    dataFrame["ADOSC "]= ta.ADOSC (dataFrame.High, dataFrame.Low, dataFrame.Close, dataFrame.Volume,fastperiod=3, slowperiod=10)

def OBV(dataFrame):#On Balance Volume
    dataFrame["OBV"]= ta.OBV(dataFrame.Close, dataFrame.Volume)