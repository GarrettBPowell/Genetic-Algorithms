import stockReader as sr
import numpy as np
import random 

RANDOM_SEED_VALUE = 10
POPULATION_SIZE = 20
MUTATION_RATE = .1
GENERATIONS = 20

rnd = np.random.RandomState(RANDOM_SEED_VALUE) 

def calcSMA(dataRange):
    return(sum(dataRange) / len(dataRange))
        

def calcEMA(dataRange):
    a = 2 / (len(dataRange) + 1)
    totalSum = dataRange[0]
    totalDenom = 1
    for i in range(1, len(dataRange)):
        totalSum += pow(1 - a, i) * dataRange[i]
        totalDenom += pow(1 - a, i)

    return totalSum / totalDenom

def calcMax(dataRange):
    return max(dataRange)

# sees if current day is greater than max of previous n days, returns false if n > len of file data
def maximum(stockData, N):
    index = 0
    currentRange = []
    trueIndexes = set({})
    length = len(stockData) - 1

    if(len(stockData) <= N):
        return trueIndexes

    while(index < length):
        while(index < length and len(currentRange) < N):
            currentRange.append(stockData[index])
            index += 1
        if(index >= length):
            return trueIndexes
        if(stockData[index + 1] > max(currentRange)):
           trueIndexes.add(index + 1)

        del(currentRange[0])

    return trueIndexes

# driver that returns the correct rule's value
def runRule(rule, range):
    if rule[0] == 's':
        return calcSMA(range)
    elif rule[0] == 'e':
        return calcEMA(range)
    else:
        return calcMax(range)

    return -1

def getRandRule(current):
    if current == 's':
        return random.choice(['m', 'e'])
    if current == 'm':
        return random.choice(['s','e'])

    return e

def getRandNum(current):
    return random.choice([i for i in range(0,9) if i not in [current]])

def mutate(rate, population):
    mutated = []

    for row in population:
        newRule = ""

        for x in range(2):
            # change first/ sec rule
            randNum = rnd.rand()
            if( randNum < rate):
                newRule += getRandRule(row[1][x*5])
            else:
                newRule += row[1][x * 5]

            # change first/ sec rule num
            for i in range (1 + x*5, 1 + x*5):
                randNum = rnd.rand()
                if( randNum < rate):
                    newRule += getRandNum(int(row[1][i]))

            # change first/sec bool
            randNum = rnd.rand()
            if randNum < rate and row[1][1 + x*5] == '&':
               newRule += '|'
            elif randNum < rate:
                newRule += '&'
            else:
                newRule += row[1][1 + x*5]

        # change third rule
        randNum = rnd.rand()
        if( randNum < rate):
            newRule += getRandRule(row[1][10])
        else:
            newRule += row[1][10]

        # change third rule num
        for i in range (11,14):
            randNum = rnd.rand()
            if( randNum < rate):
                newRule += getRandNum(int(row[1][i]))
            else:
                newRule += row[1][i]






    return population

