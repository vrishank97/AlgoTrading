import sys
import os
import numpy as np
from random import randint, random, uniform
from operator import add

from optimise import run_cci, run_sma, run_ema, run_dema, run_tema
from optimise import run_optimisation


def individual():
	return [np.random.randint(5,50), uniform(0.01,0.25), uniform(0.01,0.25)]

def population(count):
	return [ individual() for x in range(0, count) ]

def fitness(individual, algo, year, stock):
	# Insert scoring function here
	mean_sharpe, std_sharpe, mean_sortino, std_sortino = run_optimisation(algo, year, stock, individual[0], individual[1], individual[2])
	return mean_sharpe

def grade(pop, algo, year, stock):
	summed = sum([fitness(x, algo, year, stock) for x in pop])
	return summed / (len(pop) * 1.0)

def evolve(pop, algo, year, stock, retain=0.2, random_select=0.05, mutate=0.01):
	graded = [ (fitness(x, algo, year, stock), x) for x in pop]
	graded = [ x[1] for x in sorted(graded, reverse = True)]
	print(graded[0])
	retain_length = int(len(graded)*retain)
	parents = graded[:retain_length]


	for individual in graded[retain_length:]:
		if random_select > random():
			parents.append(individual)


	for individual in parents:
		if mutate > random():
			pos_to_mutate = np.random.randint(0, 2)
			if pos_to_mutate == 0:
				individual[pos_to_mutate] = np.random.randint(5, 50)
			if pos_to_mutate == 1:
				individual[pos_to_mutate] += np.random.normal(0, 0.025)
			if pos_to_mutate == 2:
				individual[pos_to_mutate] += np.random.normal(0, 0.025)


	parents_length = len(parents)
	desired_length = len(pop) - parents_length
	print(desired_length)
	children = []
	while len(children) < desired_length:
		male = parents[np.random.randint(0, len(parents)-1)]
		female = parents[np.random.randint(0, len(parents)-1)]
		if male != female:
			half = len(male) // 2
			child = male[:half] + female[half:]
			children.append(child)
	parents.extend(children)
	return parents


if __name__ == "__main__":
	if(len(sys.argv) != 6):
		print("Invalid input")
		sys.exit(1)
	algo = sys.argv[1]
	population_count = int(sys.argv[2])
	epochs = int(sys.argv[3])
	year = sys.argv[4]
	stock = sys.argv[5]

	test_function = {
				"cci" : run_cci,
				"sma" : run_sma,
				"ema" : run_ema,
				"dema" : run_dema,
				"tema" : run_tema,
				}

	if algo not in test_function.keys():
		print("Algo %s is not available" %(algo))
		sys.exit(1)

	p = population(population_count)
	fitness_history = [grade(p, algo, year, stock),]
	for i in range(0, epochs):
		print("Epoch: %d" % (i))
		p = evolve(p, algo, year, stock)
		scores = grade(p, algo, year, stock)
		print(scores)
		fitness_history.append(scores)

	for datum in fitness_history:
		print (datum)

	p = evolve(p, algo, year, stock)