import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.six_month_cycle_agent import SixMonthCycle_Agent
from algotrading.evaluation import Evaluation

def test(year, stock):
	filename = "../Historical Data/%s/%s-%s.csv" %(year, stock, year)
	prices = pd.read_csv(filename)["Close"]
	dates = pd.read_csv(filename)["Date"]

	'''
	Parameters for the Six month cycle MACD:
	1. Small EMA (default 12)
	2. Large EMA (default 26)
	3. Signal Line (default 9)
	'''

	agent = SixMonthCycle_Agent(10000, 26, 12, 26, 9, 0.015, 0.015)

	test = Backtest(agent)

	output = test.run(prices, dates)

	# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
	evaluator = Evaluation(prices, output, "Six Month Cycle MACD", "FB")
	evaluator.complete_evaluation()

if __name__ == "__main__":
	test(sys.argv[1], sys.argv[2])