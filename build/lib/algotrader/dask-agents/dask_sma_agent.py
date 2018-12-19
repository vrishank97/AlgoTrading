from .BaseDaskAgent import BaseDaskAgent
import numpy as np
from time import time
import pandas as pd

class SMA_Agent(BaseDaskAgent):
    def __init__(self, cash, window_size, up, down):
        super().__init__(cash, window_size)
        self.up = up
        self.down = down
        self.window_size = window_size
        self.memory = Null
        self.moving_avg = 0

    def step(self, row):
        row = np.array(row)

        if self.memory is Null:
            self.memory = pd.read_csv("dummy.csv")

        if len(self.memory)<self.window_size:
            self.memory.append(row)
            return 0

        self.memory["SMA"]=0

        self.moving_avg = self.memory.loc[len(self.memory)-self.window_size:len(self.memory)]["Close"].mean()

        # Buy
        if(row[5]<=np.mean(self.memory)*(1-self.down)):
            if(self.cash>price):
                #print("Buying %d stocks for %f each" % ((self.cash)//price, price))
                self.stock += (self.cash)//price
                self.cash -= ((self.cash)//price)*price
                self.memory.append((row, self.moving_avg))
                return 1

        # Sell
        if(row[5]>=np.mean(self.memory)*(1+self.up)):
            if(self.stock>0):
                #print("Selling %d stocks for %f each" % (self.stock, price))
                self.cash += self.stock*price
                self.stock =0
                self.memory.append((row, self.moving_avg))
                return -1
        self.memory.append((row, self.moving_avg))
        return 0