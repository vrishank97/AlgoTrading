import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.momentum_agent import Momentum_Agent
import matplotlib.pyplot as plt
import numpy as np

prices = pd.read_csv("../Historical data/ICBK Historical Data.csv")["Price"]

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

agent = Momentum_Agent(10000, 150, 20, 150, 5, 20, 80, 12, 26, 9)

test = Backtest(agent)

output = test.run(prices)

fig, ax = plt.subplots()
ax.plot(np.arange(len(prices)), output, color='red')
ax.plot(np.arange(len(prices)), prices, color='green')

ax.set(xlabel='Days', ylabel='INR',
       title='Monies')
ax.grid()
plt.show()