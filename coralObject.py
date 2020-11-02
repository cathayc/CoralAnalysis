import numpy as np
import matplotlib.pyplot as plt
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
        plt.clf()
        plt.title(self.coralName + "'s my FD: " + str(round(self.myFD, 3)))
        X, Y = self.myXY
        plt.scatter(X, Y, c="yellow")
        m, b = np.polyfit(X, Y, 1)
        plt.plot(X, m*np.array(X) + b)
        saveFilePath = "D:\Members\Cathy\coralAnalysis\myFDOutputGraphs\\"
        plt.savefig(saveFilePath + self.coralName)
    
    
    def plotBothFD(self):
        plt.clf()
        saveFilePath = "D:\Members\Cathy\coralAnalysis\output\\"
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=0.5)

        #First plot online FD
        ax1.set_ylabel(r'$log(N(\epsilon))$')
        ax1.set_xlabel(r'$log(\frac{1}{\epsilon})$')
        X1, Y1 = self.onlineXY
        m1, b1 = np.polyfit(X1, Y1, 1)
        ax1.scatter(X1, Y1, c = "teal", label = "online FD")
        ax1.set_title(self.coralName + "'s online FD: " + str(round(self.onlineFD, 3)))
        ax1.plot(X1, m1*np.array(X1) + b1)

        #Then plot file FD
        ax2.set_ylabel(r'$log(V(r))$')
        ax2.set_xlabel(r'$log(r)$')
        X2, Y2 = self.fileXY
        m2, b2 = np.polyfit(X2, Y2, 1)
        ax2.scatter(X2, Y2, c = "red", label = "file FD")
        ax2.set_title(self.coralName + "'s file FD:  " + str(round(self.fileFD, 3)))
        ax2.plot(X2, m2*np.array(X2) + b2, color="orange")

        #Plot both on the same graph
        diff = X1[0]-X2[0]
        ax3.scatter(X1-diff, Y1, c = "teal", label = "online FD")
        ax3.scatter(X2, Y2, c = "red", label = "file FD")
        ax3.set_title("both")
        ax3.plot(X1-diff, m1*np.array(X1) + b1)
        ax3.plot(X2, m2*np.array(X2) + b2, color="orange")
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