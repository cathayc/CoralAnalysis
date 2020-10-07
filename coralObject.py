import numpy as np
import matplotlib.pyplot as plt
class Coral:
    coralName = ""
    numEdges = 0
    vertexList = []
    numVertices = 0
    numFaces = 0
    numHoles = 0
    surfaceArea = 0
    volume = 0
    fileName = ""
    analysisTime = 0
    onlineFD = 0
    onlineXY = []
    boxDimensions=[]
    jessicaFileName = ""
    fileFD = 0
    fileXY = []
    def __init__(self, fileName):
        self.fileName = fileName
        self.coralName = fileName.split("\\")[-2]
        self.jessicaFileName = fileName.strip(".obj") + ".txt"
    
    def findBoundBox(self):
        [minX, minY, minZ, maxX, maxY, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]
    
    def plotOnlineXY(self, online=True, file=False):
        X = Y = []
        fd = 0
        figTitle = ""
        if online:
            X, Y = self.onlineXY
            fd = self.onlineFD
            figTitle =  self.coralName + "online_FD"
        else:
            X, Y = self.fileXY
            fd = self.fileFD
            figTitle =  self.coralName + "file_FD"
        fig, ax = plt.subplots(figsize = (8,6))
        ax.scatter(X, Y, c = "teal", label = "Measured ratios")
        ax.set_ylabel("$\log N(\epsilon)$")
        ax.set_xlabel("$\log 1/ \epsilon$")
        m, b = np.polyfit(X, Y, 1)
        plt.title(figTitle + str(fd))
        #plt.plot(np.array(X), m*np.array(X) + b)
        plt.savefig(figTitle)
    
    def plotBothFD(self):
        fig, ax = plt.subplots(figsize = (8,6))
        ax.set_ylabel("$\log N(\epsilon)$")
        ax.set_xlabel("$\log 1/ \epsilon$")

        #First plot online FD
        X, Y = self.onlineXY
        m1, b = np.polyfit(X, Y, 1)
        ax.scatter(X, Y, c = "teal", label = "online FD")
        #plt.plot(X, m1*np.array(X) + b)

        #Then plot file FD
        X, Y = self.fileXY
        m2, b = np.polyfit(X, Y, 1)
        ax.scatter(X, Y, c = "yellow", label = "file FD")
        #plt.plot(X, m2*X + b)

        #Save the file
        plt.title(self.coralName + "'s both online FD: " + str(m1) + " & file FD:  " + str(m2))
        plt.savefig(self.coralName+"both")

"""
    def findFromFDFile(self):
        X, Y = [], []
        file = self.jessicaFileName
        for line in open(file, 'r'):
            values = [float(s) for s in line.split()]
            X.append(values[2])
            Y.append(values[3])
        m, b = np.polyfit(X, Y, 1)
        fd = str(round(3-m, 3))
        print("Jessica's fractal dimension of " + self.coralName + " : " + fd)
        plt.plot(X, Y, 'o')
        #plt.plot(X, m*X[0] + b)
        plt.show()
        return fd
        #print(b)

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