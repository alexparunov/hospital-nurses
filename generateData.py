import random as rnd


def generate_data(scale = 1):
    nNurses = rnd.randint(10,24)*scale
    nHours = 24
    minHours = rnd.randint(1,10)
    maxHours = rnd.randint(minHours+1,24)
    maxConsec = rnd.randint(1,maxHours)
    maxPresence = rnd.randint(maxHours, 2*maxHours - 1)
    
    demand = []
    for i in range(0,nHours):
        demand_hours = rnd.randint(1,nNurses)
        demand.append(demand_hours)
    
    return (nNurses, nHours, minHours, maxHours, maxConsec, maxPresence, demand)
    
def main():
    print generate_data()
    
#nNurses = 7;
#nHours = 8;
#minHours = 2;
#maxHours = 5;
#maxConsec = 4;
#demand = [1, 2, 3, 2, 4, 3, 2, 4];
#maxPresence = ;