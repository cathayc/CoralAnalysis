import numpy as np
import matplotlib.pyplot as plt

from FDOutputGraphRevision import singleCoralRevision

class Coral:
    coralName = ""
    numEdges = 0
    vertexList = []
    normalList = []
    numVertices = 0
    numFaces = 0
    numHoles = 0
    surfaceArea = 0
    volume = 0
    filePath = ""
    analysisTime = 0
    onlineFD = 0
    onlineXY = []
    boxDimensions=[]
    jessicafilePath = ""
    fileFD = 0
    fileXY = []
    myFD =0
    myXY = []
    def __init__(self, filePath):
        self.filePath = filePath
        self.coralName = filePath.strip('.obj').split("\\")[-1]
        self.jessicafilePath = 'D:\Members\Cathy\JessicaCoralFiles\{}.txt'.format(self.coralName)
    
    def findBoundBox(self):
        [minX, minY, minZ, maxX, maxY, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]

    def plotMyFD(self):
        print("Save unrevised coral graph")
        plt.clf()
        saveFilePath = "D:\Members\Cathy\coralAnalysis\myFDOutputGraphs\\"
        plt.title(self.coralName + "'s my FD: " + str(round(self.myFD, 3)))
        X, Y = self.myXY

        plt.scatter(X, Y, c="green")
        m, b = np.polyfit(X, Y, 1)
        plt.plot(X, m*np.array(X) + b)
        plt.savefig(saveFilePath + self.coralName)

    def plotToPlateau(self):
        X, Y = self.myXY
        self.myFD = singleCoralRevision(self.coralName, X, Y)

    def plotFileFD(self):
        plt.clf()
        saveFilePath = "D:\Members\Cathy\coralAnalysis\\fileFDOutputGraphs\\"
        X, Y = self.fileXY
        if len(X) != 0:
            plt.title(self.coralName + "'s file FD: " + str(round(self.fileFD, 3)))
            plt.scatter(X, Y, c="green")
            m, b = np.polyfit(X, Y, 1)
            plt.plot(X, m*np.array(X) + b)
            plt.savefig(saveFilePath + self.coralName)
    

"""
    def getVertexList(self):
        if self.vertexList[0][0]=="v":
            trueList = []
            for vertex in self.vertexList:
                xCoord=float(vertex.lstrip('v ').split(' ')[0])
                yCoord=float(vertex.lstrip('v ').split(' ')[1])
                zCoord=float(vertex.lstrip('v ').split(' ')[2])
                trueList.append((xCoord, yCoord, zCoord))
            self.vertexList = trueList
        return self.vertexList
"""