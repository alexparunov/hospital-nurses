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

#nNurses=1100;
#nHours=24;
#minHours=6;
#maxHours=18;
#maxConsec=7;
#maxPresence=24;
#demand=[964, 650, 966, 1021, 824, 387, 828, 952, 611, 468, 403, 561, 862, 597, 1098, 855, 918, 1016, 897, 356, 615, 670, 826, 349];

filename = 'jsons/all_solutions_{}.json'.format(nHours)
elem_solutions = json.load(open(filename,'r'))

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

# Generates all solutions
def generate_all_element_solutions(hours, nurses, minHours, maxHours, maxConsec, maxPresence, filename):

    max_number = 0
    for h in range(hours):
        max_number += 2**h

    cpus = mp.cpu_count() - 1

    pool = mp.Pool(processes=cpus)
    all_nums = [i for i in range(1,max_number+1)]
    element_solutions = pool.map(func_generate_solution, all_nums)
    pool.close()

    element_solutions = list(map(lambda x: solution_is_ok(x, minHours, maxHours, maxConsec, maxPresence) == True, element_solutions))
    for element_solution in element_solutions:
        for i in range(hours - len(element_solution)):
            element_solution.append(0) # appending 0-s

    with open(filename,"w") as f:
        json.dump(element_solutions, f)

    return element_solutions

# Generate at least |2*nurses| random solutions so that we can choose

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


def solve(alpha=0.3):
    global elem_solutions, demand, nHours, nNurses
    solution = []
    used_indices = []
    k = 0
    cpus = mp.cpu_count() - 1
    while k < nNurses:
        if(is_solved(demand)):
            return solution

        if k % nHours == 0:
            pool = mp.Pool(processes=cpus)
            all_indices = [i for i in range(len(elem_solutions))]
            elem_solutions_cost = pool.map(func_map, all_indices)
            pool.close()

        grasp_set = get_grasp_set(elem_solutions_cost, alpha)
        randPosGrasp = int(math.floor(np.random.rand() * len(grasp_set)))
        if randPosGrasp not in used_indices:
            if len(grasp_set) == 0:
                return []
            solution.append(grasp_set[randPosGrasp][0])
            used_indices.append(randPosGrasp)
            elem_solutions_cost.remove(grasp_set[randPosGrasp])
            #print(demand)
            demand = gc(grasp_set[randPosGrasp][0], demand)[0]
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
    for hour in range(1,25):
        filename = "jsons/all_solutions_{}.json".format(hour)
        elem_sol = generate_all_element_solutions(hour, nNurses, minHours, maxHours, maxConsec, maxPresence, filename)

def generate_one_json(hour):
    filename = "jsons/all_solutions_{}.json".format(hour)
    start_time = timeit.default_timer()
    elem_sol = generate_all_element_solutions(hour, nNurses, minHours, maxHours, maxConsec, maxPresence, filename)
    elapsed = timeit.default_timer() - start_time
    print("{} solutions generated for nHours = {} in {} secs.".format(len(elem_sol), hour, np.round(elapsed*1000)/1000))

def main():
    global nHours, nNurses, minHours, maxHours, maxConsec, maxPresence

    start_time = timeit.default_timer()
    solution = solve(0.35)
    elapsed = timeit.default_timer() - start_time
    
    if len(solution) > 0:
        print("Solution found in {} secs with objective cost: {}".format(np.round(elapsed*1000)/1000, objective_function_value(solution)))
        print_solution(solution)
if __name__ == "__main__":
    main()
