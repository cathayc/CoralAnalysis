from FractalDimension import findOnlineFD, findFromFDFile

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

    #[minX, minY, minZ, maxX, maxY, maxZ]
    boxDimensions=[]

    def __init__(self, fileName):
        self.fileName = fileName
        self.coralName = fileName.split("\\")[-2]
    
    def findBoundBox(self):
        [minX, minY, minZ, maxX, maxY, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]
    
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
    
    def getOnlineFD(self):
        fd = findOnlineFD(self.getVertexList(), self.findBoundBox(), self.boxDimensions)
        return fd