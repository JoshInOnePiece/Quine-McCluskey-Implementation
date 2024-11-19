f = open("adder.pla", "r")

numberOfInput = 0
numberOfOutput = 0
nameOfInputs = [None]*2
nameofOutput = ""

readValue = f.readline()
print("Read Value: " + readValue[0:2] + "\n")
if readValue[0:1] == ".i":
    numberOfInput = int(readValue[3])
    nameOfInputs = [None]*numberOfInput
    print("Number of inputs: " + str(numberOfInput))

while readValue != ".e":
    print("Read Value: " + readValue + "\n")
    if readValue[0:4] == ".ilb":
        for x in range(0,numberOfInput):
            nameOfInputs[x] = readValue[2*x+5]
        print(nameOfInputs)
        readValue = f.readline()
        continue
    elif readValue[0:2] == ".i" and readValue[0:3] != ".ilb":
        numberOfInput = int(readValue[3])
        nameOfInputs = [None]*numberOfInput
        print("Number of inputs: " + str(numberOfInput))
    elif readValue[0:2] == ".o" and readValue[0:3] != ".ob":
        numberOfOutput = int(readValue[3])
        nameOfOutput = [None]*numberOfOutput
        print("Number of outputs: " + str(numberOfOutput))
    elif readValue[0:3] == ".ob":
        nameOfOutput = readValue[4]
        print("Name of output: " + str(nameOfOutput))
        break
    readValue = f.readline()

minterms = []

while readValue != ".e":
    readValue = f.readline()
    if readValue[len(readValue)-2] == "1":
        minterms.append(readValue.split(None, 1)[0])
        print(readValue.split(None, 1)[0])
f.close()