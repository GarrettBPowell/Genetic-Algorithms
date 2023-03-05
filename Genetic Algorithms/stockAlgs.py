import stockReader as sr
import numpy as np
import random 

RANDOM_SEED_VALUE = 10
rnd = np.random.RandomState(RANDOM_SEED_VALUE) 

def calcSMA(dataRange):
    return(sum(dataRange) / len(dataRange))
        
# returns true if current day is greater than the simple moving average of n days, returns false if n > len of file data
def simpleMovingAverage(stockData, N):
    index = 0
    currentRange = []
    length = len(stockData) - 1
    if(len(stockData) <= N):
        return False

    while(index < length):
        while(index < length and len(currentRange) < N):
            currentRange.append(stockData[index])
            index += 1
        if(index >= length):
            return False

        if(stockData[index + 1] > calcSMA(currentRange)):
           return True

        del(currentRange[0])

    return False

def calcEMA(dataRange):
    a = 2 / (len(dataRange) + 1)
    totalSum = dataRange[0]
    totalDenom = 1
    for i in range(1, len(dataRange)):
        totalSum += pow(1 - a, i) * dataRange[i]
        totalDenom += pow(1 - a, i)

    return totalSum / totalDenom

# returns true if current day is greater than the exponential moving average of n days, returns false if n > len of file data
def exponentialMovingAverage(stockData, N):
    index = 0
    currentRange = []
    length = len(stockData) - 1

    if(len(stockData) <= N):
        return False

    while(index < length):
        while(index < length and len(currentRange) < N):
            currentRange.append(stockData[index])
            index += 1
        if(index >= length):
            return False

        if(stockData[index + 1] > calcEMA(currentRange)):
           return True

        del(currentRange[0])

    return False

def CalcMax(dataRange):
    return max(dataRange)

# sees if current day is greater than max of previous n days, returns false if n > len of file data
def maximum(stockData, N):
    index = 0
    currentRange = []
    length = len(stockData) - 1

    if(len(stockData) <= N):
        return False

    while(index < length):
        while(index < length and len(currentRange) < N):
            currentRange.append(stockData[index])
            index += 1
        if(index >= length):
            return False
        if(stockData[index + 1] > max(currentRange)):
           return True

        del(currentRange[0])

    return False

# runs input data against 3 rules contained in genotype
def calcFitness(stockData, population):
    fitPop = []
    for genotypes in population:
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
                            newRules.append((maximum(dataset, rule[2]), rule[1], rule[2], rule[3]))
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
                    availableFunds = (dataset[-1]) * totalStock
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

        ruleTypes = []
        ruleValues = []
        ruleBools = []

        for rand in range(3):
            randNum = rnd.randint(0, 3)
            if(randNum == 0):
                ruleTypes.append('s')
            elif(randNum == 1):
                ruleTypes.append('e')
            else:
                ruleTypes.append('m')

        for rand in range(3):
            ruleValues.append(str(rnd.randint(0, 1000)).zfill(3))

        for rand in range(2):
            randNum = rnd.randint(0,2)
            if(randNum == 0):
                ruleBools.append('&')
            else:
                ruleBools.append('|')

        genotype = ruleTypes[0] + ruleValues[0] + ruleBools[0] + ruleTypes[1] + ruleValues[1] + ruleBools[1] + ruleTypes[2] + ruleValues[2]
        population.append((0.0, genotype))

    return population

def stockRunner():
    POPULATION_SIZE = 20
    stockData = sr.readAllFileStocks()

    population = genereatePopulation(POPULATION_SIZE)
    population = calcFitness(stockData, population)

    for x in population:
        print(x)
