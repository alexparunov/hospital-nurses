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

    for j in range(hours - 1, -1, step=-1):
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
	return [[(0, 0) for j in range(nHours)] for i in range(nNurses)]

# Greedy Cost function. Return cost and updated demand.

def gc(cost_matrix, demand):
	# nNurses
	for i in range(len(cost_matrix)):
		# nHours
		for j in range(len(cost_matrix[0])):
			costNotAssigned = math.exp(-demand[j])
			if(demand[j] <= 0):	
				costAssigned = math.exp(-demand[j] - 1)
			else:
				costAssigned = math.exp(-demand[j] + 1)

			# We want to choose minimum between those costs
			cost = (1/costNotAssigned, 1/costAssigned)
			cost_matrix[i][j] = cost

	return cost_matrix

def is_solved(demand):
    return all(h <= 0 for h in demand)


def solve():
	global demand, nNurses, nHours, minHours, maxHours, maxConsec, maxPresence

	# Solution matrix 
	solution = np.zeros((nNurses, nHours), dtype=int)
	elem_sol_matrix = generate_element_solution_matrix(nHours, nNurses)
	cost_matrix = generate_cost_matrix(nHours, nNurses)
	greedy_cost = gc2(cost_matrix, demand)
	
	for i in range(nNurses):
		for j in range(nHours):