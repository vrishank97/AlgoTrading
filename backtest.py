import pandas as pd

class Backtest:
	def __init__(self, agent):
		self.agent = agent

	def run(self, data):
		results = []
		for price in data:
			self.agent.step(price)
			val = self.agent.getPortfolioVal(price)
			results.append(val)
			print("Portfolio valuation : %f" % (val))
		return results