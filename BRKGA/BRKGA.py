import math
import numpy as np

def initializePopulation(numIndividuals, chrLength):
    population=[]
    for i in range(numIndividuals):
        chromosome= list(np.random.rand(chrLength))
        population.append({'chr':chromosome, 'solution':{},'fitness':None})
    return(population)
        
def classifyIndividuals(population, numElite):
    fitness=np.array([e['fitness'] for e in population])
    order=sorted(range(len(fitness)), key=lambda k: fitness[k])
    whichElite=order[0:numElite]
    whichNonElite=order[numElite:(len(fitness))]
    population=np.array(population)
    elite=population[whichElite]
    nonElite=population[whichNonElite]
    return list(elite), list(nonElite)
    
def generateMutantIndividuals(numMutants, chrLength):
    mutants=[]
    for i in range(numMutants):
        chromosome= list(np.random.rand(chrLength))
        mutants.append({'chr':chromosome, 'solution':{},'fitness':None})
    return mutants

 
def doCrossover(elite,nonelite,ro,numCrossover):
    crossover=[]
    for i in range(numCrossover):
        indexElite=int(math.floor(np.random.rand()*len(elite)))
        indexNonElite=int(math.floor(np.random.rand()*len(nonelite)))
        chrElite=elite[indexElite]['chr']
        chrNonElite=nonelite[indexNonElite]['chr']
        rnd=list(np.random.rand(len(chrElite)))
        chrCross=[chrElite[i] if rnd[i]<= ro else chrNonElite[i] for i in range(len(chrElite))]
        crossover.append({'chr':chrCross, 'solution':{},'fitness':None})
    return crossover
    
def getBestFitness(population):
    fitness=np.array([e['fitness'] for e in population])
    print fitness
    order=sorted(range(len(fitness)), key=lambda k: fitness[k])
    print order
    return population[order[0]]

def getAllValid(population,iter, maxVal):
    fitness = np.array([e['fitness'] for e in population])
    valid = []
    for val in fitness:
        if val < maxVal:
            valid.append((val, iter))
    return valid
