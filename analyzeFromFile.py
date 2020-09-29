from analyzeObj import analyzeObject
from coralObject import *

coralFileList = "D:\Members\Cathy\coralAnalysis\coralFileList.txt"
coralDataOutputFile = "D:\Members\Cathy\coralAnalysis\dataOutput.txt"

# Given a coral object, determine what to return to the output file
def obtainCurrentCoralData(fileName, currentCoral):
    if currentCoral==None:
        return fileName + " not found, please try another file!\n"
    else:
        coralName = currentCoral.coralName
        sa=currentCoral.surfaceArea
        volume=currentCoral.volume
        analysisTime = currentCoral.analysisTime
        #fd = currentCoral.getOnlineFD()
        [boundingLength, boundingWidth, boundingHeight]=currentCoral.findBoundBox()
        return str(coralName) + " | " + str(sa) + " | " + str(volume) + " | " + str(analysisTime) + " | " + str(boundingLength) + " | " + str(boundingWidth) + " | " + str(boundingHeight) + "\n"

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
        outputFile.write("File Name: | Surface Area (mm^2): | Volume (mm^3): | Analysis time (seconds): | Bounding Length (mm): | Bounding Width (mm): | Bounding Height (mm):\n")
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
