#!/usr/bin/python
import numpy as np
import math
import json
import timeit

hours = 10
nurses = 100

# solution represented as binary array [0,1,1,0,...#hours] 
def num_to_bin(num = 0):
	bin_ar = []
	while num != 0:
		bin_ar.append(num % 2)
		num = int(num/2)

	return bin_ar

# solution represented as number. one-to-one correspondence between binary array and number
def bin_to_num(bin_ar):
    return sum(list(map(lambda (i,x): x*(2**i), enumerate(bin_ar))))

# check for constraints
def solution_is_ok(solution = [], minHours = 0, maxHours = 0, maxConsec = 0, maxPresence = 0):
	if(sum(solution) < minHours): return False
	if(sum(solution) > maxHours): return False

	# maximum consecutive hours constraint
	hours = len(solution)
	s = 0
	for sol in solution:
		if sol == 0:
			s = 0
		else:
			s += sol

		if s > maxConsec:
			return False

	# first and last positions of 1 in solution binary array
	first_pos = 0
	last_pos = hours-1

	for i in range(hours/2):
		if solution[i] == 1:
			first_pos = i
			break

	for j in range(hours-1, hours/2-1, -1):
		if solution[j] == 1:
			last_pos = j
			break

	if last_pos - first_pos >= maxPresence:
		return False

	# No rest for more than 2 consecutive hours
	s = 0
	for sol in solution[first_pos:last_pos+1]:
		if s >=2 and sol != 0:
			return False

		if sol == 1:
			s = 0
		else:
			s += 1

	return True

# Generate at least |2*nurses| solutions so that we can choose
def generate_solutions(hours = 0, nurses = 0, minHours = 0, maxHours = 0, maxConsec = 0, maxPresence = 0):

	# calculating the upper bound for solution as number. [1,1,1,1,1....#hours]
	max_number = 0
	for h in range(hours):
		max_number += 2**h

	solutions = []

	n_sols = 0
	while n_sols <= 2*nurses:
		# Generate random number as solution
		sol_num = int(math.ceil(np.random.rand()*max_number))
		solution = num_to_bin(sol_num)
		for i in range(hours-len(solution)):
			solution.append(0) #appending 0-s
		
		if(solution_is_ok(solution, minHours, maxHours, maxConsec, maxPresence)):
			solutions.append(solution)
			n_sols += 1 

	return solutions

# Greedy Cost function. Return cost and updated demand.
def gc(solution = [], demand = []):
	sol = np.array(solution)
	dem = np.array(demand)

	updated_demand = np.array(dem - sol)
	return(updated_demand, sum(dem) - sum(updated_demand))

def is_solved(demand = []):
	hours = len(demand)

	for h in range(hours):
		if demand[h] > 0:
			return False

	return True

def solve(elem_solutions = [], demand = []):
	solution = []
	k = 0
	while k <= 10:
		if is_solved(demand):
			return solution
		elif k >= len(elem_solutions) and not is_solved(demand):
			print("Oops, no solution was found, from given set of element solutions.")
			return []

		solution_cost = [(el,gc(el, demand)[1]) for el in elem_solutions]
		solution_cost.sort(key = lambda x: x[1], reverse = True)
		print(solution_cost[:10])
		
		k += 1
		

def main():
	nNurses = 100000;
	nHours = 8;
	minHours = 2;
	maxHours = 5;
	maxConsec = 4;
	demand = [1, 2, 3, 2, 4, 3, 2, 4];
	maxPresence = 5;

	start_time = timeit.default_timer()
	#sols = generate_solutions(nHours, nNurses, minHours, maxHours, maxConsec, maxPresence)
	elapsed = timeit.default_timer() - start_time

	#with open('solutions.json', 'w') as f:
		#json.dump(sols, f)
		#print(len(sols),"solutions generated in:",elapsed,"secs")
	
	elem_solutions = json.load(open('solutions.json','r'))
	solve(elem_solutions, demand)

if __name__ == "__main__":
	main()
