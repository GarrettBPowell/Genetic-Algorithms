import csv
import os
import numpy as np

def readFileStocks(fileNameRead):
    name = ''
    date = ''
    stockPrices = []

    fileName = os.path.abspath('stockResources/' + fileNameRead + '.txt')

    with open(fileName, 'r') as file:
        lineNum = 0
        
        for line in file.readlines():
            if(lineNum == 0):
                name = line
            elif(lineNum == 1):
                date = line
            else:
                stockPrices.append(float(line))
            lineNum +=1 

    return (stockPrices)

def readAllFileStocks():
    allStocks = []

    directory = os.path.abspath('stockResources/')
    for filename in os.listdir(os.path.abspath(directory)):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, 'r') as file:
                lineNum = 0
                name = ''
                date = ''
                stockPrices = []

                for line in file.readlines():
                    if(lineNum == 0):
                        name = line
                    elif(lineNum == 1):
                        date = line
                    else:
                        stockPrices.append(float(line))
                    lineNum +=1 
                allStocks.append(np.array(stockPrices))
    return np.array(allStocks, dtype=object)

def readAllNewFileStocks():
    allStocks = []

    directory = os.path.abspath('newStockResources/newPrices/')
    for filename in os.listdir(os.path.abspath(directory)):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, 'r') as file:
                lineNum = 0
                name = ''
                date = ''
                stockPrices = []

                for line in file.readlines():
                    if(lineNum == 0):
                        name = line
                    elif(lineNum == 1):
                        date = line
                    else:
                        stockPrices.append(float(line))
                    lineNum +=1 
                allStocks.append(np.array(stockPrices))
    return np.array(allStocks, dtype=object)
