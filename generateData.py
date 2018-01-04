#!/usr/bin/python3
import random as rnd
import math
import sys

def generate_data(scale = 1):
    nNurses = rnd.randint(10,24)*scale
    nHours = 24
    minHours = rnd.randint(1,10)
    maxHours = rnd.randint(minHours+1,24)
    maxConsec = rnd.randint(1,maxHours)
    maxPresence = min(rnd.randint(maxHours, 2*maxHours - 1), 24)
    
    demand = []
    for i in range(0,nHours):
        demand_hours = rnd.randint(1,math.floor(0.7*nNurses))
        demand.append(demand_hours)
    
    return (nNurses, nHours, minHours, maxHours, maxConsec, maxPresence, demand)
    
def main():

    if(len(sys.argv) > 1):
        scale = int(sys.argv[1])
        data = generate_data(scale)
        data_str = ""
        data_str += "nNurses=" + str(data[0]) + ";\n"
        data_str += "nHours=" + str(data[1]) + ";\n"
        data_str += "minHours=" + str(data[2]) + ";\n"
        data_str += "maxHours=" + str(data[3]) + ";\n"
        data_str += "maxConsec=" + str(data[4]) + ";\n"
        data_str += "maxPresence=" + str(data[5]) + ";\n"
        data_str += "demand=" + str(data[6]) + ";\n"

        data_str2 = ""
        data_str2 += "'nNurses':" + str(data[0]) + ",\n"
        data_str2 += "'nHours':" + str(data[1]) + ",\n"
        data_str2 += "'minHours':" + str(data[2]) + ",\n"
        data_str2 += "'maxHours':" + str(data[3]) + ",\n"
        data_str2 += "'maxConsec':" + str(data[4]) + ",\n"
        data_str2 += "'maxPresence':" + str(data[5]) + ",\n"
        data_str2 += "'demand':" + str(data[6]) + "\n"

        print(data_str)
        print(data_str2)
    else:
        print("Scale argument needed.")
    

if __name__ == "__main__":
    main()