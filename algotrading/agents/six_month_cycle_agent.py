from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from itertools import islice

class SixMonthCycle_Agent(BaseAgent):
    def __init__(self, cash, window_size, small, large, signal, up, down):
        super().__init__(cash, window_size)
        self.up = up
        self.down = down
        self.large = large
        self.small = small
        self.signal = signal
        self.window_size = window_size

    def get_macd_signal(self):
        memory_slice = list(islice(self.memory, self.window_size - self.large, self.window_size))
        memory_slice = pd.DataFrame(memory_slice)

        df_memory = pd.DataFrame(memory_slice)
        df_macd = df_memory.ewm(span=self.small, adjust=False).mean() - df_memory.ewm(span=self.large, adjust=False).mean()
        signal = df_macd.ewm(span=self.signal, adjust=False).mean()[0][self.large - 1]

        macd = df_macd[0][self.large - 1]

        if macd >= (1 + self.up)*(signal):
            return "buy"
        elif macd <= (1 - self.down)*(signal):
            return "sell"
        else:
            return "hold"


    def step(self, price, date):
        self.memory.append(price)
        
        if len(self.memory)<self.window_size:
            return 0

        date = list(map(int, date.split("-")))
        month = date[1]

        macd_signal = self.get_macd_signal()

        # Buy in november
        if month > 10 or month < 5 and macd_signal == "buy":
            if(self.cash>price):
                #print("Buying %d stocks for %f each" % ((self.cash)//price, price))
                self.stock += (self.cash)//price
                self.cash -= ((self.cash)//price)*price
                return 1

        # Sell in may
        if month > 4 and month < 11 and macd_signal == "sell":
            if(self.stock>0):
                #print("Selling %d stocks for %f each" % (self.stock, price))
                self.cash += self.stock*price
                self.stock =0
                return -1
        return 0