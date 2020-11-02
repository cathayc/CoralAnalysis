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
        x = coral.x
        y = coral.y
        plateau_point = findPlateauPoint(x, y)
        print("\ncoral: {}".format(coral.name))
        fd = plotToPlateau(coral.name, x, y, plateau_point)
        coral_and_fd.append("{} | {}".format(coral.name, fd))
    
    writeToOutputFile(coral_and_fd, output_file_path)


def writeToOutputFile(coral_and_fd, output_file_path):        
    with open(output_file_path, 'a') as outputFile:
        outputFile.truncate(0)
        outputFile.write("Coral Name: | fd: \n")
        for data in coral_and_fd:
            print(data)
            outputFile.write(data + "\n")
        
def plotToPlateau(name, x, y, plateau_point):
    plt.clf()
    m, b = np.polyfit(x[:plateau_point], y[:plateau_point], 1)
    plt.title("Coral name: {} with FD: {}".format(name, m))
    plt.scatter(x, y, c="yellow")
    plt.plot(x, m*np.array(x) + b)
    saveFilePath = "D:\Members\Cathy\coralAnalysis\myFDOutputGraphsRevised\\"
    plt.savefig(saveFilePath + name)
    return m

def findPlateauPoint(x, y):
    slopeList = findSlopeList(x, y)
    print("slopeList: {}".format(slopeList))
    for i in range(len(slopeList)-1):
        slope = slopeList[i+1]
        if slope < 0.5:
            print("plateau point: {}".format(i))
            return i
    return i

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