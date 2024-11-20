import re
from collections import defaultdict
def popcount_py(x):
    return x.count("1")

def diffByOne(str1, str2):
    if len(str1) != len(str2):
        return False
    differingBits = sum(b1 != b2 for b1, b2 in zip(str1, str2))

    return differingBits == 1

def findDiff(str1, str2):
    combined = ''.join(b1 if b1 == b2 else '-' for b1, b2 in zip(str1, str2))
    return combined

class QM:
    def __init__(self):
        self.inputNames = []
        self.outputNames = []
        self.inputTerms = []
        self.outputTerms = []
        self.numInputs = 0


    def parsePLA(self, path):
        """Parses the file at path and populates the QM with the names of the inputs, names of
        the outputs, the input terms, and the output terms. Also saves number of inputs."""
        with open(path, 'r') as f:
            lines = f.readlines()
        
        numInputs = int(next(line.split()[1] for line in lines if line.startswith('.i ')))
        numOutputs = int(next(line.split()[1] for line in lines if line.startswith('.o ')))

        inputLabels = next(line.split()[1:] for line in lines if line.startswith('.ilb'))
        outputLabels = next(line.split()[1:] for line in lines if line.startswith('.ob'))

        self.inputNames = inputLabels
        self.numInputs = len(inputLabels)
        self.outputNames = outputLabels

        terms = [line.strip().split() for line in lines if re.match(r'^[01-]+\s+[01-]+$', line)]

        for line in terms:
            inputTerm = line[0]
            outputTerm = line[1]
            self.inputTerms.append(inputTerm)
            self.outputTerms.append(outputTerm)
    
    def createTable(self):
        """Takes a list of strings (int this case the inputTerms) and returns a 2D list of n lists, where list n has all strings with n # of 1's"""
        groupedByOnes = []
        for numOnes in range(0, self.numInputs + 1):
            newList = [s for s in self.inputTerms if s.count("1") == numOnes]
            groupedByOnes.append(newList)
        print(groupedByOnes)
        return groupedByOnes

    def printData(self):
        print("Input Labels: ")
        print(self.inputNames)
        print("Output Labels: ")
        print(self.outputNames)
        print("Input Terms: ")
        print(self.inputTerms)
        print("Output Terms: ")
        print(self.outputTerms)

    def tabulate(self, list):
        """Perform the tabulate step on 'list', which should be a list of lists, where sublist in list at position n has all items with n 1's"""
        terms = []
        pairFirst = 0
        pairSecond = len(list[0])
        for x in range(0, len(list) - 1):#iterating over sublists, do not check last list
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y]
                nextList = list[x+1]
                
                for z in range(0, len(nextList)):
                    if diffByOne(currString, nextList[z]):
                        pair = (pairFirst, pairSecond)
                        combined = (pair,findDiff(currString, nextList[z]))
                        terms.append((combined))
                    pairSecond += 1
                pairFirst += 1
        print(terms)
        return terms



def main():

    qm = QM()
    qm.parsePLA('adder.pla')
    qm.printData()
    temp = qm.createTable()
    qm.tabulate(temp)

if __name__ == "__main__":
    main()

#f = open("adder.pla", "r")
#
#numberOfInput = 0
#numberOfOutput = 0
#nameOfInputs = []
#nameofOutput = ""
#
#readValue = f.readline()
#print("Read Value: " + readValue[0:2] + "\n")
#if readValue[0:1] == ".i":
#    numberOfInput = int(readValue[3])
#    nameOfInputs = [None]*numberOfInput
#    print("Number of inputs: " + str(numberOfInput))
#
#while readValue != ".e":
#    print("Read Value: " + readValue + "\n")
#    if readValue[0:4] == ".ilb":
#        for x in range(0,numberOfInput):
#            nameOfInputs[x] = readValue[2*x+5]
#        print(nameOfInputs)
#        readValue = f.readline()
#        continue
#    elif readValue[0:2] == ".i" and readValue[0:3] != ".ilb":
#        numberOfInput = int(readValue[3])
#        nameOfInputs = [None]*numberOfInput
#        print("Number of inputs: " + str(numberOfInput))
#    elif readValue[0:2] == ".o" and readValue[0:3] != ".ob":
#        numberOfOutput = int(readValue[3])
#        nameOfOutput = [None]*numberOfOutput
#        print("Number of outputs: " + str(numberOfOutput))
#    elif readValue[0:3] == ".ob":
#        nameOfOutput = readValue[4]
#        print("Name of output: " + str(nameOfOutput))
#        break
#    readValue = f.readline()
#
#minterms = []
#mintermBitLength = 0
#mintermsGrouped = [[]*1 for i in range(numberOfInput+1)]
#while readValue != ".e":
#    readValue = f.readline()
#    if readValue[len(readValue)-2] == "1":
#        minterm = readValue.split(None, 1)[0]
#        minterms.append(minterm)
#        mintermBitLength = len(minterm)
#        print(minterm)
#        hammingWeight = popcount_py(minterm)
#        print("Number of ones:" + str(hammingWeight))
#        mintermsGrouped[hammingWeight].append(minterm)
#print(mintermsGrouped)
#f.close()
#


