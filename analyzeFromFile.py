from analyzeObj import analyzeObject
from coralObject import *
import os

output_filepath = "D:\Members\Cathy\output\dataOutput.txt"
coralList = []
coralfilepath = "D:\Members\Cathy\coralFiles\2510.obj"

# Main method
def main():
    coral_filepath = input("File path of the coral to be analyzed: ")
    analyzeFile(coral_filepath)

def analyzeFile(filepath):
    currentCoral = analyzeObject(filepath)
    print(obtainCurrentCoralData(currentCoral))
    writeAndUploadData(currentCoral)
    currentCoral.writeXYtoFile()

# Given a coral object, determine what to return to the output file
def obtainCurrentCoralData(currentCoral):
    if currentCoral==None:
        return "File not found, please try another file!\n"
    else:
        return currentCoral.obtainCoralText()

# Analyze and write to file
def writeAndUploadData(currentCoral):
    info_to_append = ""

    # Open local file
    with open(output_filepath, 'a') as outputFile:
        if os.path.getsize(output_filepath) == 0:
            info_to_append = "File Name: | Surface Area (mm^2) | Volume (mm^3) | myFD | FileFD | numVertices | boundLength | boundWidth | boundHeight | myX | myY\n"
        coralName = currentCoral.coralName
        sa = currentCoral.surfaceArea
        vol = currentCoral.volume
        myFD = currentCoral.myFD
        fileFD =  currentCoral.fileFD
        numV = currentCoral.numVertices
        boundLength, boundWidth, boundHeight = currentCoral.findBoundBox()
        myX, myY = currentCoral.myXY
        info_to_append += "{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n".format(coralName, sa, vol, myFD, fileFD, numV, boundLength, boundWidth, boundHeight, myX, myY)

        # Write to local file first
        outputFile.write(info_to_append)
        print("Successfully wrote to output file")

if __name__ == "__main__":
    main()