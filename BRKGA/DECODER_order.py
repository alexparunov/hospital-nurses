import sys
import logging
import math



logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


def getChromosomeLength(data):
    return int(data["nHours"])


def decode(population, data):
    for ind in population:
        solution, fitness=decoder_order(data,ind['chr'])
        ind['solution']=solution
        ind['fitness']=fitness    
    return(population)


def start_end(nurse):
    start, end = -1,-1
    for i in xrange(len(nurse)):
        if nurse[i] == 1:
            start = i
            break
    for i in reversed(xrange(len(nurse))):
        if nurse[i] == 1:
            end = i
            break
    return start, end

# check that nurse doesn't work more than maxConsec hours
def max_consec(nurse, maxConsec):
    consec = 0
    for i in xrange(len(nurse)):
        if nurse[i]:
            consec +=1
        else:
            consec = 0
        if consec > maxConsec:
            logging.info("fail in maxConsec")
            return False
    return True

# check that there is no assignment that will later cause two consecutive rest hours
# example: maxConsec = 3:
#          0001110011100 - we cannot "fix" the two consecutive rest in this assignment
#
def consec_and_rest(nurse, maxConsec):
    start, end = start_end(nurse)
    consec = 0
    consecPrev = -1
    consecNext = -1
    for i in range(start, end+1):
        if nurse[i]:
            consec += 1
        else:
            consec = 0

        if consec == maxConsec:
            if consecPrev == -1:
                consecPrev = i
            else:
                consecNext = i - maxConsec
            if consecNext != -1 and consecPrev != -1:
                if consecNext - consecPrev == 2:
                    #print "illegal consec rest combination"
                    return False
                else:
                    consecPrev = i
                    consecNext = -1
    return True


# check that the nurse doesn't stay in the hospital more than maxPresence hours.
def max_presence(nurse, maxPresence):
    start, end = start_end(nurse)
    logging.info("Start: %s End: %s", str(start), str(end))
    if end - start + 1 > maxPresence:
        logging.info("fail in maxPresence")
        return False
    return True

# check that the nurse don't work more then maxHours in total.
# also check that the presence time doesn't exceed maxHours + maxPresence*0.15
# this part is heuristic choice.
def max_hours(nurse, maxHours, maxPresence):
    if sum(nurse) > maxHours:
        return False

    start, end = start_end(nurse)

    logging.info("Start: %s End: %s", str(start), str(end))
    if end - start > math.ceil(maxHours + maxPresence*0.15):
        logging.info("fail in maxHours")
        return False
    return True

# check that the nurse can work in the new hour and all the constrains are satisfied.
def can_work(nurse, hour, constraints):
    if nurse[hour] == 1:
        return False
    nurse[hour] = 1
    if not max_consec(nurse, constraints["maxConsec"]) or not max_presence(nurse, constraints["maxPresence"]) or \
            not max_hours(nurse, constraints["maxHours"], constraints["maxPresence"]) or not consec_and_rest(nurse, constraints["maxConsec"]):
        return False
    return True


# legalizing the nurse work working hour.
# make sure she doesn't rest for more than 1 consecutive hour
# make sure she have the minimum working hours.
def legalize_nurse(nurse, constraints):

    minHours = constraints["minHours"]
    start, end = start_end(nurse)
    hours = len(nurse)

    for i in range(start, end):
        if i+2 < end and nurse[i] == 0 and nurse[i+1] == 0 and nurse[i+2] == 0 and \
                can_work(list(nurse), i+1, constraints):
            nurse[i+1] = 1
        elif nurse[i] == 0 and nurse[i+1] == 0:
            if can_work(list(nurse), i, constraints):
                nurse[i] = 1
            elif can_work(list(nurse), i+1, constraints):
                nurse[i+1] = 1

    total = sum(nurse)

    minConst = True if total >= minHours else False

    idx = 1
    while not minConst and start + idx < hours:
        if can_work(list(nurse), start+idx, constraints):
            nurse[start+idx] = 1
            total += 1
            if total >= minHours:
                minConst = True
                break
        idx += 1

    idx = 1
    while not minConst and end - idx >= 0:
        if can_work(list(nurse), end - idx, constraints):
            nurse[end - idx] = 1
            total += 1
            if total >= minHours:
                minConst = True
                break
        idx += 1

    if not minConst:
        #print "cannot satisfy min constraints"
        return False

    start, end = start_end(nurse)
    for i in range(start, end):
        if nurse[i] == 0 and nurse[i+1] == 0:
            #print "fail in rest"
            return False
    return True

# Iterate over all the working nurses and legalize their timetable.
def legalize(sol, used, constraints):
    for nrs in xrange(sum(used)):
        if not legalize_nurse(sol[nrs], constraints):
            return False
    return True

def decoder_order(data,chromosome):

    demand = list(data["demand"])
    nurses = data["nNurses"]

    # sol - nurses x hours table
    sol = [[0 for x in range(len(demand))] for y in range(nurses)]

    # used[i] = 1 : nurse i is working at least 1 hr
    used = [0] * nurses

    chr_demand = chromosome[0:len(demand)]
    task_order = sorted(range(len(chr_demand)), key=lambda k: chr_demand[k], reverse=True)

    for demIdx in task_order:
        if demand[demIdx] <= 0:
            continue
        for nrs in xrange(nurses):
            if can_work(list(sol[nrs]), demIdx, data):
                used[nrs] = 1
                sol[nrs][demIdx] = 1
                demand[demIdx] -= 1
                # Heuristic : Go to the neighbors of the current hour with steps of 2:
                #               -> if the neighbor is inside the working interval and
                #                   -> if the demand of the neighbor is bigger than half of current demand.
                #                       -> try to assign the nurse to the neighbor
                start, end = start_end(sol[nrs])
                for i in range(1, int(data["maxConsec"]), 2):
                    if True and demIdx - i > start and demand[demIdx - i] >= demand[demIdx]/2 and\
                            can_work(list(sol[nrs]), demIdx - i, data):
                        sol[nrs][demIdx - i] = 1
                        demand[demIdx - i] -= 1
                    if demIdx + i < end and demand[demIdx + i] >= demand[demIdx]/2 and \
                            can_work(list(sol[nrs]), demIdx + i, data):
                        sol[nrs][demIdx + i] = 1
                        demand[demIdx + i] -= 1
            if demand[demIdx] <= 0:
                break
    #print used
    #print "total working nurses = " + str(sum(used))
    # for i in xrange(nurses): print sol[i]
    for i in demand:
        if i > 0:
            #print demand
            #print "Failed to satisfy the demand"
            return None, sys.maxint

    if legalize(sol, used, data):
        return sol, sum(used)
    # for i in xrange(nurses): print sol[i]

    return None, sys.maxint
