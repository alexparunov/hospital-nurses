# imports
import math
import matplotlib.pyplot as plt
import datetime
import sys

import BRKGA as brkga # BRKGA framework (problem independent)
import DECODER_order as decoder # Decoder algorithm (problem-dependent)
from DATA_1 import data # Input data (problem-dependent and instance-dependent)
from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)

# initializations
numIndividuals=int(config['numIndividuals'])
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]
validFitness = []

bestKnownFit = [1098]
if bestKnownFit:
    bestKnownFit = [1098] * (maxNumGen+1)


# Main body
start = datetime.datetime.now()

chrLength=decoder.getChromosomeLength(data)

population=brkga.initializePopulation(numIndividuals,chrLength)
i=0
while (i<maxNumGen):
    print i
    population = decoder.decode(population,data)
    evol.append(brkga.getBestFitness(population)['fitness'])
    if numElite>0:
        elite, nonelite = brkga.classifyIndividuals(population,numElite)
    else: 
        elite = []
        nonelite = population
    if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
    else: mutants = []
    if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
    else: crossover=[]
    validFitness.append(brkga.getAllValid(population, i, sys.maxint))
    population=elite + crossover + mutants
    i+=1
    print datetime.datetime.now()
    
population = decoder.decode(population, data)
bestIndividual = brkga.getBestFitness(population)
evol.append(bestIndividual['fitness'])
validFitness.append(brkga.getAllValid(population, i, sys.maxint))


finish = datetime.datetime.now()
delta = finish - start
print "start:  " + str(start)
print "finish: " + str(finish)
print "delta:  " + str(delta)
print bestIndividual

flat_list = [item for sublist in validFitness for item in sublist]
res = zip(*flat_list)

if res:
    plt.plot(res[1], res[0], "o")

if bestKnownFit:
    plt.plot(bestKnownFit)

plt.plot(evol)
plt.xlabel('number of generations')
plt.ylabel('Fitness of best individual')
plt.axis([0, len(evol), 0, data["nNurses"]+5])
plt.show()