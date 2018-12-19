import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
#import matplotlib
#matplotlib.use("Tkagg")
import matplotlib.pyplot as plt
import numpy as np
import os


prices = pd.read_csv("../Historical data/2017/CIPLA-2017.csv")["Open"]
agent = SMA_Agent(10, 0.015, 0.015)
test = Backtest(agent, 10000, logging=True, ticker="CIPLA")
output = test.run(prices)
fig, ax = plt.subplots()
ax.plot(np.arange(len(prices)), output, color='red')
ax.plot(np.arange(len(prices)), prices, color='green')

ax.set(xlabel='Days', ylabel='INR',
       title="CIPLA")
ax.grid()
plt.show()

print(test.logstore.read('CIPLA').data)