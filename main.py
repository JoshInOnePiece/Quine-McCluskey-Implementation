import re
from collections import defaultdict
import sys
from itertools import combinations
import copy
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
        ###print(b1,b2)
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
        self.dontCareTerms = []
        self.outputTerms = []
        self.numInputs = 0
        self.numOutputs = 0
        self.file = path
        self.unUsedTerms = set()
        self.implicantTable = {}
        self.implicantToMintermTable = {}
        self.keepGoing = False
        self.chosenImplicants = []
        self.termsDecimal = []
        self.covered = []


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
        self.numOutputs = len(outputLabels)
        terms = [line.strip().split() for line in lines if re.match(r'^[01-]+\s+[01-]+$', line)]


        for line in terms:
            inputTerm = line[0]
            outputTerm = line[1]
            if outputTerm == '1': # or outputTerm =='-':
                self.onsetTerms.append(inputTerm)
            if outputTerm == '-':
                self.dontCareTerms.append(inputTerm)
            self.inputTerms.append(inputTerm)
            self.outputTerms.append(outputTerm)
    
    def createTable(self, list):
        """Takes a list of strings (int this case the inputTerms) and returns a 2D list of n lists, where list n has all strings with n # of 1's"""
        groupedByOnes = []
        for numOnes in range(0, self.numInputs + 1):
            newList = [s for s in list if s.count("1") == numOnes]
            groupedByOnes.append(newList)
        ###print(groupedByOnes)
        return groupedByOnes

    def createTablePairs(self, list):
        groupedByOnes = []
        # Extract only the strings from the pairs to determine the maximum count
        max_ones = self.numInputs

        for numOnes in range(0, max_ones + 1):
            # Filter pairs based on the count of '1's in the string
            newList = [pair for pair in list if pair[1].count("1") == numOnes]
            groupedByOnes.append(newList)

        ###print(groupedByOnes)
        return groupedByOnes
    

    def printData(self):
        #print("Input Labels: ")
        #print(self.inputNames)
        #print("Output Labels: ")
        #print(self.outputNames)
        #print("Input Terms: ")
        #print(self.inputTerms)
        #print("Output Terms: ")
        #print(self.outputTerms)
        ##print("Decimal Terms")
        ##print(self.termsDecimal)
        return

    def tabulate(self, list):
        """Perform the tabulate step on 'list', which should be a list of lists, where sublist in list at position n has all items with n 1's"""
        terms = []
        usedTerms = set()
        self.keepGoing = False
        usedLast = False
        ##print(list)
        listLen = len(list)
        for x in range(0, listLen):#iterating over sublists, do not check last list
            ##print(x)
            if (x == (listLen - 1)):
                print(usedLast)
                if not usedLast and len(list) > 0 and len(list[-1]) > 0:
                    ##print(list[-1][0])
                    pair = (int(list[-1][-1],2), int(list[-1][-1],2))
                    combine = (pair,list[-1][-1])
                    self.unUsedTerms.add(list[-1][-1])
                    terms.append(combine)
                elif len(list) > 0 and len(list[-1]) > 0:
                    usedTerms.add(list[-1][-1])
                break
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y]
                
                nextList = list[x+1]
                for z in range(0, len(nextList)):
                    if diffByOne(currString, nextList[z]):
                        if (x == (listLen-2)):
                            #print("YESAY")
                            usedLast = True
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
        ##print(self.unUsedTerms)
        ###print(terms)
        #print(terms)
        return terms

    def tabulatePair(self, list):
        """takes list of (pair, term) pairs sorted into sublists based on number of 1s and tabulate them"""
        terms = []
        usedTerms = set()
        self.keepGoing = False
        usedLast = False
        listLen = len(list)
        for x in range(0, len(list)):#iterating over sublists, do not check last list
            if (x == (listLen - 1)):
                if not usedLast and len(list) > 0 and len(list[-1]) > 0:
                    ##print(list[-1][0])
                    item = list[-1][-1][1]
                    ##print("item")
                    ##print(item)
                    #print("yes")
                    pair = (int(item,2), int(item,2))
                    combine = (pair,item)
                    self.unUsedTerms.add(item)
                    terms.append(combine)
                elif len(list) > 0 and len(list[-1]) > 0:
                    #print("no")
                    item = list[-1][-1][1]
                    usedTerms.add(item)
                break
            for y in range(0, len(list[x])):#iterating over string in sublist
                # x[y] is now the current string being checked
                currList = list[x]
                currString = currList[y][1]
                nextList = list[x+1]
                
                for z in range(0, len(nextList)):
                    ###print("curr " + currString)
                    ###print(nextList[z][1])
                    if diffByOne(currString, nextList[z][1]):
                        ###print("diff")
                        #pair = (int(currString, 2), int(nextList[z], 2))
                        if (x == (listLen-2)):
                            #print("YESY")
                            usedLast = True
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
        ##print(self.unUsedTerms)
        return terms
    
    def createImplicantTable(self):
        implicantTable = {}
        implicantsForEachMinterm = []
        for minterm in self.onsetTerms:
            implicantsForEachMinterm.clear()
            implicantTable[minterm] = []
            #print(self.unUsedTerms)
            for implicant in self.unUsedTerms:
                #valid = validImplicant(minterm,implicant)
                #print("implicant")
                #print(implicant)
                if(validImplicant(minterm,implicant)):
                    # ##print(minterm,implicant, end=" ")
                    # ##print(valid)
                    implicantsForEachMinterm.append(implicant)
            # ##print(implicantsForEachMinterm)
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
                    # ##print(minterm,implicant, end=" ")
                    # ##print(valid)
                    mintermForImplicant.append(minterm)
            # ##print(mintermForImplicant)
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
                    
        ##print("Implicant List", implicantList)
        self.implicantToMintermTable = remadeTable
        return remadeTable
    
    def remakeImplicantTable(self):
        remadeTable = {}
        mintermSet = set()
        for value in self.implicantToMintermTable.values():
            mintermSet.update(value)
        mintermList = list(mintermSet)
        implicantList = []
        for minterm in mintermList:
            implicantList.clear()
            remadeTable[minterm] = []
            for implicant in self.implicantToMintermTable:
                if validImplicant(minterm, implicant):
                    implicantList.append(implicant)
            remadeTable[minterm] += implicantList
                    
        ##print("Minterm List", mintermList)
        self.implicantTable = remadeTable
        return remadeTable

    def findingEssentialPrimeImplicants(self):
        chosenImplicants = []
        i = 1
        for minterms in self.onsetTerms:
            ##print(i)
            if minterms in chosenImplicants:
                continue
            if minterms not in self.implicantTable.keys():
                continue
            ##print(minterms)
            ##print(minterms, len(self.implicantTable.get(minterms)))
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
                ###print(self.implicantTable)
                ###print(self.implicantToMintermTable)
                i = i+1
        return
    
    def findColumnDomination(self):
        didColumnDominate = False
        implicantList = []
        for key in self.implicantToMintermTable:
            implicantList.append(key)
        ##print("Minterm List ", implicantList)
        for key1 in implicantList:
            for key2 in implicantList:
                if key1 == None or key2 == None:
                    continue
                # ##print(key1, key2)
                # ##print(self.implicantToMintermTable.get(key1),self.implicantToMintermTable.get(key2))
                if self.implicantToMintermTable.get(key1) == None or self.implicantToMintermTable.get(key2) == None:
                    continue
                if self.implicantToMintermTable.get(key1) == self.implicantToMintermTable.get(key2):
                    continue
                if set(self.implicantToMintermTable.get(key1)).issubset(set(self.implicantToMintermTable.get(key2))):
                    # ##print("Key1 is subset of key2")
                    del self.implicantToMintermTable[key1]
                    didColumnDominate = True
                elif set(self.implicantToMintermTable.get(key2)).issubset(set(self.implicantToMintermTable.get(key1))):
                    # ##print("Key2 is subset of key1")
                    del self.implicantToMintermTable[key2]
                    didColumnDominate = True
        self.remakeImplicantTable()
        return didColumnDominate
    
    def findRowDomination(self):
        didRowDominate = False
        mintermList = []
        for key in self.implicantTable:
            mintermList.append(key)
        ##print("Minterm List ", mintermList)
        for key1 in mintermList:
            for key2 in mintermList:
                if key1 == None or key2 == None:
                    continue
                # ##print(key1, key2)
                # ##print(self.implicantToMintermTable.get(key1),self.implicantToMintermTable.get(key2))
                if self.implicantTable.get(key1) == None or self.implicantTable.get(key2) == None:
                    continue
                if self.implicantTable.get(key1) == self.implicantTable.get(key2):
                    continue
                if set(self.implicantTable.get(key1)).issubset(set(self.implicantTable.get(key2))):
                    # ##print("Key1 is subset of key2")
                    del self.implicantTable[key1]
                    didRowDominate = True
                elif set(self.implicantTable.get(key2)).issubset(set(self.implicantTable.get(key1))):
                    # ##print("Key2 is subset of key1")
                    del self.implicantTable[key2]
                    didRowDominate = True
        self.remakeImplicantTable()
        return didRowDominate
        
    def doQM(self):#, listIn):
        terms = self.createTable(self.onsetTerms + self.dontCareTerms)
        print(terms)
        termPairs = self.tabulate(terms)
        print(termPairs)
        while True:
            terms = self.createTablePairs(termPairs)
            termPairs = self.tabulatePair(terms)
            print("terms")
            print(terms)
            if self.keepGoing == False:
                break
        print(self.unUsedTerms)
        self.implicantTable = self.createImplicantTable()
        print("Implicant Table: ", self.implicantTable)
        self.implicantToMintermTable = self.createImplicantToMintermTable()

        while True: 
            continueQM = False
            #print("Minterms for each implicant")
            #print(self.implicantToMintermTable)
            self.findingEssentialPrimeImplicants()
            #print("Chosen implicants")
            #print(self.chosenImplicants)
            ##print(self.implicantTable)
            #print("Remade Table")
            remadeTable = self.remakeTable()
            #print(remadeTable)
            ##print("Starting Column Domination")
            hasColumnDomination = self.findColumnDomination()
            #print("Implicant Table: ",self.implicantTable)
            #print("Implicant to minterm table: ", self.implicantToMintermTable)
            ##print("Starting Row Domination")
            hasRowDomination = self.findRowDomination()
            ##print("Implicant Table: ",self.implicantTable)
            ##print("Implicant to minterm table: ", self.implicantToMintermTable)
            if hasColumnDomination == False and hasRowDomination == False:
                break
        print("Final Chosen Implicants: ")
        print(self.chosenImplicants)
        return self.chosenImplicants
        #pairs = [termPair[0] for termPair in termPairs]
        #terms = [termPair[1] for termPair in termPairs]
        # ##print("Term pairs")
        # ###print(termPairs)
        # temp2 = self.createTablePairs(termPairs)
        # temp3 = self.tabulatePair(temp2)
        # ###print(temp3)
        # temp4 = self.createTablePairs(temp3)
        # temp5 = self.tabulatePair(temp4)
        # temp6 = self.createTablePairs(temp5)
        # temp7 = self.tabulatePair(temp6)
        ###print(temp5)

    def writeFile(self, filename):
        f = open(filename, "w")
        content = f".i {self.numInputs}\n"
        f.write(content)
        content = f".o {self.numOutputs}\n"
        f.write(content)
        content = f".ilb"
        names = ""
        for inputName in self.inputNames:
            names = names + " " + inputName
        content += names + "\n"
        f.write(content)
        content = f".ob"
        names =""
        for outputName in self.outputNames:
            names = names + " " + outputName
        content += names + "\n"
        f.write(content)

        content = f".p " + str(len(self.chosenImplicants)) + "\n"
        f.write(content)
        for implicant in self.chosenImplicants:
            content = implicant + " 1\n"
            f.write(content)
        content = f".e"
        f.write(content)
        f.close()
        #print("Output file written to (", filename, ")")

    def getNumTerms(self):
        return len(self.chosenImplicants)

