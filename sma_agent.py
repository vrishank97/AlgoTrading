from BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time

class SMA_Agent(BaseAgent):
    def __init__(self, cash, window_size, up, down):
        super().__init__(cash, window_size)
        self.up = up
        self.down = down

    def step(self, price):
        self.memory.append(price)
        if len(self.memory)<window_size:
            return 0
        if(price>=mean(self.memory)*(1+up)):
            self.cash += self.stock*price
            self.stock =0
            return -1
        if(price<=mean(self.memory)*(1-down)):
            self.stock += (self.cash)//price
            self.cash -= self.stock*price
            return 1
        return 0