"""
    This file defines the coral object. As analysis continues, it will store all the attributes
    Important notes:
        jessicafilePath refers to the filepath of the file that's obtained when one runs Jeessica Reichart's 
            Fractal Dimension Toolbox. Please feel free to change the filepath on line 39.
"""

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
    generalFilePath = ""
    
    def __init__(self, filePath):
        self.filePath = filePath
        self.generalFilePath = filePath.strip('.obj')
        self.coralName = filePath.strip('.obj').split("\\")[-1]
        self.coralName = filePath.strip('.obj').split("/")[-1]
        self.jessicafilePath = '{}.txt'.format(self.generalFilePath)
    
    def findBoundBox(self):
        [minX, minY, minZ, maxX, maxY, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]

    """
        Plots the fractal dimension slope into a file called "_name of coral_myFD.png"
    """
    def plotMyFD(self):
        print("Save unrevised coral graph")
        plt.clf()
        plt.title(self.coralName + "'s my FD: " + str(round(self.myFD, 3)))
        X, Y = self.myXY

        plt.scatter(X, Y, c="green")
        m, b = np.polyfit(X, Y, 1)
        plt.plot(X, m*np.array(X) + b)
        plt.savefig(self.generalFilePath + "myFD")

    """
        Plots the fractal dimension slope, revised to the plateau point, into a file called "_name of coral_myFD.png"
    """
    def plotToPlateau(self):
        X, Y = self.myXY
        self.myFD = singleCoralRevision(self.coralName, X, Y, self.generalFilePath)

    """
        Plots the fractal dimension slope obtained by Jessica's file.
    """
    def plotFileFD(self):
        plt.clf()
        X, Y = self.fileXY
        if len(X) != 0:
            plt.title(self.coralName + "'s file FD: " + str(round(self.fileFD, 3)))
            plt.scatter(X, Y, c="green")
            m, b = np.polyfit(X, Y, 1)
            plt.plot(X, m*np.array(X) + b)
            plt.savefig(self.generalFilePath + "file FD")

    def obtainCoralText(self):
        coralName = self.coralName
        sa=self.surfaceArea
        volume=self.volume
        numVertices = self.numVertices
        numEdges = self.numEdges
        numFaces = self.numFaces
        fileFD = self.fileFD
        analysisTime = self.analysisTime
        [boundingLength, boundingWidth, boundingHeight]=self.findBoundBox()
        return str(coralName) + " | " + str(sa) + " | " + str(volume)   + " | " + str(numVertices)   + str(numEdges)   +  " | " + str(numFaces)   + " | "  + " | " + str(fileFD) + " | " + str(analysisTime) + "\n"

    def writeXYtoFile(self):
        file_name = "D:\Members\Cathy\output" + self.coralName
        f  = open(file_name, "w+")
        X, Y = self.myXY
        for i in range(len(X)):
            print(X)
            f.write(str(X[i]) + " " + str(Y[i]) + "\n")