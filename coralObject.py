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
    
    
    def plotBothFD(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=2)

        #First plot online FD
        ax1.set_ylabel("log(N(e))")
        ax1.set_xlabel("log(1/e)")
        X1, Y1 = self.onlineXY
        m1, b1 = np.polyfit(X1, Y1, 1)
        ax1.scatter(X1-6, Y1, c = "teal", label = "online FD")
        ax1.set_title(self.coralName + "'s online FD: " + str(round(self.onlineFD, 3)))
        ax1.plot(X1-6, m1*np.array(X1) + b1)

        #Then plot file FD
        ax2.set_ylabel("log(Influence_Volume(mm^2))")
        ax2.set_xlabel("log(Dilation_Radius(m))")
        X2, Y2 = self.fileXY
        m2, b2 = np.polyfit(X2, Y2, 1)
        ax2.scatter(X2, Y2, c = "yellow", label = "file FD")
        ax2.set_title(self.coralName + "'s file FD:  " + str(self.fileFD))
        ax2.plot(X2, m2*np.array(X2) + b2)

        diff = X1[0]-X2[0]
        ax3.scatter(X1-diff, Y1, c = "teal", label = "online FD")
        ax3.scatter(X2, Y2, c = "yellow", label = "file FD")
        ax3.set_title("both")
        ax3.plot(X1-diff, m1*np.array(X1) + b1)
        ax3.plot(X2, m2*np.array(X2) + b2)
        plt.savefig(self.coralName+"both")
        

"""
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