import pandas as pd
import quandl
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.ema_agent import EMA_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window=10, up=0.05, down=0.05, get_plots=True, verbose=True):
	quandl.ApiConfig.api_key = "FDEDsMbK1E2t_PMf7X3M"
	df = quandl.get('NSE/ZEEL', start_date='2017-01-01', end_date='2017-12-31')
	prices = df["Close"]
	dates = df["Date"]

	agent = EMA_Agent(window, up, down)

	test = Backtest(agent, 10000)

	output = test.run(prices)

	# class Evaluation takes for initialization - prices, output, name of algorithm, name of security

	evaluator = Evaluation(prices, dates, output, "EMA", stock)
	return evaluator.complete_evaluation(get_plots, verbose)


if __name__ == "__main__":
	test(sys.argv[1], sys.argv[2])