# runs input data against 3 rules contained in genotype
def calcFitness(stockData, population):
    fitPop = []
    for genotypes in population:
        # somehow break out the different rules
        ruleBlock = genotypes[1]
        rules = [(ruleBlock[0], int(ruleBlock[1:4]), ruleBlock[4]), (ruleBlock[5], int(ruleBlock[6:9]), ruleBlock[9]), (ruleBlock[10], int(ruleBlock[11:14]), 'end')]

        profit = 0
        availableFunds = 20000
        response = set({})
        numOfPurchasedStocks = 0

        if not(rules[0][1] == 0 and rules[1][1] == 0 and rules[2][1] == 0):
            for dataset in stockData:

                rule0Range = []
                rule1Range = []
                rule2Range = []

                for data in dataset:
                    ruleBoolean = [False, False, False]

                    # adjust profit and available funds to be appropriate starting ammounts
                    if(availableFunds > 20000):
                        profit += availableFunds - 20000
                        availableFunds = 20000
                    elif(availableFunds < 20000 and numOfPurchasedStocks == 0):
                        if(profit - (20000 - availableFunds) > 0):
                            profit -= 20000 - availableFunds
                            availableFunds = 20000
                        else:
                            availableFunds += profit
                            profit = 0

                # add current data to previous data and adjust accordingly
                    if( len(rule0Range) < rules[0][1]):
                        rule0Range.append(data)
                        ruleBoolean[0] = False
                    elif(rules[0][1] != 0) :                 
                        ruleReturn = runRule(rules[0], rule0Range)
                        if(numOfPurchasedStocks == 0 and data > ruleReturn):
                            ruleBoolean[0] = True
                        elif numOfPurchasedStocks > 0 and data < ruleReturn:
                            ruleBoolean[0] = True
               
                        del(rule0Range[0])
                        rule0Range.append(data)

                    if( len(rule1Range) < rules[1][1]):
                       rule1Range.append(data)
                       ruleBoolean[1] = False
                    elif rules[1][1] != 0:
                        ruleReturn = runRule(rules[1], rule1Range)
                        if(numOfPurchasedStocks == 0 and data > ruleReturn):
                            ruleBoolean[1] = True
                        elif numOfPurchasedStocks > 0 and data < ruleReturn:
                            ruleBoolean[1] = True

                        del(rule1Range[0])
                        rule1Range.append(data)

                    if( len(rule2Range) < rules[2][1]):
                       rule2Range.append(data)
                       ruleBoolean[2] = False
                    elif rules[2][1] != 0:
                        ruleReturn = runRule(rules[2], rule2Range)
                        if(numOfPurchasedStocks == 0 and data > ruleReturn):
                            ruleBoolean[2] = True
                        elif numOfPurchasedStocks > 0 and data < ruleReturn:
                            ruleBoolean[2] = True

                        del(rule2Range[0])
                        rule2Range.append(data)


                    # determine if the rule is true
                    choice = False

                    # check that the range is not 0 meaning that that portion of the rule should be excluded
                    # if rules are applied it checks the bools determined from the above code against each portion of the rule from left to right
                    # if 2 of the 3 rules are excluded it takes the bool of the remaining rule
                    # if the middle rule is excluded it takes the bool of the first and last rule and uses the 2 operator in the sequence ie. s100|m000&s500 would do s100&s500
                    if rules[0][1] != 0 and rules[1][1] != 0:
                        if(rules[0][2] == '&'):
                            choice = ruleBoolean[0] and ruleBoolean[1]
                        else:
                            choice = ruleBoolean[0] or ruleBoolean[1]
                    elif rules[0][1] != 0:
                        choice = ruleBoolean[0]
                    elif rules[1][1] != 0:
                        choice = ruleBoolean[1]

                    if rules[2][1] != 0 and rules[1][1] != 0:
                        if rules[1][2] == '&':
                            choice = choice and ruleBoolean[2]
                        else:
                            choice = choice or ruleBoolean[2]
                    elif rules[2][1] != 0 and rules[0][1] != 0:
                        if rules[1][2] == '&':
                            choice = choice and ruleBoolean[2]
                        else:
                            choice = choice or ruleBoolean[2]
                    elif rules[2][1] != 0:
                        choice = ruleBoolean[2]

                    if(choice):
                        if(numOfPurchasedStocks == 0):
                            numOfPurchasedStocks = availableFunds / data
                            availableFunds = 0
                        else:
                            availableFunds = numOfPurchasedStocks * data
                            numOfPurchasedStocks = 0

        # save fitness
        fitPop.append((profit, genotypes[1]))
    return fitPop



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

            newItem1 = item1[0:pivot] + item2[pivot:]
            newItem2 = item2[0:pivot] + item1[pivot:]
            #print("New Item1: ", newItem1, "New Item 2: ", newItem2)

            returnPop.append((pairs[0][0], newItem1))
            returnPop.append((pairs[1][0], newItem2))

    return returnPop
    

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

        #population = [(0.0, "s010&e000&m000"), (0.0,"s000&e010&m000"), (0.0,"s000&e000&m010"), (0.0,"s010&e010&m000"), (0.0,"s010&e000&m020"), (0.0,"s025|e015&m000"), (0.0,"s030|e030|m030"), (0.0,"s010&s025|e000"), (0.0,"s900&e950|m950"), (0.0,"s008&e008|m050")]

    return population

def stockRunner():
    stockData = sr.readAllFileStocks()

    bestRule = (0.0,"s050&m050&e050")

    population = genereatePopulation(POPULATION_SIZE)
    population = calcFitness(stockData, population)

    for i in range(GENERATIONS):
        population = generateIntermediatePopulation(population, POPULATION_SIZE, 14)
        population = mutate(MUTATION_RATE, population)
        population = calcFitness(stockData, population)
        population.sort(key=lambda a: a[0], reverse=True)

        if(population[0][0] > bestRule[0]):
            bestRule = population[0]
            print("*************************************")
            print("New best rule in {} generation is {} \n\n".format(i, bestRule))

        print("\n\n\n", population)

    for x in population:
        print("{}, {}".format(x[1], round(x[0], 2)))
