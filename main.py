import re
from collections import defaultdict
def popcount_py(x):
    return x.count("1")

def diffByOne(str1, str2):
    if len(str1) != len(str2):
        return False
    differingBits = 0
    for b1, b2 in zip(str1, str2):
        if b1 == '-' and b2 != '-':
            return False
        if b1 != '-' and b2 == '-':
            return False
        if b1 != b2:
            differingBits += 1

    return differingBits == 1

def findDiff(str1, str2):
    combined = ''.join(b1 if b1 == b2 else '-' for b1, b2 in zip(str1, str2))
    return combined



class QM:
    def __init__(self, path):
        self.inputNames = []
        self.outputNames = []
        self.inputTerms = []
        self.outputTerms = []
        self.numInputs = 0
        self.file = path


    def parsePLA(self):
        """Parses the file at path and populates the QM with the names of the inputs, names of
        the outputs, the input terms, and the output terms. Also saves number of inputs."""
        with open(self.file, 'r') as f:
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
    
    def createTable(self, list):
        """Takes a list of strings (int this case the inputTerms) and returns a 2D list of n lists, where list n has all strings with n # of 1's"""
        groupedByOnes = []
        for numOnes in range(0, self.numInputs + 1):
            newList = [s for s in list if s.count("1") == numOnes]
            groupedByOnes.append(newList)
        #print(groupedByOnes)
        return groupedByOnes

    def createTablePairs(self, list):
        groupedByOnes = []
        # Extract only the strings from the pairs to determine the maximum count
        max_ones = self.numInputs

        for numOnes in range(0, max_ones + 1):
            # Filter pairs based on the count of '1's in the string
            newList = [pair for pair in list if pair[1].count("1") == numOnes]
            groupedByOnes.append(newList)

        #print(groupedByOnes)
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
        for x in range(0, len(list) - 1):#iterating over sublists, do not check last list
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y]
                nextList = list[x+1]
                
                for z in range(0, len(nextList)):
                    if diffByOne(currString, nextList[z]):
                        pair = (int(currString, 2), int(nextList[z], 2))
                        combined = (pair,findDiff(currString, nextList[z]))
                        terms.append((combined))

        #print(terms)
        return terms

    def tabulatePair(self, list):
        """takes list of (pair, term) pairs sorted into sublists based on number of 1s and tabulate them"""
        terms = []
        for x in range(0, len(list) - 1):#iterating over sublists, do not check last list
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y][1]
                nextList = list[x+1]
                
                for z in range(0, len(nextList)):
                    #print("curr " + currString)
                    #print(nextList[z][1])
                    if diffByOne(currString, nextList[z][1]):
                        #print("diff")
                        #pair = (int(currString, 2), int(nextList[z], 2))
                        pair = currList[y][0] + nextList[z][0]
                        combined = (pair,findDiff(currString, nextList[z][1]))
                        terms.append((combined))
        return terms
    
    def doQM(self):
        temp = self.createTable(self.inputTerms)
        termPairs = self.tabulate(temp)
        #pairs = [termPair[0] for termPair in termPairs]
        #terms = [termPair[1] for termPair in termPairs]
        print("Term pairs")
        print(termPairs)
        temp2 = self.createTablePairs(termPairs)
        temp3 = self.tabulatePair(temp2)
        print(temp3)
        temp4 = self.createTablePairs(temp3)
        temp5 = self.tabulatePair(temp4)
        print(temp5)


def main():

    qm = QM('adder.pla')
    qm.parsePLA()
    qm.doQM()

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


