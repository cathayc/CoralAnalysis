class Coral:
    coralName = ""
    numEdges = 0
    numVertices = 0
    numFaces = 0
    numHoles = 0
    boundLength = 0
    boundWidth = 0
    boundHeight = 0
    surfaceArea = 0
    volume = 0
    fileName = ""
    analysisTime = 0

    def __init__(self, fileName):
        self.fileName = fileName