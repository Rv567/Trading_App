from Functions.mylibraries import *


#MAcross strategy
class SmaCross(Strategy):
    # Define the two moving averages
    n1 = 50  # Short-term moving average
    n2 = 200  # Long-term moving average

    def init(self):
        # Precompute the two moving 
        close = self.data.Close
        self.sma1 = self.I(ta.sma,pd.Series(close) , self.n1)
        self.sma2 = self.I(ta.sma, pd.Series(close), self.n2)

    def next(self):
        # If short MA crosses above long MA, buy the asset
        if crossover(self.sma1, self.sma2):
            self.buy()

        # Conversely, if short MA crosses below long MA, sell it
        elif crossover(self.sma2, self.sma1):
            self.position.close()


#MAcross strategy with stop loss
class SmaCross_StopLoss(Strategy):
        # Define the two moving averages
        n1 = 50  # Short-term moving average
        n2 = 200  # Long-term moving average
        trailing_stop = 5

        def init(self):
            # Precompute the two moving 
            close = self.data.Close
            self.sma1 = self.I(ta.sma,pd.Series(close) , self.n1)
            self.sma2 = self.I(ta.sma, pd.Series(close), self.n2)

        def next(self):
            buy_signals = 0
            
            if crossover(self.sma1, self.sma2):
                buy_signals += 1

            if buy_signals == 1 and not self.position:
                self.buy()
                self.highest_price = self.data.Close[-1] # Highest price is initialized by the last close

            elif self.position:
                # Inside the position taken we update the highest price
                if self.data.Close[-1] > self.highest_price:
                    self.highest_price = self.data.Close[-1]

                # Trailing stop loss
                trailing_stop = self.highest_price * (1 - self.trailing_stop/100)  # 5% trailing stop
                if self.data.Close[-1] < trailing_stop:
                    self.position.close()
                    self.highest_price = None

#3 out of 4 startegy
class MultiIndicatorStrategy(Strategy):
    # Define the Indicator parameters
    n_rsi = 14
    level_rsi = 30
    n_sma = 50
    n_atr = 14
    trailing_stop = 2

    def init(self):
        high = self.data.High
        low = self.data.Low
        close = self.data.Close
        volume = self.data.Volume

        self.rsi = self.I(ta.rsi, pd.Series(close),self.n_rsi)
        self.sma = self.I(ta.sma, pd.Series(close),self.n_sma)
        self.atr = self.I(ta.atr, pd.Series(high), pd.Series(low), pd.Series(close),self.n_atr)
        self.ad = self.I(ta.ad, pd.Series(high), pd.Series(low), pd.Series(close), pd.Series(volume))
    
    def next(self):
        buy_signals = 0
        
        if self.rsi[-1] < self.level_rsi:
            buy_signals += 1
        if self.data.Close[-1] > self.sma[-1]:
            buy_signals += 1
        if self.atr[-1] > self.atr[-2]:
            buy_signals += 1
        if self.ad[-1] > self.ad[-2]:
            buy_signals += 1
        
        if buy_signals >= 3 and not self.position:
            self.buy()
            self.highest_price = self.data.Close[-1] # Highest price is initialized by the last close

        elif self.position:
            # Inside the position taken we update the highest price
            if self.data.Close[-1] > self.highest_price:
                self.highest_price = self.data.Close[-1]

            # Trailing stop loss
            trailing_stop = self.highest_price * (1 - self.trailing_stop/100)  # 5% trailing stop
            if self.data.Close[-1] < trailing_stop:
                self.position.close()
                self.highest_price = None
                buy_signals = 0