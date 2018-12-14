import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
from algotrading.evaluation import Evaluation

prices = pd.read_csv("../Historical data/2017/ADANIPORTS-2017.csv")["Close"]

agent = SMA_Agent(10000, 10, 0.015, 0.015)

test = Backtest(agent)

output = test.run(prices)

# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
evaluator = Evaluation(prices, output, "SMA", "DABU")
evaluator.complete_evaluation()