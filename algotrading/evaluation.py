import sys
sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np

class Evaluation:
	def __init__(self, prices, output, algo, security):
		self.prices = prices
		self.output = output
		self.algo = algo
		self.security = security

	def plot_output(self, scaling_factor=1):
		fig, ax = plt.subplots()
		ax.plot(np.arange(len(self.prices)), self.output, color='red')
		ax.plot(np.arange(len(self.prices)), self.prices*scaling_factor, color='green')

		ax.set(xlabel='Days', ylabel='INR',
		       title='Monies')
		ax.grid()
		plt.show()

	def complete_evaluation(self, price_scaling_factor=1):
		self.plot_output(price_scaling_factor)
