"""
    This file finds the plateau point of fractal dimension and plots the fractal dimension to plateau point
"""
import numpy as np
import matplotlib.pyplot as plt
import math

input_file_path = 'D:\Members\Cathy\coralAnalysis\driveOutputDataMYFD.txt'
output_file_path = 'D:\Members\Cathy\coralAnalysis\coralAndRevisedFD.txt'

class coral_x_y:  
    def __init__(self, name, x, y):  
        self.name = name  
        self.x = x
        self.y = y


def singleCoralRevision(name, x, y, general_file_path):
    start_point, plateau_point = findPlateauPoint(x, y)
    print("\ncoral: {}".format(name))
    fd = plotPlateauFD(name, x, y, start_point, plateau_point, general_file_path)
    print("my revised fd: {}".format(fd))
    return fd

        
def plotPlateauFD(name, x, y, start_point, plateau_point, general_file_path):
    plt.clf()
    print("startPoint: {} endPoint: {}".format(start_point, plateau_point))
    m, b = np.polyfit(x[start_point:plateau_point], y[start_point:plateau_point], 1)

    plt.title("Coral name: {} with FD: {}".format(name, m))
    plt.scatter(x[start_point:plateau_point], y[start_point:plateau_point], c="red")
    plt.scatter(x[plateau_point:], y[plateau_point:], c="blue")
    plt.scatter(x[:start_point], y[:start_point], c="blue")
    plt.plot(x, m*np.array(x) + b)
    plt.savefig(general_file_path + "plateau")
    #plt.show()
    return m

def findPlateauPoint(x, y):
    slopeList = findSlopeList(x, y)
    #make sure we only care about the middle ones where slope>0.5 to calculate average slope
    start = -math.inf
    end = math.inf
    for i in range(len(slopeList)-1):
        if start>-100 and end<100:
            print("found start: {} end: {}".format(start, end))
            break
        if slopeList[i]>0.75 and start<-100:
            start = i
        if slopeList[len(slopeList)-i-1]>0.75 and end>100:
            print(len(slopeList)-i)
            end = len(slopeList)-i
    avgSlope = (sum(slopeList[start:end])/len(slopeList[start:end]))

    print("Average slope: {}".format(avgSlope))
    startPoint = -1
    plateauPoint = -1

    for i in range(len(slopeList)):
        slope = slopeList[i]

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
    if startPoint ==-1:
        startPoint=0
    plateauPoint = i+1
    print("plateau point: {}".format(plateauPoint))
    return startPoint, plateauPoint

def findSlopeList(x, y):
    slopeList = []
    for i in range(len(x)-1):
        slope = findSlope((x[i+1], y[i+1]), (x[i], y[i]))
        slopeList.append(slope)
    return slopeList


def findSlope(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    slope = (y2-y1)/(x2-x1)
    return slope

if __name__ == "__main__":
    main()