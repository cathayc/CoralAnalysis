from analyzeObj import analyzeObject
from coralObject import *

coralFileList = "D:\Members\Cathy\coralFileList.txt"
coralDataOutputFile = "D:\Members\Cathy\dataOutput.txt"

# Given a coral object, determine what to return to the output file
def obtainCurrentCoralData(fileName, currentCoral):
    fileName = currentCoral.fileName
    sa=currentCoral.surfaceArea
    volume=currentCoral.volume
    analysisTime = currentCoral.analysisTime

    if sa == 0:
        return fileName + " not found \n"
    else:

        return fileName + " " + str(sa) + "  " + str(volume) + "    " + str(analysisTime) +"\n"

# Open, parse and read coral file list, and return the list of corals in the coral file
def openAndRead(coralFileList):
    with open(coralFileList,'r') as file:
        line = file.readline()
        while line:
            coralList.append(line.strip())
            line = file.readline()
    return coralList

# Analyze and write to file
def analyzeAndWrite(coralList, coralDataOutputFile):
    with open(coralDataOutputFile, 'a') as outputFile:
        outputFile.truncate(0)
        outputFile.write("File Name:        Surface Area (mm^2):       Volume (mm^3):         Analysis time (seconds)\n")
        for fileName in coralList:
            print(fileName)
            currentCoral = analyzeObject(fileName)
            outputFile.write(obtainCurrentCoralData(fileName, currentCoral))


# ----------------------------------------
#               Main Method
# ----------------------------------------
# read all coral files and store file name in coralList
coralList = []
coralList = openAndRead(coralFileList)
analyzeAndWrite(coralList, coralDataOutputFile)
print("Analysis finished!")
