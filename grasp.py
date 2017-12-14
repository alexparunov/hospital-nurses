#!/usr/bin/python
import numpy as np
import math
import json
import timeit

hours = 10
nurses = 100

# element solution represented as binary array [0,1,1,0,...#hours] 
def num_to_bin(num = 0):
	bin_ar = []
	while num != 0:
		bin_ar.append(num % 2)
		num = int(num/2)

	return bin_ar

# element solution represented as number. One-to-one correspondence between binary array and number
def bin_to_num(bin_ar):
    return sum(list(map(lambda (i,x): x*(2**i), enumerate(bin_ar))))

# check for constraints
def solution_is_ok(el_solution = [], minHours = 0, maxHours = 0, maxConsec = 0, maxPresence = 0):
	if(sum(el_solution) < minHours): return False
	if(sum(el_solution) > maxHours): return False

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
	last_pos = hours-1

	for i in range(hours):
		if el_solution[i] == 1:
			first_pos = i
			break

	for j in range(hours-1, -1, step = -1):
		if el_solution[j] == 1:
			last_pos = j
			break

	if last_pos - first_pos >= maxPresence:
		return False

	# No rest for more than 2 consecutive hours
	s = 0
	for el_sol in el_solution[first_pos:last_pos+1]:
		if s >=2 and el_sol != 0:
			return False

		if el_sol == 1:
			s = 0
		else:
			s += 1

	return True

# Generate at least |2*nurses| solutions so that we can choose
def generate_element_solutions(hours = 0, nurses = 0, minHours = 0, maxHours = 0, maxConsec = 0, maxPresence = 0):

	# calculating the upper bound for solution as number. [1,1,1,1,1....#hours]
	max_number = 0
	for h in range(hours):
		max_number += 2**h

	element_solutions = []

	n_sols = 0
	while n_sols <= 2*nurses:
		# Generate random number as solution
		sol_num = int(math.ceil(np.random.rand()*max_number))
		el_solution = num_to_bin(sol_num)
		for i in range(hours-len(el_solution)):
			el_solution.append(0) #appending 0-s
		
		if(solution_is_ok(el_solution, minHours, maxHours, maxConsec, maxPresence)):
			element_solutions.append(solution)
			n_sols += 1 

	return element_solutions

# Greedy Cost function. Return cost and updated demand.
def gc(el_solution = [], demand = []):
	sol = np.array(el_solution)
	dem = np.array(demand)

	updated_demand = np.array(dem - sol)
	return(updated_demand, 1/(sum(dem) - sum(updated_demand)))

def is_solved(demand = []):
	return any(h <= 0 for h in demand)

def solve(elem_solutions = [], demand = []):
	solution = []
	k = 0
	while k <= 4:
		if is_solved(demand):
			return solution
		elif k >= len(elem_solutions) and not is_solved(demand):
			print("Oops, no solution was found, from given set of element solutions.")
			return []

		el_solutions_cost = [(el,gc(el, demand)[1]) for el in elem_solutions]
		print(el_solutions_cost)
        # minCost = 
        # maxCost = 
        # alphaP = 0.4
        #filtered_el_solutions_cost = list(filter(lambda x: x[1] <= minCost + alphaP*(maxCost - minCost), el_solutions_cost))
        
        #filtered_len = len(filtered_el_solutions_cost)
        #f_pos = math.floor(np.random.rand()*filtered_len)
		
        #demand = filtered_el_solutions_cost[f_pos][0]
		

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
