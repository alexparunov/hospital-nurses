#!/usr/bin/python
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

elem_solutions = json.load(open('solutions.json','r'))

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
    return sum(list(map(lambda (i, x): x * (2**i), enumerate(bin_ar))))

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

# Generate at least |2*nurses| solutions so that we can choose

def generate_all_element_solutions(hours, nurses, minHours, maxHours, maxConsec, maxPresence):

    max_number = 0
    for h in range(hours):
        max_number += 2**h

    cpus = mp.cpu_count() - 1

    pool = mp.Pool(processes=cpus)
    all_nums = [i for i in range(1,max_number+1)]
    element_solutions = pool.map(func_generate_solution, all_nums)
    pool.close()

    element_solutions = list(filter(lambda x: solution_is_ok(x, minHours, maxHours, maxConsec, maxPresence) == True, element_solutions))
    for element_solution in element_solutions:
        for i in range(hours - len(element_solution)):
            element_solution.append(0) # appending 0-s

    with open("all_solutions.json","w") as f:
        json.dump(element_solutions, f)

def generate_random_element_solutions(hours, nurses, minHours, maxHours, maxConsec, maxPresence):

    # calculating the upper bound for solution as number. [1,1,1,1,1....#hours]
    max_number = 0
    for h in range(hours):
        max_number += 2**h

    element_solutions = []

    n_sols = 0
    while n_sols <= 2 * nurses:
        # Generate random number as solution
        sol_num = int(math.ceil(np.random.rand() * max_number))
        el_solution = num_to_bin(sol_num)
        for i in range(hours - len(el_solution)):
            el_solution.append(0)  # appending 0-s

        if(solution_is_ok(el_solution, minHours, maxHours, maxConsec, maxPresence)):
            element_solutions.append(solution)
            n_sols += 1

    return element_solutions

def gc(el_solution, demand):
    el_sol = np.array(el_solution)
    dem = np.array(demand)

    updated_demand = np.array(dem - el_sol)
    demand = list(updated_demand)

    # total number of decreased hours in demand (the higher, the better)
    positive_sum = sum(dem) - sum(updated_demand)
    # total number of decreased hours from negative demand[i] values
    #(the lower, the better)
    negative_sum = sum(list(map(lambda (i, x): updated_demand[i] if x <= 0 else 0, enumerate(demand))))
    exp1 = 2**positive_sum
    exp2 = 3**(-negative_sum)
    if exp2 != 0:
        cost = float(exp1) / float(exp2)
    else:
        cost = 0.0

    return(demand, cost)


def is_solved(demand):
    return all(h <= 0 for h in demand)

# Function used in multiprocessing map function to map element solution to
# tuple if (el_sol, cost)


def func_map(i):
    global elem_solutions, demand
    return elem_solutions[i], gc(elem_solutions[i], demand)[1]

def func_generate_solution(num):
    return num_to_bin(num)

def get_grasp_set(elem_solutions_cost, alpha):
    minCost = min(list(map(lambda x: x[1], elem_solutions_cost)))
    maxCost = max(list(map(lambda x: x[1], elem_solutions_cost)))

    grasp_set = list(filter(
        lambda x: x[1] <= minCost + alpha * (maxCost - minCost), elem_solutions_cost))
    return grasp_set


def solve(alpha=0.2):
    global elem_solutions
    global demand
    solution = []
    used_indices = []
    k = 0
    cpus = mp.cpu_count() - 1
    while True:
        if(is_solved(demand)):
            return solution
        elif k >= len(elem_solutions) and not is_solved(demand):
            print("Ooops, no solution was found with a given set of element solutions.")
            return []

        if k < 4:
            pool = mp.Pool(processes=cpus)
            all_indices = [i for i in range(len(elem_solutions))]
            elem_solutions_cost = pool.map(func_map, all_indices)
            pool.close()

        grasp_set = get_grasp_set(elem_solutions_cost, alpha)
        while True:
            randPosGrasp = int(math.floor(np.random.rand() * len(grasp_set)))
            if randPosGrasp not in used_indices:
                solution.append(grasp_set[randPosGrasp][0])
                used_indices.append(randPosGrasp)
                print(demand)
                demand = gc(grasp_set[randPosGrasp][0], demand)[0]
                break
        k += 1

def objective_function_value(solution):
    return sum(map(sum, solution))

def main():

    start_time = timeit.default_timer()
    global nHours, nNurses, minHours, maxHours, maxConsec, maxPresence
    generate_all_element_solutions(nHours, nNurses, minHours, maxHours, maxConsec, maxPresence)
    elapsed = timeit.default_timer() - start_time
    print("Time elapsed",elapsed)

if __name__ == "__main__":
    main()
