import stockReader as sr
import numpy as np
import random
RANDOM_SEED_VALUE = 10
rnd = np.random.RandomState(RANDOM_SEED_VALUE) 

def calcSMA(dataRange,):
    return(sum(dataRange) / len(dataRange))
        
# returns true if current day is greater than the simple moving average of n days, returns false if n > len of file data
def simpleMovingAverage(stockData, N):
    index = 0
    currentRange = []

    if(len(stockData) < N + 1):
        return False

    while(index < len(stockData) - 1):
        while(len(currentRange) < N):
            currentRange.append(stockData[index])
            index += 1

        if(stockData[index + 1] > calcSMA(currentRange)):
           return True

        del(currentRange[0])

    return False

# returns true if current day is greater than the exponential moving average of n days, returns false if n > len of file data
def exponentialMovingAverage(stockData, N):
    if(len(stockData < N + 1)):
        return False

# sees if current day is greater than max of previous n days, returns false if n > len of file data
def maximum(stockData, N):
    if(len(stockData < N + 1)):
        return False

# runs input data against 3 rules contained in genotype
def calcFitness(stockData, population):

    for genotypes in population:
        fitPop = []

        # somehow break out the different rules
        ruleBlock = genotypes[1]
        rules = [(False, ruleBlock[0], int(ruleBlock[1:4]), ruleBlock[4]), (False, ruleBlock[5], int(ruleBlock[6:9]), ruleBlock[9]), (False, ruleBlock[10], int(ruleBlock[11:14]), 'end')]

        profit = 0
        availableFunds = 20000

        response = False

        for dataset in stockData:    
            if(availableFunds > 0):
                newRules = []
                for rule in rules:
                    if(rule[2] != 0):
                        if(rule[1] == 's'):
                            newRules.append((simpleMovingAverage(dataset, rule[2]), rule[1], rule[2], rule[3]))
                        elif(rule[1] == 'e'):
                            newRules.append((exponentialMovingAverage(dataset, rule[2]), rule[1], rule[2], rule[3]))
                        elif(rule[1] == 'm'):
                            newRules.append(maximum((dataset, rule[2]), rule[1], rule[2], rule[3]))
                    else:
                        newRules.append((True, rule[1], rule[2], rule[3]))
                if(newRules[0][3] == '&'):
                    response = newRules[0][0] and newRules[1][0]
                elif(newRules[0][3] == '|'):
                    response = newRules[0][0] or newRules[1][0]

                if(newRules[1][3] == '&'):
                    response = response and newRules[2][0]
                elif(newRules[1][3] == '|'):
                    response = response or newRules[2][0]

                # buy and sell stocks
                if(response):
                    totalStock = availableFunds / 10
                    availableFunds = (dataset[-1] - 10) * totalStock
                    print(availableFunds)
                # didn't buy 
                else:
                    availableFunds = availableFunds / 2
            
                # move funds to correct place 
                if(availableFunds > 20000):
                    profit += availableFunds - 20000
                    availableFunds -= (availableFunds - 20000)
                elif(profit > 20000 - availableFunds):
                    profit -= 20000 - availableFunds
                    availableFunds = 20000
                else:
                    availableFunds += profit
                    profit = 0
            # save fitness
        fitPop.append((profit + availableFunds, genotypes[1]))
    return fitPop

                    



def generateIntermediatePopulation():
    print('')

# makes the initial population based off set pop size
def genereatePopulation(popSize):
    population = []

    for i in range(popSize):
        genotype = 's010&s020&s999'
        # something random to generate genotype

        population.append((0.0, genotype))

    return population

def stockRunner():
    POPULATION_SIZE = 1
    stockData = sr.readAllFileStocks()

    population = genereatePopulation(POPULATION_SIZE)
    population = calcFitness(stockData, population)

    print(population)

