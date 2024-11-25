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

# This checks if implicant represents specified minterm
def validImplicant(str1,str2):
    if len(str1) != len(str2):
        return False
    for b1, b2 in zip(str1, str2):
        #print(b1,b2)
        if b1 == '-' or b2 == '-':
            continue
        if b1 != b2:
            return False
    return True

class QM:
    def __init__(self, path):
        self.inputNames = []
        self.outputNames = []
        self.inputTerms = []
        self.onsetTerms = []
        self.outputTerms = []
        self.numInputs = 0
        self.file = path
        self.unUsedTerms = set()
        self.implicantTable = {}
        self.implicantToMintermTable = {}
        self.keepGoing = False
        self.chosenImplicants = []


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
            if outputTerm == '1':
                self.onsetTerms.append(inputTerm)
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
        usedTerms = set()
        self.keepGoing = False
        for x in range(0, len(list) - 1):#iterating over sublists, do not check last list
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y]
                nextList = list[x+1]
                for z in range(0, len(nextList)):
                    if diffByOne(currString, nextList[z]):
                        self.keepGoing = True
                        usedTerms.add(currString)
                        usedTerms.add(nextList[z])
                        pair = (int(currString, 2), int(nextList[z], 2))
                        combined = (pair,findDiff(currString, nextList[z]))
                        terms.append((combined))
                if currString in usedTerms:
                    continue
                else:
                    self.unUsedTerms.add(currString)
        print(self.unUsedTerms)
        #print(terms)
        return terms

    def tabulatePair(self, list):
        """takes list of (pair, term) pairs sorted into sublists based on number of 1s and tabulate them"""
        terms = []
        usedTerms = set()
        self.keepGoing = False
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
                        self.keepGoing = True
                        pair = currList[y][0] + nextList[z][0]
                        combined = (pair,findDiff(currString, nextList[z][1]))
                        usedTerms.add(currString)
                        usedTerms.add(nextList[z][1])
                        terms.append((combined))
                if currString in usedTerms:
                    continue
                else:
                    self.unUsedTerms.add(currString)
        print(self.unUsedTerms)
        return terms
    
    def createImplicantTable(self):
        implicantTable = {}
        implicantsForEachMinterm = []
        for minterm in self.onsetTerms:
            implicantsForEachMinterm.clear()
            implicantTable[minterm] = []
            for implicant in self.unUsedTerms:
                #valid = validImplicant(minterm,implicant)
                if(validImplicant(minterm,implicant)):
                    # print(minterm,implicant, end=" ")
                    # print(valid)
                    implicantsForEachMinterm.append(implicant)
            # print(implicantsForEachMinterm)
            implicantTable[minterm] += implicantsForEachMinterm
        return implicantTable
    
    def createImplicantToMintermTable(self):
        implicantTable = {}
        mintermForImplicant = []
        for implicant in self.unUsedTerms:
            mintermForImplicant.clear()
            implicantTable[implicant] = []
            for minterm in self.onsetTerms:
                #valid = validImplicant(minterm,implicant)
                if(validImplicant(implicant,minterm)):
                    # print(minterm,implicant, end=" ")
                    # print(valid)
                    mintermForImplicant.append(minterm)
            # print(mintermForImplicant)
            implicantTable[implicant] += mintermForImplicant
        return implicantTable
    
    def remakeTable(self):
        remadeTable = {}
        implicantSet = set()
        for value in self.implicantTable.values():
            implicantSet.update(value)
        implicantList = list(implicantSet)
        mintermList = []
        for implicant in implicantList:
            mintermList.clear()
            remadeTable[implicant] = []
            for minterm in self.implicantTable:
                if validImplicant(implicant, minterm):
                    mintermList.append(minterm)
            remadeTable[implicant] += mintermList
                    
        print("Implicant List", implicantList)
        return remadeTable
    
    def findingEssentialPrimeImplicants(self):
        chosenImplicants = []
        i = 1
        for minterms in self.onsetTerms:
            print(i)
            if minterms in chosenImplicants:
                continue
            print(minterms, len(self.implicantTable.get(minterms)))
            # Case if only one implicant represents a minterm
            if len(self.implicantTable.get(minterms)) == 1:
                chosenImplicant = self.implicantTable.get(minterms, "Not Found")[0]
                self.chosenImplicants.append(chosenImplicant) # Save implicant 
                #del self.implicantTable[minterms] # Since implicant that represents minterm is found, we don't need minterm
                mintermsRepresentedByImplicant = self.implicantToMintermTable.get(chosenImplicant) # Finds minterms represented by chosen implicant
                for sharedMinterms in mintermsRepresentedByImplicant:
                    if sharedMinterms in chosenImplicants:
                        continue
                    del self.implicantTable[sharedMinterms] # Since chosen implicate represents multiple minterms, we do not needs to find the implicant for those minterms. Thus, we delet from dictionary
                    chosenImplicants.append(sharedMinterms)
                del self.implicantToMintermTable[chosenImplicant] # Delete chosen implicant from table
                #print(self.implicantTable)
                #print(self.implicantToMintermTable)
                i = i+1
        return

    def doQM(self):
        terms = self.createTable(self.inputTerms)
        termPairs = self.tabulate(terms)
        print(self.onsetTerms)
        while True:
            terms = self.createTablePairs(termPairs)
            termPairs = self.tabulatePair(terms)
            if self.keepGoing == False:
                break
        self.implicantTable = self.createImplicantTable()
        print(self.implicantTable)
        self.implicantToMintermTable = self.createImplicantToMintermTable()
        print("Minterms for each implicant")
        print(self.implicantToMintermTable)
        self.findingEssentialPrimeImplicants()
        print("Chosen implicants")
        print(self.chosenImplicants)
        print(self.implicantTable)
        print("Remade Table")
        remadeTable = self.remakeTable()
        print(remadeTable)

        #pairs = [termPair[0] for termPair in termPairs]
        #terms = [termPair[1] for termPair in termPairs]
        # print("Term pairs")
        # #print(termPairs)
        # temp2 = self.createTablePairs(termPairs)
        # temp3 = self.tabulatePair(temp2)
        # #print(temp3)
        # temp4 = self.createTablePairs(temp3)
        # temp5 = self.tabulatePair(temp4)
        # temp6 = self.createTablePairs(temp5)
        # temp7 = self.tabulatePair(temp6)
        #print(temp5)
def main():

    qm = QM('onlineExample1.pla')
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
#implicantsGrouped = [[]*1 for i in range(numberOfInput+1)]
#while readValue != ".e":
#    readValue = f.readline()
#    if readValue[len(readValue)-2] == "1":
#        minterm = readValue.split(None, 1)[0]
#        minterms.append(minterm)
#        mintermBitLength = len(minterm)
#        print(minterm)
#        hammingWeight = popcount_py(minterm)
#        print("Number of ones:" + str(hammingWeight))
#        implicantsGrouped[hammingWeight].append(minterm)
#print(implicantsGrouped)
#f.close()
#