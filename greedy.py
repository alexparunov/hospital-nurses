import logging
import random as rnd
import math

DEBUG = True


class HospitalData:
    def __init__(self, nNurses, nHours,minHours, maxHours, maxConsec, maxPresence, ndemand):
        self.nurses = nNurses
        self.hours = nHours
        self.minH = minHours
        self.maxH = maxHours
        self.consec = maxConsec
        self.presence = maxPresence
        self.demand = list(ndemand)
        self.c_demand = list(ndemand)

    def c_print(self):
        print self.nurses
        print self.hours
        print self.minH
        print self.maxH
        print self.consec
        print self.presence
        print self.demand

    def update_demand(self, res):
        for i in xrange(self.hours):
            self.demand[i] -= res[i]


class NurseData:
    def __init__(self, hd):
        self.minH = hd.minH
        self.maxH = hd.maxH
        self.consec = hd.consec
        self.c_consec = hd.consec
        self.presence = hd.presence

#    def init_self(self, minHours, maxHours, maxConsec, maxPresence):
#        self.minH = minHours
#        self.maxH = maxHours
#        self.consec = maxConsec
#        self.c_consec = maxConsec
#        self.presence = maxPresence

    def dec(self):
        self.minH -= 1
        self.maxH -= 1
        self.consec -= 1

    def reset_consec(self):
        self.consec = self.c_consec

    def c_print(self):
        print self.minH
        print self.maxH
        print self.consec
        print self.presence


def print_worktable(wt):
    if DEBUG:
        for n in wt:
            print n


def print_used(u):
    if DEBUG:
        print u

def min_hours(nrs, ref):
    count = 0
    for i in nrs:
        count += i
    if count >= ref.minH:
        return "PASS"
    return "Fail, the nurse works " + str(count) + "insted of min" + str(ref.minH)

def max_hours(nrs, ref):
    count = 0
    for i in nrs:
        count += i
    if count <= ref.maxH:
        return "PASS"
    return "Fail, the nurse works " + str(count) + "insted of max" + str(ref.maxH)

def consec_hours(nrs, ref):
    count = 0
    for i in nrs:
        if count > ref.consec:
            return "Fail, the nurse works " + str(count) + " consec hours, insted of max" + str(ref.consec) + " consec hours"
        if i:
            count += i
        else:
            count = 0
    return "PASS"

def max_presence(nrs, ref):
    first = -1
    last = -1
    for i,v in enumerate(nrs):
        if v == 1 and first == -1:
            first = i
            last = i
        if v == 1 and i > last:
            last = i

    if last - first < ref.presence:
        return "Pass"
    return "Fail, the nurse exceed the max presence in the hospital" + str(last - first) + "insted of max" + str(ref.presence)

def is_legal(worktable, hospital, used):
    for idx,nrs in enumerate(worktable):
        if not used[idx]:
            continue
        ref_nurse = NurseData(hospital)
        print "min hour constrain:" + min_hours(nrs, ref_nurse)
        print "max hour constrain:" + max_hours(nrs, ref_nurse)
        print "consec hour constrain:" + consec_hours(nrs, ref_nurse)
        print "max presence hour constrain:" + max_presence(nrs, ref_nurse)
    for id, val in enumerate(hospital.c_demand):
        count = 0
        for n in range(hospital.nurses):
            count += worktable[n][id]
        #print hospital.c_demand
        #print hospital.demand
        #print "needed: " + str(val) + " actual: " + str(count)
        if count < val:
            print "FAIL: there are missing nurses in the " + str(id) + " hour"


def nurse_constrains(startIdx, nurse, hours):
    vec = []
    for i in range(0, startIdx):
        vec.append(0)
    vec.append(1)
    nurse.dec()
    for i in range(startIdx + 1, min(startIdx + nurse.presence, hours)):
        if vec[i - 1] == 1 and nurse.consec > 0:
            vec.append(1)
            nurse.dec()
        elif vec[i - 1] == 1 and nurse.consec == 0:
            vec.append(0)
            nurse.reset_consec()
        elif vec[i - 1] == 0 and nurse.maxH > 0:
            vec.append(1)
            nurse.dec()

        if nurse.maxH == 0:
            break
    if nurse.minH > 0:
        #TODO: need to take care of the case that min > max_consec, in that case we can't just give more working hour before.
        #print "minumum constrain before:" + str(vec)
        for i in range(0, nurse.minH+1):
            vec[startIdx-i] = 1
        #print "minimum constrain after :" + str(vec)

    if hours != len(vec):
        for i in range(0, hours - len(vec)):
            vec.append(0)
    return vec


def assignment(hospital):
    used = []
    worktable = []
    for n in range(0, hospital.nurses):
        used.append(0)
        worktable.append([])
        for h in range(0, hospital.hours):
            worktable[n].append(0)

    for n in xrange(hospital.nurses):  # for nurse in nurses
        print "nurse #" + str(n)
        nurse = NurseData(hospital)
        d = 0
        demand = False
        for ind in xrange(hospital.hours):
            if hospital.demand[ind] > 0:
                demand = True
                d = ind
                break
        if not demand:
            print "the demanded hours are fulfill!"
            break
        res = nurse_constrains(d, nurse, hospital.hours)
        if not res:
            print "the minimum constrain doesn't met"
            break
        worktable[n] = res
        used[n] = 1
        # update demanded:
        print "demand before:" + str(hospital.demand)
        print "          res:" + str(res)
        hospital.update_demand(res)
        print "demand after :" + str(hospital.demand)


    is_legal(worktable, hospital, used)
    print_worktable(worktable)
    print_used(used)


def generate_data(scale=1):
    nNurses = rnd.randint(10, 24) * scale
    nHours = 24
    minHours = rnd.randint(1, 10)
    maxHours = rnd.randint(minHours + 1, 24)
    maxConsec = rnd.randint(1, maxHours)
    maxPresence = min(rnd.randint(maxHours, 2 * maxHours - 1), 24)

    demand = []
    for i in range(0, nHours):
        demand_hours = rnd.randint(1, nNurses)
        demand.append(demand_hours)

    return (nNurses, nHours, minHours, maxHours, maxConsec, maxPresence, demand)


def main():
    data = [7,  # nNurses
              8,  # nHours
              2,  # minHours
              5,  # maxHours
              3,  # maxConsec
              6,  # maxPresence
              [1, 2, 3, 2, 4, 3, 2, 4]  # demand
              ]
    # [7, 8, 2, 5, 3, 6, [1, 2, 3, 2, 4, 3, 2, 4]]
    hospital = HospitalData(7, 8, 2, 5, 3, 6, [1, 2, 3, 2, 4, 3, 2, 4])
    nurse = NurseData(hospital)

    hospital.c_print()
    nurse.c_print()

    assignment(hospital)

    # print "nNurses=" + str(data[0]) + ";"
    # print "nHours=" + str(data[1]) + ";"
    # print "minHours=" + str(data[2]) + ";"
    # print "maxHours=" + str(data[3]) + ";"
    # print "maxConsec=" + str(data[4]) + ";"
    # print "maxPresence=" + str(data[5]) + ";"
    # print "demand=" + str(data[6]) + ";"


if __name__ == "__main__":
    main()
# nNurses = 7;
# nHours = 8;
# minHours = 2;
# maxHours = 5;
# maxConsec = 4;
# demand = [1, 2, 3, 2, 4, 3, 2, 4];
# maxPresence = ;