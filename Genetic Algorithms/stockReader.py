import csv
import os

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
