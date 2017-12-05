import random as rnd
import math

def generate_data(scale = 1):
    nNurses = rnd.randint(10,24)*scale
    nHours = 24
    minHours = rnd.randint(1,10)
    maxHours = rnd.randint(minHours+1,24)
    maxConsec = rnd.randint(1,maxHours)
    maxPresence = min(rnd.randint(maxHours, 2*maxHours - 1), 24)
    
    demand = []
    for i in range(0,nHours):
        demand_hours = rnd.randint(1,nNurses)
        demand.append(demand_hours)
    
    return (nNurses, nHours, minHours, maxHours, maxConsec, maxPresence, demand)
    
def main():
    data = generate_data(100)
    print "nNurses=" + str(data[0]) + ";"
    print "nHours=" + str(data[1]) + ";"
    print "minHours=" + str(data[2]) + ";"
    print "maxHours=" + str(data[3]) + ";"
    print "maxConsec=" + str(data[4]) + ";"
    print "maxPresence=" + str(data[5]) + ";"
    print "demand=" + str(data[6]) + ";"
    

if __name__ == "__main__":
    main()
#nNurses = 7;
#nHours = 8;
#minHours = 2;
#maxHours = 5;
#maxConsec = 4;
#demand = [1, 2, 3, 2, 4, 3, 2, 4];
#maxPresence = ;