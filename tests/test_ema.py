import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.ema_agent import EMA_Agent
import matplotlib.pyplot as plt
import numpy as np

prices = pd.read_csv("../Historical data/GE Historical Data.csv")["Price"]

agent = EMA_Agent(10000, 10, 0.05, 0.05)

test = Backtest(agent)

output = test.run(prices)

fig, ax = plt.subplots()
ax.plot(np.arange(len(prices)), output, color='red')
ax.plot(np.arange(len(prices)), prices*33, color='green')

ax.set(xlabel='Days', ylabel='INR',
       title='Monies')
ax.grid()
plt.show()