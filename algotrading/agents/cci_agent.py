from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time

class CCI_Agent(BaseAgent):
    def __init__(self, cash, window_size, up, down):
        super().__init__(cash, window_size)
        self.up = up
        self.down = down
        self.window_size = window_size

    def step(self, price):
        self.memory.append(price)
        if len(self.memory)<self.window_size:
            return 0

        CCI = (price - np.mean(self.memory))/(0.015*np.std(self.memory))

        # Buy
        if(CCI>100):
            if(self.cash>price):
                #print("Buying %d stocks for %f each" % ((self.cash)//price, price))
                self.stock += (self.cash)//price
                self.cash -= ((self.cash)//price)*price
                return 1

        # Sell
        if(CCI<(-100)):
            if(self.stock>0):
                #print("Selling %d stocks for %f each" % (self.stock, price))
                self.cash += self.stock*price
                self.stock =0
                return -1
        return 0