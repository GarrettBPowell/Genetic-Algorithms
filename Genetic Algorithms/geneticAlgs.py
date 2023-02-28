import fileReader as fr
import numpy as np
import random
RANDOM_SEED_VALUE = 10
rnd = np.random.RandomState(RANDOM_SEED_VALUE) 

def getKnapFitness(N, data, binArr, maxWeight):
    totalWeight = 0
    totalValue = 0

    i = 0
    for row in data:
        if( binArr[1][i] == 1):
            totalWeight += row[1]
            totalValue += row[2]
        i += 1

    if(totalWeight == 0 and totalValue == 0):
        return 0.0

    # want to fill knap as much as possible without overfilling 
    adjWeight = totalWeight

    if(totalWeight > maxWeight): # if overfilled it will give a score of 0
        adjWeight = 0


    # 50% score from value proportion, 50% value from filling knapsack as much as possible
    return (totalValue / totalWeight) + (adjWeight / maxWeight)


def mutate(rate, population):
    hundScale = int(rate * 100)
    for row in population:
        for item in row[1]:
            randNum = rnd.randint(100)
            if( randNum < hundScale):
                if(item == 1):
                    item = 0
                else:
                    item = 1


def generatePopulation(popSize, N):
    population = []
    for i in range(popSize):
        arr = np.random.randint(2, size=N)
        population.append((float(0.0), arr))

    return population

def generateIntermediatePopulation(population, popSize):
    popAverage = 0.0
    for row in population:
       popAverage += row[0]
    popAverage /= popSize

    intermediatePop = []

    for i in range(10):
        intermediatePop.append(population[i])


    for row in population:
        randNum = rnd.randint(100)

        if(row[0] > 3 * popAverage):
            intermediatePop.append(row)
        if(row[0] > 2 * popAverage and randNum > 25):
            intermediatePop.append(row)
        if(row[0] > popAverage and randNum > 50):
            intermediatePop.append(row)
        if(row[0] > .75 * popAverage and randNum > 75):
            intermediatePop.append(row)

    while(len(intermediatePop) < 100):
        intermediatePop.append(population[rnd.randint(100)])

    # get new pop 
    returnPop = []

    # cross over or 25% chance to take parent
    for i in range(popSize):
        pairs = random.choices(population, k=2)
        randNum = rnd.randint(4)
        if(randNum == 0):
            returnPop.append(pairs[0])
            returnPop.append(pairs[1])
        else:
            item1 = pairs[0][1]
            item2 = pairs[1][1]

            pivot = rnd.randint(1, len(item1)-1)
         

            newItem1 = item1[0:pivot]
            for x in item2[pivot::1]:
                newItem1 + [x]

            newItem2 = item2[0:pivot]
            for x in  item1[pivot::1]:
                newItem2 + [x]

            returnPop.append((pairs[0][0], newItem1))
            returnPop.append((pairs[1][0], newItem2))

    return returnPop


def genKnapRunner(fileName):
    fileData = fr.readFileKnap(fileName)

    POPULATION_SIZE = 100
    MUTATION_RATE = 0.05
    NUM_GENERATIONS = 200

    N = fileData[0]
    maxWeight = fileData[1]
    data = fileData[2]

    population = generatePopulation(100, N)


    numGenerations = 0
    while(numGenerations < NUM_GENERATIONS):
        for i in range(POPULATION_SIZE):
            fitness = getKnapFitness(N, data, population[i], maxWeight)
            population[i] = (fitness, population[i][1])
        
        population.sort(key=lambda a: a[0], reverse=True)
        print("Generation: ", numGenerations, " Best Option: ", population[0])
        newPop = generateIntermediatePopulation(population, POPULATION_SIZE)

        mutate(MUTATION_RATE, newPop)

        numGenerations += 1

    population.sort(key=lambda a: a[0], reverse=True)


    print("**************************************************************")
    print("The best selection is: ")
    print(population[0])

    return (N, maxWeight, population[0][1])
    
