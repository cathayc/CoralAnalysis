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

    #[minX, maxX, minY, maxY, minZ, maxZ]
    boxDimensions=[]

    def __init__(self, fileName):
        self.fileName = fileName
        self.coralName = fileName.split("\\")[-2]
    def findBoundBox(self):
        [minX, maxX, minY, maxY, minZ, maxZ] = self.boxDimensions
        return [maxX-minX, maxY-minY, maxZ-minZ]
    def getVertexList(self):
        trueList = []
        for vertex in self.vertexList:
            trueList.append(vertex.lstrip('v ').split(' ')[:3])
        return trueList