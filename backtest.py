import pandas as pd

class Backtest:
	def __init__(self, agent):
		self.agent = agent

	def run(self, data):
		for prices in data:
			self.agent.step(prices)