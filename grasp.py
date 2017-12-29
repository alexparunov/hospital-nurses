#!/usr/bin/python3
import numpy as np
import math
import json
import timeit
import multiprocessing as mp
import pickle
import sys
import os

nNurses = 20
nHours = 8
minHours = 2
maxHours = 5
maxConsec = 4
maxPresence = 5
demand = [1, 2, 3, 2, 4, 3, 2, 4]

#nNurses=1800;
#nHours=24;
#minHours=6;
#maxHours=18;
#maxConsec=7;
#maxPresence=24;
#demand=[964, 650, 966, 1021, 824, 387, 828, 952, 611, 468, 403, 561, 862, 597, 1098, 855, 918, 1016, 897, 356, 615, 670, 826, 349];

# element solution represented as binary array [0,1,1,0,...#hours]


def num_to_bin(num):
	bin_ar = []
	while num != 0:
		bin_ar.append(num % 2)
		num = int(num / 2)

	return bin_ar

# element solution represented as number. One-to-one correspondence
# between binary array and number


def bin_to_num(bin_ar):
	return sum(list(map(lambda ix: ix[1] * (2**ix[0]), enumerate(bin_ar))))

def progress(count, total, status=''):
	bar_len = 60
	filled_len = int(round(bar_len*count/float(total)))
	
	percents = round(100*count/float(total),1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)
	
	sys.stdout.write("[{0}] {1}% ...{2}\r".format(bar, percents, status))
	sys.stdout.flush()

# check for constraints


def solution_is_ok(el_solution, minHours, maxHours, maxConsec, maxPresence):
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

# Generates all element solutions solutions for all hours. (Need to generate once)

def generate_all_element_solutions(hour, filename):

	max_number = 2**hour - 1

	cpus = mp.cpu_count() - 1

	pool = mp.Pool(processes=cpus)
	all_nums = [i for i in range(1,max_number+1)]
	element_solutions = pool.map(func_generate_solution, all_nums)
	pool.close()

	for element_solution in element_solutions:
		for i in range(hour - len(element_solution)):
			element_solution.append(0) # appending 0-s

	with open(filename,"w") as f:
		json.dump(element_solutions, f)

	return element_solutions

def filter_all_element_solutions(minHours, maxHours, maxConsec, maxPresence, filename):
	global nHours
	if not os.path.exists(filename):
		generate_all_element_solutions(nHours, filename)

	element_solutions = json.load(open(filename,'r'))

	element_solutions = list(filter(lambda x: solution_is_ok(x, minHours, maxHours, maxConsec, maxPresence) == True, element_solutions))

	return element_solutions

# Generate at least |2*nurses| random solutions so that we can choose

def generate_random_element_solutions(hours, nurses, minHours, maxHours, maxConsec, maxPresence):

	
	# calculating the upper bound for solution as number. [1,1,1,1,1....#hours]
	max_number = 2**hours - 1
	element_solutions = []

	n_sols = 0
	while n_sols <= 4 * nurses:
		# Generate random number as solution
		sol_num = int(math.ceil(np.random.rand() * max_number))
		el_solution = num_to_bin(sol_num)
		for i in range(hours - len(el_solution)):
			el_solution.append(0)  # appending 0-s

		if(solution_is_ok(el_solution, minHours, maxHours, maxConsec, maxPresence)):
			element_solutions.append(el_solution)
			n_sols += 1

	return element_solutions
 
def gc(el_solution, demand):
	el_sol = np.array(el_solution)
	dem = np.array(demand)

	pos_hits_map_func = lambda h: 1 if (demand[h] > 0 and el_solution[h] == 1) else 0
	neg_hits_map_func = lambda h: 1 if (demand[h] <= 0 and el_solution[h] == 1) else 0

	# number of times we decrease from positive value of demand
	positive_hits = sum(list(map(pos_hits_map_func, range(len(demand)))))

	# number of times we decrease from negative value of demand
	negative_hits = sum(list(map(neg_hits_map_func, range(len(demand)))))

	demand = np.array(dem - el_sol)

	# The final goal of our greedy cost function is to have more positive hits than negative hits
	# We first calculate the difference between positive and negative hits
	# Then we exponentiate this difference, which means the higher/lower is difference, the higher/lower is cost
	# After that we reciprocate exponentiated difference, since we are looking for minimal cost
	# In other words, max(exp(hits_difference)) = min(exp(-hit_difference))

	hits_difference = positive_hits - negative_hits
	cost = math.exp(-hits_difference)
	#print(positive_hits, negative_hits, cost)
	return(demand, cost)


def is_solved(demand):
	return all(h <= 0 for h in demand)

# Function used in multiprocessing map function to map element solution to
# tuple of (el_sol, cost)


def func_map(elem_solution):
	global demand
	return elem_solution, gc(elem_solution, demand)[1]

def func_generate_solution(num):
	return num_to_bin(num)

