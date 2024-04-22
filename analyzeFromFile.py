from analyzeObj import analyzeObject
from coralObject import *
import os, sys

# Get the current working directory
current_directory = os.getcwd()

# Construct the output and coral input paths using the current directory
output_name = "output.txt"
coral_directory_name = ""

output_filepath = os.path.join(current_directory, "/output/", output_name)
coral_directory_path = os.path.join(current_directory, "/input/", coral_directory_name)


# Main method
def main():
    global coral_filepath
    coral_filepath = input("File path of the coral to be analyzed: ")
    analyzeFile(coral_filepath, output_filepath)

def analyzeFile(filepath, output_path):
    output_filepath = output_path
    if not checkIfIsFile(coral_filepath, output_filepath):
        sys.exit()
    currentCoral = analyzeObject(filepath)
    print(obtainCurrentCoralData(currentCoral))
    writeAndUploadData(currentCoral)
    #currentCoral.writeXYtoFile()

# Given a coral object, determine what to return to the output file
def obtainCurrentCoralData(currentCoral):
    if currentCoral==None:
        return "File not found, please try another file!\n"
    else:
        return currentCoral.obtainCoralText()

def checkIfIsFile(coral_filepath, output_filepath):
    if not os.path.isfile(output_filepath):
        print(output_filepath + " is not a valid filepath. Please enter the correct path.")
        return False
    if not os.path.isfile(coral_filepath):
        print(coral_filepath + " is not a valid filepath. Please enter the correct path.")
        return False
    return True

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
