#!/usr/bin/python
import math
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('../')

import BRKGA as brkga # BRKGA framework (problem independent)
import DECODER_order as decoder # Decoder algorithm (problem-dependent)
from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)
from parameters import params # Input data (problem-dependent and instance-dependent)
from plot_results import ilp_objective

if len(sys.argv) <= 1:
    sys.stdout.write("Please insert 1 argument as index of parameters array to solve a problem [0-24]\n")
    sys.exit()
else:
    pos = int(sys.argv[1])

best_fitness = ilp_objective[pos]
data = params[pos]

# initializations
numIndividuals=int(config['numIndividuals'])
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]
validFitness = []

bestKnownFit = [best_fitness]
if bestKnownFit:
    bestKnownFit = [best_fitness] * (maxNumGen+1)


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