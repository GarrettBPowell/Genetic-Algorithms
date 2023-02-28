import csv
import os

# reads data in from file and returns a tuple that is
# Number of Items, Max Weight, List of data points
# data points are a touple of (label, weight, value)

def readFileKnap(fileNameRead):
    NumItems = -1 
    MaxWeight = -1
    pairedValues = []

    fileName = os.path.abspath('resources/' + fileNameRead + '.csv')

    with open(fileName) as openFile:
        csvReader = csv.reader(openFile, delimiter=',')

        lineNum = 0
        for row in csvReader:
            if(lineNum == 0):
                NumItems, MaxWeight = row #save values

                MaxWeight = int(MaxWeight.replace(' ', '')) #remove that stupid space and convert to int
                NumItems = int(NumItems) #convert to int

                lineNum += 1
            elif(lineNum != 0):
                pairedValues.append([row[0], int(row[1]), int(row[2])])

    return (NumItems, MaxWeight, pairedValues)
