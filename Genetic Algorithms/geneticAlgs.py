import fileReader as fr
import numpy as np
import random
RANDOM_SEED_VALUE = 10
rnd = np.random.RandomState() 

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
        return 0.1


    if(totalWeight > maxWeight): # if overfilled 
        return 0.0

    # 50% score from value proportion, 50% value from filling knapsack as much as possible
    return (float(totalValue) / totalWeight) + (float(totalWeight) / maxWeight)


def mutate(rate, population):
    mutated = []

    for i in range(len(population)):
        for j in range( len(population[i][1])):
            randNum = rnd.rand()
            if( randNum < rate):
                if(population[i][1][j] == 1):
                    population[i][1][j] = 0
                else:
                    population[i][1][j] = 1

    return population


def generatePopulation(popSize, N):
    population = []
    population.append((float(0.0), np.zeros(N, dtype=int)))
    population.append((float(0.0), np.ones(N, dtype=int)))
    for i in range(popSize - 2):
        arr = np.random.randint(2, size=N)
        population.append((float(0.0), arr))

    return population

def generateIntermediatePopulation(population, popSize, N):
    popAverage = 0.0
    for row in population:
       popAverage += row[0]
    popAverage /= popSize

    intermediatePop = []
    #print(popAverage, len(population))
    
    

    for row in population:
        
        randNum = rnd.randint(100)

        fitness = row[0]

        if(fitness != 0):
            intermediatePop.append(row)
        # readd high performers
        if( fitness >= popAverage and randNum > 10):
            for i in range(10):
                    intermediatePop.append(row)
        if( randNum > 95):
            intermediatePop.append(row)

    # get new pop 
    returnPop = []
    # cross over or 25% chance to take parent
    for i in range(popSize // 2):
        pairs = random.choices(intermediatePop, k=2)
        randNum = rnd.randint(4)
        if(randNum == 0):
            returnPop.append(pairs[0])
            returnPop.append(pairs[1])
        else:
            item1 = pairs[0][1]
            item2 = pairs[1][1]

            pivot = rnd.randint(1, N-1)
         
            newItem1 = []
            newItem2 = []
            for i in range(0,pivot):
                newItem1 = newItem1 + [item1[i]]
                newItem2 = newItem2 +  [item2[i]]

            for i in range(pivot, N):
                newItem1 = newItem1 + [item2[i]]
                newItem2 = newItem2 + [item1[i]]

            returnPop.append((pairs[0][0], newItem1))
            returnPop.append((pairs[1][0], newItem2))

    return returnPop


def constructList(binArr, data, n):
    returnList = []
    for i in range(n):
        if( binArr[i] == 1):
            returnList += [data[i]]

    return returnList

def getWeightAndValue(knap, data):
    totWeight = 0
    totVal = 0
    for i in range(len(knap)):
        if(knap[i] == 1):
            totWeight += data[i][1]
            totVal += data[i][2]
    return(totWeight, totVal)
            


def genKnapRunner(fileName):
    fileData = fr.readFileKnap(fileName)

    POPULATION_SIZE = 100
    MUTATION_RATE = 0.005
    NUM_GENERATIONS = 200
    BEST_SELECTION = (-1, [1])

    N = fileData[0]
    maxWeight = fileData[1]
    data = fileData[2]

    population = generatePopulation(POPULATION_SIZE, N)
    population.sort(key=lambda a: a[0], reverse=True)

    BEST_SELECTION = (0.1, np.zeros(N,dtype=int))

    numGenerations = 0
    while(numGenerations < NUM_GENERATIONS):
        for i in range(POPULATION_SIZE):
            fitness = getKnapFitness(N, data, population[i], maxWeight)
            population[i] = (fitness, population[i][1])

        
        population.sort(key=lambda a: a[0], reverse=True)

        if(getWeightAndValue(population[0][1], data)[1] > getWeightAndValue(BEST_SELECTION[1],data)[1]):
            BEST_SELECTION = (population[0][0], (population[0][1]).copy())
            print("Generation: ", numGenerations, " Best Option: ", BEST_SELECTION, getWeightAndValue(BEST_SELECTION[1], data))

        population = generateIntermediatePopulation(population, POPULATION_SIZE, N)

        population = mutate(MUTATION_RATE, population)

        numGenerations += 1
        for i in range(POPULATION_SIZE):
            fitness = getKnapFitness(N, data, population[i], maxWeight)
            population[i] = (fitness, population[i][1])


    print("\n\n\n**************************************************************")
    print("The best selection is: ")
    print(BEST_SELECTION, getWeightAndValue(BEST_SELECTION[1], data))
    print("**************************************************************\n\n\n")

    return (N, maxWeight, constructList(BEST_SELECTION[1], data, N))
    
