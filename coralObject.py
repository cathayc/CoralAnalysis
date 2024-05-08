"""
    This file defines the coral object. As analysis continues, it will store all the attributes
    Important notes:
        reichartFilePath refers to the filepath of the file that's obtained when one runs Jeessica Reichart's 
            Fractal Dimension Toolbox. Please feel free to change the filepath on line 39.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import time

from analysisHelpers import buildVertexFaceList, findAreaVolume, removeDuplicateEdges, findNumHoles, findMinMaxCoord, calculateSphericity, determineMinScale
from FractalDimension import plot_3D_dataset, findBucketFD, findFromReichartFile
from FDOutputGraphRevision import singleCoralRevision, findPlateauPoint

current_directory = os.getcwd()

class Coral:
    coralName = ""
    numEdges = 0
    vertexList = []
    normalList = []
    faceList = []
    edgeList = []
    vertexList = []
    numVertices = 0
    numFaces = 0
    numHoles = 0
    surfaceArea = 0
    sphericity = 0
    volume = 0
    filePath = ""
    analysisTime = 0
    minScale = []
    onlineFD = 0
    onlineXY = []
    boxDimensions=[]
    reichartFilePath = ""
    reichartFD = 0
    reichartXY = []
    bucketFD =0
    bucketXY = []
    outputGraphFilePath = ""

    minX=math.inf
    maxX=-math.inf
    minY=math.inf
    maxY=-math.inf
    minZ=math.inf
    maxZ=-math.inf

    surfaceArea=0
    volume=0
    
    def __init__(self, filePath):
        self.filePath = filePath
        self.coralName = filePath.strip('.obj').split("/")[-1]

        # Define all the file paths
        self.outputGraphFilePath = filePath.strip('.obj')
        self.unrevisedOutputGraphFilePath = os.path.join(current_directory, "output", "unrevised", self.coralName)
        self.plateauOutputGraphFilePath = os.path.join(current_directory, "output", "plateau", self.coralName)
        self.toolboxOutputGraphFilePath = os.path.join(current_directory, "output", "toolbox", self.coralName)
        self.reichartFilePath = '{}.txt'.format(self.outputGraphFilePath)
        self.runGeneralAnalysis(filePath)
    
    """
        Finds the bounding box of the coral
    """
    def findBoundBox(self):
        [minX, minY, minZ, maxX, maxY, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]

    """
        Plots the fractal dimension slope into a file called "_name of coral_bucketFD.png"
    """
    def plotUnrevisedFD(self):
        print("Save unrevised coral graph")
        plt.clf()
        plt.title(self.coralName + "'s my FD: " + str(round(self.bucketFD, 3)))
        X, Y = self.bucketXY

        plt.scatter(X, Y, c="green")
        m, b = np.polyfit(X, Y, 1)
        plt.plot(X, m*np.array(X) + b)
        plt.savefig(self.unrevisedOutputGraphFilePath + "bucketFD")

    """
        Plots the fractal dimension slope, revised to the plateau point, into a file called "_name of coral_bucketFD.png"
    """
    def plotPlateauFD(self):
        X, Y = self.bucketXY
        self.bucketFD = singleCoralRevision(self.coralName, X, Y, self.plateauOutputGraphFilePath)

    """
        Plots the fractal dimension slope obtained by Reichart's group's toolbox file. This doesn't work unless you have the reichartFilePath populated.
    """
    def plotReichartFD(self):
        plt.clf()
        X, Y = self.reichartXY
        if len(X) != 0:
            plt.title(self.coralName + "'s file FD: " + str(round(self.reichartFD, 3)))
            plt.scatter(X, Y, c="green")
            m, b = np.polyfit(X, Y, 1)
            plt.plot(X, m*np.array(X) + b)
            plt.savefig(self.toolboxOutputGraphFilePath + "reichartFD")
        
    """
        Returns everything that defines the coral (height, width, length, bounding box, etc.)
    """
    def obtainCoralText(self):
        coralName = self.coralName
        sa=self.surfaceArea
        volume=self.volume
        numVertices = self.numVertices
        numEdges = self.numEdges
        numFaces = self.numFaces
        reichartFD = self.reichartFD
        analysisTime = self.analysisTime
        [boundingLength, boundingWidth, boundingHeight]=self.findBoundBox()
        return str(coralName) + " | " + str(sa) + " | " + str(volume)   + " | " + str(numVertices)   + str(numEdges)   +  " | " + str(numFaces)   + " | "  + " | " + str(reichartFD) + " | " + str(analysisTime) + "\n"

    def runGeneralAnalysis(self, filePath):
        try:
            with open(filePath,'r') as file:
                text=file.read().splitlines()
                print("Coral file " + self.coralName + " found!")
        except IOError as e:
            print(filePath + " not found, please try another file:")
            return None
        
        # Start timer to analyze performance
        start_time = time.time()

        # Build lists of all vertices and faces
        print("Building list of all vertices and faces.")
        buildVertexFaceList(text, self.vertexList, self.faceList)

        # Calculate area and volume
        print("Calculating area and volume")
        self.surfaceArea, self.volume = findAreaVolume(self.faceList, self.edgeList, self.vertexList)

        # Remove duplicates of edges
        print("Removing duplicate edges")
        removeDuplicateEdges(self.edgeList)

        # Find num holes
        self.holes = findNumHoles(self.vertexList, self.edgeList, self.faceList)

        # Get box dimensions
        self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = findMinMaxCoord(self.vertexList)

        # Bounding Box distances
        length=abs(self.maxX-self.minX)
        width=abs(self.maxY-self.minY)
        height=abs(self.maxZ-self.minZ)
        boxDimensions = [self.minX, self.minY, self.minZ, self.maxX, self.maxY, self.maxZ]
        self.sphericity = calculateSphericity(self.volume, self.surfaceArea)

        # Set coral object attributes
        self.numEdges = len(self.edgeList)
        self.numVertices = len(self.vertexList)
        self.numFaces = len(self.faceList)
        self.boxDimensions = boxDimensions

        # Pop up the 3D file
        # print("Printing the 3D file")
        # plot_3D_dataset(self.vertexList)

        print("Calculating fractal dimension.")

        # Calculate fractal dimension using bucket fractal dimension
        self.bucketFD, self.bucketX, self.bucketY = findBucketFD(self.vertexList, self.findBoundBox())
        self.bucketXY = self.bucketX, self.bucketY

        self.minScale = determineMinScale(self.bucketXY[0], findPlateauPoint(self.bucketXY[0], self.bucketXY[1])[1])

        # Plotting the FD
        self.plotUnrevisedFD()
        self.plotPlateauFD()

        #	Some print statements to help with visualizing if writing to document doesn't work
        self.analysisTime = time.time() - start_time
        print("\n\nThere are " + str(len(self.vertexList)) + " vertices.")
        print("There are " + str(len(self.edgeList)) + " edges.")
        print("There are " + str(len(self.faceList)) + " faces.")
        print("There are " + str(self.holes) + " holes in the object.")
        print ("\nThe bounding box dimensions are {:,.2f}".format(length) + "mm x " + "{:,.2f}".format(width) + "mm x " + "{:,.2f}".format(height) + "mm.")
        print ("The surface area is {:,.3f}".format(self.surfaceArea) + " square mm.")
        print ("The volume is {:,.3f}".format(self.volume) + " cubic mm.")
        print("Sphericity: {}".format(self.sphericity))

        print ("\n\n--- Elapsed time: {:,.2f}".format(time.time() - start_time) + " seconds ---")

        # Using Reichart's fractal dimension
        reichartFD, reichartX, reichartY = findFromReichartFile(self.reichartFilePath)
        self.reichartFD = reichartFD
        self.reichartXY = reichartX, reichartY
        self.plotReichartFD()
        print("Reichart FD: {}".format(reichartFD))