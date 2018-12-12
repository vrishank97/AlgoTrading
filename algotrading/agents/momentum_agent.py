from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time
from itertools import islice
from collections import deque

'''
Parameters for the Moving Momentum algorithm:
1. Small SMA (default 20)
2. Large SMA (default 150)
3. Stochastic oscillator sensitivity (default 14)
4. Stochastic oscillator oversold threshold (default below 20)
5. Stochastic oscillator overbought threshold (default above 80)
6. Small EMA (default 12)
7. Large EMA (default 26)
8. Signal Line (default 9)
'''

class Momentum_Agent(BaseAgent):
    def __init__(self, cash, window_size, small_sma=20, large_sma=150, stoch_osc_days=14, stoch_osc_oversold=20, stoch_osc_overbought=80, small_ema=12, large_ema=26, signal_ema=9):
        super().__init__(cash, window_size)
        self.window_size = window_size
        self.small_sma = small_sma
        self.large_sma = large_sma
        self.stoch_osc_days = stoch_osc_days
        self.stoch_osc_oversold = stoch_osc_oversold
        self.stoch_osc_overbought = stoch_osc_overbought
        self.small_ema = small_ema
        self.large_ema = large_ema
        self.signal_ema = signal_ema
        self.running_ema_small = 0
        self.running_ema_large = 0
        self.running_ema_signal = 0

        self.multiplier_small = 2/(small_ema + 1)
        self.multiplier_large = 2/(large_ema + 1)
        self.multiplier_signal = 2/(signal_ema + 1)

        self.macd_memory = deque(maxlen=self.signal_ema)

    def get_sma(self, window):
        memory_slice = list(islice(self.memory, self.window_size - window, self.window_size))
        return np.mean(memory_slice)

    def get_stoch_osc(self, days):
        memory_slice = list(islice(self.memory, self.window_size - days, self.window_size))
        min_price = np.min(memory_slice)
        max_price = np.max(memory_slice)
        curr_price = memory_slice[-1]

        return ((curr_price - min_price)*100)/(max_price - min_price)

    def get_macd_hist(self, small, large, signal, price):
        memory_slice = list(islice(self.memory, self.window_size - large, self.window_size))
        memory_slice = pd.DataFrame(memory_slice)

        #print(price, self.running_ema_small,self.running_ema_large, self.running_ema_signal)

        runnner_small = None
        runner_large = None
        runner_signal = None

        if(self.running_ema_small == 0):
            runner_small = self.get_sma(small)
        else:
            runner_small = self.running_ema_small

        if(self.running_ema_large == 0):
            runner_large = self.get_sma(large)
        else:
            runner_large = self.running_ema_large

        if(self.running_ema_signal == 0 and len(self.macd_memory) > 0):
            runner_signal = np.mean(self.macd_memory)
        else:
            runner_signal = self.running_ema_signal

        self.running_ema_small = (price - runner_small)*self.multiplier_small + runner_small
        self.running_ema_large = (price - runner_large)*self.multiplier_large + runner_large
        macd = self.running_ema_small - self.running_ema_large
        self.running_ema_signal = (macd - runner_signal)*self.multiplier_signal + runner_signal

        self.macd_memory.append(macd)

        if(len(self.macd_memory) < self.signal_ema):
            return 0

        return (self.running_ema_small - self.running_ema_large) - self.running_ema_signal

    def step(self, price):
        self.memory.append(price)

        if len(self.memory)<self.window_size:
            return 0

        trading_bias = self.get_sma(self.small_sma) - self.get_sma(self.large_sma)
        stoch_osc = self.get_stoch_osc(self.stoch_osc_days)
        macd_hist = self.get_macd_hist(self.small_ema, self.large_ema, self.signal_ema, price)

        #print("Trading bias = " + str(trading_bias) + ", stochastic_osc = " + str(stoch_osc) + ", and macd_histogram = " + str(macd_hist))
        #if(macd_hist > 0):
        #    print("POSITIVE")

        if(trading_bias > 0 and stoch_osc < 20 and macd_hist > 0):
            if(self.cash>price):
                print("Buying %d stocks for %f each" % ((self.cash)//price, price))
                self.stock += (self.cash)//price
                self.cash -= ((self.cash)//price)*price
                return 1

        if(trading_bias < 0 and stoch_osc > 80 and macd_hist < 0):
            if(self.stock>0):
                print("Selling %d stocks for %f each" % (self.stock, price))
                self.cash += self.stock*price
                self.stock =0
                return -1

        return 0

