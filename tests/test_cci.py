import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.cci_agent import CCI_Agent
from algotrading.evaluation import Evaluation

prices = pd.read_csv("../Historical data/DABU Historical Data.csv")["Price"]

agent = CCI_Agent(1000, 25, 0.015, 0.015)

test = Backtest(agent)

output = test.run(prices)

# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
evaluator = Evaluation(prices, output, "CCI", "DABU")
evaluator.complete_evaluation()