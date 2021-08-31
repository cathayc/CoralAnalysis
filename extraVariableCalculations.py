from FDOutputGraphRevision import convertToList, findPlateauPoint
import math

class coral:
    def __init__(self, fileName, sa, vol, myFD, fileFD, numVertices, boundLength, boundWidth, boundHeight, x, y):  
        self.fileName = fileName
        self.sa = float(sa)
        self.volume = float(vol)
        self.myFD = myFD
        self.fileFD = fileFD
        self.numVertices = numVertices
        self.boundLength = boundLength
        self.boundWidth = boundWidth
        self.boundHeight = boundHeight
        self.x = x
        self.y = y

input_file_path = 'D:\Members\Cathy\coralAnalysis\driveOutputDataCombined.txt'
output_file_path = 'D:\Members\Cathy\coralAnalysis\extraVariableCalculations.txt'

def main():
    coral_and_data = []
    corals = openAndExtract(input_file_path)
    for coral in corals:
        plateauPoint =  findPlateauPoint(coral.x, coral.y)[1]
        sphericity = calculateSphericity(coral.volume, coral.sa)
        minscale = determine_min_scale(coral.x, plateauPoint)
        #print("{} | Sphericity: {}".format(coral.fileName, sphericity))
        #data = "{} | plateauPoint: {} | sphericity: {} | minscale(mm): {}".format(coral.fileName, plateauPoint, sphericity, minscale)
        coral_and_data.append(str(minscale))
    writeToOutputFile(coral_and_data, output_file_path)

def determine_min_scale(myX, plateauPoint):
    x = myX[plateauPoint]
    minscale = math.e**(-x)*1000
    return minscale

# Sphericity is the ratio of the surface area of a sphere with the same volume as object and the surface area of the object
def calculateSphericity(volume, surfaceArea):
    # Calculate the surface area of a sphere with the same volume as object
    r = (3/4*volume/math.pi)**(1/3)
    sa_sphere = 4*math.pi*r**2
    sphericity = sa_sphere/surfaceArea
    return sphericity

def openAndExtract(input_file_path):
    listOfCorals = []
    #File-Name:	File number:	Surface Area (mm^2)	Volume (mm^3)	myFD	FileFD	numVertices	boundLength	boundWidth	boundHeight	myX	myY
    try:
        with open(input_file_path,'r') as file:
            text = file.read().splitlines()
            for i in range(len(text)-1):
                data = text[i+1].split(" | ")
                fileName = data[0]
                sa = data[1]
                vol = data[2]
                myFD = data[3]
                fileFD = data[5]
                numVertices = data[6]
                boundLength = data[7]
                boundWidth = data[8]
                boundHeight = data[9]
                x = convertToList(data[10])
                y = convertToList(data[11])
                listOfCorals.append(coral(fileName, sa, vol, myFD, fileFD, numVertices, boundLength, boundWidth, boundHeight, x, y))
    except IOError as e:
        return None
    return listOfCorals

def writeToOutputFile(coral_and_data, output_file_path):        
    with open(output_file_path, 'a') as outputFile:
        outputFile.truncate(0)
        for data in coral_and_data:
            print(data)
            outputFile.write(data + "\n")

if __name__ == "__main__":
    main()