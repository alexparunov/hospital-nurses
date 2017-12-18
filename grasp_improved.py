#!/usr/bin/python3
import numpy as np
import math
import json
import timeit
import multiprocessing as mp


nNurses = 20
nHours = 8
minHours = 2
maxHours = 5
maxConsec = 4

maxPresence = 5

demand = [1, 2, 3, 2, 4, 3, 2, 4]


def solution_is_ok(el_solution=[], minHours=0, maxHours=0, maxConsec=0, maxPresence=0):
	if(sum(el_solution) < minHours):
		return False
	if(sum(el_solution) > maxHours):
		return False

	hours = len(el_solution)
	# maximum consecutive hours constraint
	s = 0
	for el_sol in el_solution:
		if el_sol == 0:
			s = 0
		else:
			s += el_sol

		if s > maxConsec:
			return False

	# first and last positions of '1' in element solution binary array
	first_pos = 0
	last_pos = hours - 1

	for i in range(hours):
		if el_solution[i] == 1:
			first_pos = i
			break

	for j in range(hours - 1, -1, -1):
		if el_solution[j] == 1:
			last_pos = j
			break

	if last_pos - first_pos >= maxPresence:
		return False

	# No rest for more than 2 consecutive hours
	s = 0
	for el_sol in el_solution[first_pos:last_pos + 1]:
		if s >= 2 and el_sol != 0:
			return False

		if el_sol == 1:
			s = 0
		else:
			s += 1

	return True

# Cost Matrix for each nurse and hour. (notAssigned, assigned)


def generate_cost_matrix(nHours, nNurses):
	return [[(0, 0) for h in range(nHours)] for n in range(nNurses)]

# Greedy Cost function. Return cost and updated demand.

def gc(cost_matrix, demand):
	global nNurses, nHours

	for n in range(nNurses):
		for h in range(nHours):
			costNotAssigned = math.exp(-demand[h])
			if(demand[h] <= 0):
				costAssigned = math.exp(-demand[h] - 1)
			else:
				costAssigned = math.exp(-demand[h] + 1)

			cost = (1 / costNotAssigned, 1 / costAssigned)
			cost_matrix[n][h] = cost
	return cost_matrix

def is_solved(demand):
	return all(h <= 0 for h in demand)

def objective_function_value(solution):
	return sum(map(sum, solution))

def solve():
	global demand, nNurses, nHours, minHours, maxHours, maxConsec, maxPresence

	# Solution matrix
	solution = np.zeros((nNurses, nHours), dtype=int)
	cost_matrix = generate_cost_matrix(nHours, nNurses)

	max_iterations = 100  # maximum number of iterations
	k = 0
	while k < max_iterations:
		if is_solved(demand):
			return solution
		print(demand)
		cost_matrix = gc(cost_matrix, demand)
		
		optimal_cost_matrix = np.zeros((nHours, nNurses))
		optimal_cost_matrix = [[(cost_matrix[n][h][0],0) if cost_matrix[n][h][0] < cost_matrix[n][h][1] else (cost_matrix[n][h][1],1) for h in range(nHours)] for n in range(nNurses)]
		optimal_cost_matrix = np.array(optimal_cost_matrix)

		
		minCost = optimal_cost_matrix.min()
		maxCost = optimal_cost_matrix.max()
		#print(minCost, maxCost)
		alpha = 0.35

		# Get set of arguments where value of cost satisfies GRASP criteria based on alpha
		grasp_matrix_arguments = np.argwhere(optimal_cost_matrix[0] <= minCost + alpha*(maxCost - minCost))
		#print(grasp_matrix_arguments)
		# Random position from grasp matrix set of arguments
		
		gm_pos = math.floor(np.random.rand()*len(grasp_matrix_arguments))
		nurse = grasp_matrix_arguments[gm_pos][0]
		hour = grasp_matrix_arguments[gm_pos][1]
		#print(nurse, hour)
		
		solution[nurse][hour] = int(optimal_cost_matrix[nurse][hour][1])
		el_solution = solution[nurse]
		el_solution_ok = solution_is_ok(el_solution, minHours, maxHours, maxConsec, maxPresence)
		#if not el_solution_ok:
		#	solution[nurse][hour] = 0 # unassign
		demand[hour] -= 1
		k += 1

	# print('Full solutions was not found in {} iterations.\nPartial solution with objective value {} is:'.format(
	  #  k, objective_function_value(solution)))
	# print(solution)
	return solution


def main():
	solve()
if __name__ == "__main__":
	main()
