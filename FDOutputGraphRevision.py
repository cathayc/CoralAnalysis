import numpy as np
import matplotlib.pyplot as plt

input_file_path = 'D:\Members\Cathy\coralAnalysis\driveOutputDataMYFD2.txt'
output_file_path = 'D:\Members\Cathy\coralAnalysis\coralAndRevisedFD.txt'

class coral_x_y:  
    def __init__(self, name, x, y):  
        self.name = name  
        self.x = x
        self.y = y

def main():
    corals = openAndExtract(input_file_path)
    coral_and_fd = []
    for coral in corals:
        print("\ncoral: {}".format(coral.name))
        x = coral.x
        y = coral.y
        start_point, plateau_point = findPlateauPoint(x, y)
        fd = plotToPlateau(coral.name, x, y, start_point, plateau_point)
        print("my revised fd: {}".format(fd))
        print("-------------------------------------------------------\n\n\n")
        coral_and_fd.append("{} | {}".format(coral.name, fd))
    
    writeToOutputFile(coral_and_fd, output_file_path)

def singleCoralRevision(name, x, y):
    start_point, plateau_point = findPlateauPoint(x, y)
    print("\ncoral: {}".format(name))
    fd = plotToPlateau(name, x, y, start_point, plateau_point)
    print("my revised fd: {}".format(fd))
    return fd

def writeToOutputFile(coral_and_fd, output_file_path):        
    with open(output_file_path, 'a') as outputFile:
        outputFile.truncate(0)
        outputFile.write("Coral Name: | fd: \n")
        for data in coral_and_fd:
            print(data)
            outputFile.write(data + "\n")
        
def plotToPlateau(name, x, y, start_point, plateau_point):
    plt.clf()
    print("startPoint: {} endPoint: {}".format(start_point, plateau_point))
    m, b = np.polyfit(x[start_point:plateau_point], y[start_point:plateau_point], 1)

    plt.title("Coral name: {} with FD: {}".format(name, m))
    plt.scatter(x[start_point:plateau_point], y[start_point:plateau_point], c="red")
    plt.scatter(x[plateau_point:], y[plateau_point:], c="blue")
    plt.scatter(x[:start_point], y[:start_point], c="blue")
    plt.plot(x, m*np.array(x) + b)
    saveFilePath = "D:\Members\Cathy\coralAnalysis\myFDOutputGraphsRevised\\"
    plt.savefig(saveFilePath + name)
    #plt.show()
    return m

def findPlateauPoint(x, y):
    slopeList = findSlopeList(x, y)
    avgSlope = (sum(slopeList[3:15])/len(slopeList[3:15]))
    print("slopeList: {}\nAverage slope: {}".format(slopeList, avgSlope))
    startPoint = -1
    plateauPoint = -1

    for i in range(len(slopeList)):
        slope = slopeList[i]
        print(slope)
        #first, find start point
        if startPoint==-1: 
            # Start counting if the slope is within 25% of the average slope
            if abs(slope-avgSlope)/avgSlope < 0.25:
                startPoint = i
                print("Start point: {}".format(startPoint))
        else:
            if slope < avgSlope*0.6:
                # Make sure it won't throw index out of range
                if (i+1<len(slopeList)):
                    # Make sure that it's actually plateauing
                    if slopeList[i+1]<avgSlope*0.8:
                        print("New plateau point. Slope: {} Slope*0.75: {}".format(slope, avgSlope*0.75))
                        break
    plateauPoint = i+1
    print("plateau point: {}".format(plateauPoint))
    return startPoint, plateauPoint

def findSlopeList(x, y):
    slopeList = []
    for i in range(len(x)-1):
        slope = findSlope((x[i+1], y[i+1]), (x[i], y[i]))
        slopeList.append(slope)
    return slopeList

def openAndExtract(input_file_path):
    coralAndData = []
    try:
        with open(input_file_path,'r') as file:
            text = file.read().splitlines()
            for i in range(len(text)-1):
                data = text[i+1].split(" | ")
                x = convertToList(data[2])
                y = convertToList(data[3])
                coralAndData.append(coral_x_y(data[0], x, y))
    except IOError as e:
        return None
    return coralAndData
    
def convertToList(list):
    list = list.strip("[").strip("]")
    list = list.split(", ")
    list = [float(item) for item in list]
    return list

def findSlope(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    slope = (y2-y1)/(x2-x1)
    return slope

if __name__ == "__main__":
    main()