def findBestQMTerms(filename):
    qm = QM(filename)
    qm.parsePLA()
    terms = []
    onSet = qm.onsetTerms
    dcSet = qm.dontCareTerms
    combinationsDC = []
    for r in range(len(dcSet) + 1):  # r is the length of each combination
        combinationsDC.extend(combinations(dcSet, r))
    ##print(combinationsDC)
    numberOfTermsPerCombination = []
    terms = []
    for termsToAdd in list(combinationsDC):
        combined = onSet
        for term in list(termsToAdd):
            combined.append(term)
        #combined += termsToAdd
        #print("comibined ", combined)
        qmCopy = copy.copy(qm)
        results = qmCopy.doQM(combined)
        terms.append(combined)
        numberOfTermsPerCombination.append(len(results))
    idx = 0
    min = numberOfTermsPerCombination[0]
    for i in range(0, len(terms)):
        if numberOfTermsPerCombination[i] < min and numberOfTermsPerCombination[i] != 0:
            idx = i
            min = numberOfTermsPerCombination[i]
    ##print("terms")
    ##print(terms)
    return terms[idx]


def main():
    n = len(sys.argv)
    if n != 3:
        #print("Usage: main.py <input file path> <output file path>")
        sys.exit(1)
    input = sys.argv[1]
    output = sys.argv[2]
    
    #result = findBestQMTerms(input)

    qm = QM(input)
    qm.parsePLA()
    #qm.printData()
    qm.doQM()
    qm.writeFile(output)

if __name__ == "__main__":
    main()