def get_grasp_set(elem_solutions_cost, alpha):
	minCost = min(list(map(lambda x: x[1], elem_solutions_cost)))
	maxCost = max(list(map(lambda x: x[1], elem_solutions_cost)))

	grasp_set = list(filter(
		lambda x: x[1] <= minCost + alpha * (maxCost - minCost), elem_solutions_cost))
	return grasp_set

def local_search(candidate_element, elem_solutions_cost, demand, alpha, nHours):
	maxDistance = math.sqrt(nHours)*(1-alpha)

	distance_func = lambda x: math.sqrt(sum(np.power((np.array(x[0]) - np.array(candidate_element)),2))) <= maxDistance
	neighborhood = list(filter(distance_func, elem_solutions_cost))

	for neighbor in neighborhood:
		gc_neighbor = gc(neighbor[0], demand)[1]
		gc_candidate = gc(candidate_element, demand)[1]
		if gc_neighbor < gc_candidate:
			candidate_element = neighbor[0]
	
	return candidate_element


def solve(alpha=0.35, debug = False):
	global demand, nHours, nNurses, minHours, maxHours, maxConsec, maxPresence

	# For total hours < 20 the below given method is way faster and more optimal
	# Otherwise we need to generate random element solutions

	if(nHours < 20):
		filename = "jsons/all_solutions_{}.json".format(nHours)
		elem_solutions = filter_all_element_solutions(minHours, maxHours, maxConsec, maxPresence, filename)
	else:
		elem_solutions = generate_random_element_solutions(nHours, nNurses, minHours, maxHours, maxConsec, maxPresence)

	solution = []
	k = 0
	cpus = mp.cpu_count() - 1

	while k < nNurses:
		if(is_solved(demand)):
			return solution

		if k % nHours == 0:
			pool = mp.Pool(processes=cpus)
			elem_solutions_cost = pool.map(func_map, elem_solutions)
			pool.close()

		# Constructive Phase. Here we construct RCL.
		grasp_set = get_grasp_set(elem_solutions_cost, alpha)
		randPosGrasp = int(math.floor(np.random.rand() * len(grasp_set)))
		
		if len(grasp_set) == 0:
			return []

		# Candidate Element for solution
		candidate_element = grasp_set[randPosGrasp][0]
		if debug:
			print("Candidate Element Before: {}".format(candidate_element))

		# Perform local search in a neighborhood of candidate element
		candidate_element = local_search(candidate_element, elem_solutions_cost, demand, alpha, nHours)
		
		if debug:
			print("Candidate Element After : {}".format(candidate_element))

		solution.append(candidate_element)
		if debug:
			print("Iteration: {} / {}: ".format(k+1, nNurses))
			print("Demand: {}".format(demand))
		demand = gc(candidate_element, demand)[0]
		k += 1

	return []

def objective_function_value(solution):
	return len(solution)

def print_solution(solution):
	for i in range(len(solution)):
		for j in range(len(solution[0])):
			print(solution[i][j], sep = " ", end=" ")
		print()

def generate_all_jsons():
	for hour in range(1,20):
		filename = "jsons/all_solutions_{}.json".format(hour)
		start_time = timeit.default_timer()
		elem_sol = generate_all_element_solutions(hour, filename)
		elapsed = timeit.default_timer() - start_time
		print("{} solutions generated for nHours = {} in {} secs.".format(len(elem_sol), hour, np.round(elapsed*1000)/1000))

def generate_one_json(hour):
	filename = "jsons/all_solutions_{}.json".format(hour)
	start_time = timeit.default_timer()
	elem_sol = generate_all_element_solutions(hour, filename)
	elapsed = timeit.default_timer() - start_time
	print("{} solutions generated for nHours = {} in {} secs.".format(len(elem_sol), hour, np.round(elapsed*1000)/1000))

def serialize_json(hour):
	filename = "jsons/all_solutions_{}.json".format(hour)
	data = json.load(open(filename, 'r'))

	with open('pickles/all_solutions_{}.pkl'.format(hour),'wb') as f:
		pickle.dump(data, f)
		print("Successfully serialized {}".format(filename))

def deserialize_pickle(hour):
	filename = "pickles/all_solutions_{}.pkl".format(hour)
	data = pickle.load(open(filename, 'rb'))
	
	return data

def main():
	global nHours, nNurses, minHours, maxHours, maxConsec, maxPresence

	start_time = timeit.default_timer()
	solution = solve(0.5, debug = True)
	elapsed = timeit.default_timer() - start_time
	
	if len(solution) > 0:
		print("Solution found in {} secs with objective cost: {}".format(np.round(elapsed*1000)/1000, objective_function_value(solution)))
		print_solution(solution)
	else:
		print("Solution not found... Time elapsed: {} secs".format(np.round(elapsed*1000)/1000))

def debug():
	temp = json.load(open('jsons/all_solutions_19.json','r'))
	print(len(temp))

if __name__ == "__main__":
	main()
	#debug()
