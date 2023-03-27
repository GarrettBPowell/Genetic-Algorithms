import stockReader as sr
import numpy as np
import random 
import threading

RANDOM_SEED_VALUE = 12
POPULATION_SIZE = 5
MUTATION_RATE = .1
GENERATIONS = 10
globalBestRule = (0.0, 'e746|e121|m517', True)

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


def getRandRule(current):
    if current == 's':
        return random.choice(['m', 'e'])
    if current == 'm':
        return random.choice(['s','e'])

    return 'e'

def getRandNum(current):
    return str(random.choice([i for i in range(0,10) if i not in [current]]))

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
            for i in range(1 + x*5, 4 + x*5):
                randNum = rnd.rand()
                if( randNum < rate):
                    newRule += getRandNum(int(row[1][i]))
                else:
                    newRule += row[1][i]

            # change first/sec bool
            randNum = rnd.rand()
            if randNum < rate and row[1][4 + x*5] == '&':
               newRule += '|'
            elif randNum < rate:
                newRule += '&'
            else:
                newRule += row[1][4 + x*5]

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
        mutated.append((row[0], newRule, True))

    return mutated

# driver that returns the correct rule's value
def runRule(rule, range, data, numOfPurchasedStocks):
    calcVal = 0.0

    if(rule[1] != 0):
        if rule[0] == 's':
            calcVal = calcSMA(range)
        elif rule[0] == 'e':
            calcVal = calcEMA(range)
        else:
            calcVal = calcMax(range)

        if(numOfPurchasedStocks == 0 and data > calcVal):
            return True
        elif numOfPurchasedStocks > 0 and data < calcVal:
            return True

    return False
    
# runs input data against 3 rules contained in genotype
def calcFitness(stockData, population):
    fitPop = []
    for genotypes in population:
        if genotypes[2]:
            # break out the different rules
            ruleBlock = genotypes[1]
            rules = [(ruleBlock[0], int(ruleBlock[1:4]), ruleBlock[4]), (ruleBlock[5], int(ruleBlock[6:9]), ruleBlock[9]), (ruleBlock[10], int(ruleBlock[11:14]), 'end')]

            profit = 0
            availableFunds = 20000
            numOfPurchasedStocks = 0

            if not(rules[0][1] == 0 and rules[1][1] == 0 and rules[2][1] == 0):
                for dataset in stockData:

                    rule0Range = []
                    rule1Range = []
                    rule2Range = []
                    startPoint = 0
                    # skip portion of dataset if rules all depend on each other
                    if(rules[0][2] == '&' and rules[1][2] == '&'):
                         startPoint = max(rules[0][1], rules[1][1], rules[2][1])

                         rule0Range = dataset[(startPoint - rules[0][1]):(startPoint)]
                         rule1Range = dataset[(startPoint - rules[1][1]):(startPoint)]
                         rule2Range = dataset[(startPoint - rules[2][1]):(startPoint)]

                    for data in dataset[startPoint:]:
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
                            np.append(rule0Range,data)
                            ruleBoolean[0] = False
                        elif rules[0][1] != 0:               
                            ruleBoolean[0] = runRule(rules[0], rule0Range, data, numOfPurchasedStocks)
              
                            np.delete(rule0Range, 0)
                            np.append(rule0Range, data)

                        if( len(rule1Range) < rules[1][1]):
                           np.append(rule1Range, data)
                           ruleBoolean[1] = False
                        elif rules[1][1] != 0:
                            ruleBoolean[1] = runRule(rules[1], rule1Range, data, numOfPurchasedStocks)

                            np.delete(rule1Range, 0)
                            np.append(rule1Range, data)

                        if( len(rule2Range) < rules[2][1]):
                           np.append(rule2Range, data)
                           ruleBoolean[2] = False
                        elif rules[2][1] != 0:
                            ruleBoolean[2] = runRule(rules[2], rule2Range, data, numOfPurchasedStocks)

                            np.delete(rule2Range, 0)
                            np.append(rule2Range, data)


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
            fitPop.append((profit, genotypes[1], False))
        else:
            fitPop.append(genotypes)
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

        # readd high performers
        if( fitness >= popAverage * 2):
            for i in range(10):
                randNum = rnd.randint(100)
                if randNum > 10:
                    intermediatePop.append(row)

        # readd above average performers
        if( fitness >= popAverage):
            for i in range(5):
                randNum = rnd.randint(100)
                if randNum > 10:
                    intermediatePop.append(row)

        randNum = rnd.randint(100)
        if( randNum > 90 and row[0] != 0.0):
            intermediatePop.append(row)

    if len(intermediatePop) <= 2:
        intermediatePop.append(random.choices(population))
        intermediatePop.append(random.choices(population))
            

    # get new pop 
    returnPop = []
    # cross over or 25% chance to take parent
    for i in range(popSize // 2):
        pairs = random.choices(intermediatePop, k=2)
        randNum = rnd.randint(4)
        if(randNum == 0):
            returnPop.append((pairs[0][0], pairs[0][1], False))
            returnPop.append((pairs[1][0], pairs[1][1], False))
        else:
            item1 = pairs[0][1]
            item2 = pairs[1][1]

            if not( item1[1] == item2[1]):
                pivot = rnd.randint(1, N-1)

                returnPop.append((pairs[0][0], item1[0:pivot] + item2[pivot:], True))
                returnPop.append((pairs[1][0], item2[0:pivot] + item1[pivot:], True))
            else:
                returnPop.append(pairs[0])
                returnPop.append(pairs[1])

    return returnPop

# makes the initial population based off set pop size
def genereatePopulation(popSize):
    population = []
    population.append(globalBestRule)

    for i in range(popSize - len(population)):

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

        # (fitness, rules, has the rule changed thus the fitness has changed?)
        population.append((0.0, genotype, True))

        #population = [(0.0, "s010&e000&m000"), (0.0,"s000&e010&m000"), (0.0,"s000&e000&m010"), (0.0,"s010&e010&m000"), (0.0,"s010&e000&m020"), (0.0,"s025|e015&m000"), (0.0,"s030|e030|m030"), (0.0,"s010&s025|e000"), (0.0,"s900&e950|m950"), (0.0,"s008&e008|m050")]

    return population

def stockRunner():
    bestRule = globalBestRule
    stockData = sr.readAllFileStocks()

    population = genereatePopulation(POPULATION_SIZE)
    population = calcFitness(stockData, population)

    for i in range(GENERATIONS):
        population = generateIntermediatePopulation(population, POPULATION_SIZE, 14)
        population = mutate(MUTATION_RATE, population)
        population = calcFitness(stockData, population)
        population.sort(key=lambda a: a[0], reverse=True)

        # if population is averaging around the same genotype
        if population[0][1] == population[POPULATION_SIZE // 3][1]:
            popultation = mutate(0.5, population)
            population = calcFitness(stockData, population)
            population.sort(key=lambda a: a[0], reverse=True)
        elif population[0][1] == population[(POPULATION_SIZE // 2) - 1][1]:
            popultation = mutate(0.3, population)
            population = calcFitness(stockData, population)
            population.sort(key=lambda a: a[0], reverse=True)

        print("###################\nGeneration: {}".format(i+ 1))
        if(population[0][0] > bestRule[0]):
            bestRule = population[0]
            print("\n\n  *************************************")
            print("  New best rule in {} generation is {} \n\n".format(i + 1, bestRule))

            for item in population:
                print("  Fitness: {} Rule:{}".format(item[0], item[1]))

 
    print("The best overall rule is: {} with a fitness of {}".format(bestRule[1], round(bestRule[0], 2)))