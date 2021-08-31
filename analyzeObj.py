# Analyze Scanned Model from Obj File
# Michael Clougher


'''
A ".obj" file is one way to represent a 3d object - it has all the relevant information needed for 3d computing programs to 
generate a 3d model including xyz corrdinates of every vertex, the vertex normals, and which three vertices form a face.
This program takes an OBJ file and returns relevant geometric features about the model such as the surface area, the volume,
and whether there are any holes in the object. 

Code written by Michael Clougher: 
	TriArea, geetVertexCoord, dist, findtetraVolume, cross, dot, findBoundBox

Code written by Cathy Chang to integrate everything with FD analysis:
	getListCoord, analyzeFD, analyzeObject

The most important meethod to be used is analyzeObj, which analyzes the coral object and returns myCoral.
Example of how to usee the analyzeObj:
	coral2505 = analyzeObject("D:\Members\Cathy\\2505\\2505.obj")


'''


import itertools
import time
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from coralObject import Coral
from FractalDimension import findFromFDFile, findBucketFD

faceList=[]
edgeList=[]
vertexList=[]
surfaceArea=0
volume=0
minX=math.inf
maxX=-math.inf
minY=math.inf
maxY=-math.inf
minZ=math.inf
maxZ=-math.inf

#*********************************************************************
#                               Methods
#*********************************************************************

# Find volume of a triangle given three vertex label numbers 
def triArea(u,v,w):

	x1, y1, z1 = getVertexCoord(u)
	x2, y2, z2 = getVertexCoord(v)
	x3, y3, z3 = getVertexCoord(w)

	a=dist(x1,y1,z1,x2,y2,z2)
	b=dist(x2,y2,z2,x3,y3,z3)
	c=dist(x3,y3,z3,x1,y1,z1)
	
	#Use Heron's Formula
	s=(a+b+c)/2
	area=math.sqrt(s*(s-a)*(s-b)*(s-c))
	return area

# Returns the X, Y, and Z coordinates of a vertex given its label number
def getVertexCoord(vert):
	#xCoord=float(vertexList[int(vert)-1].lstrip('v ').split(' ')[0])
	#yCoord=float(vertexList[int(vert)-1].lstrip('v ').split(' ')[1])
	#zCoord=float(vertexList[int(vert)-1].lstrip('v ').split(' ')[2])
	coord = vertexList[int(vert)-1]
	return coord
	#return(xCoord,yCoord,zCoord)
	
# Calculate Euclidean distance	
def dist(a,b,c,d,e,f): 
	distance=math.sqrt((a-d)**2+(b-e)**2+(c-f)**2)
	return distance
	
# Find volume of a tetrahedron given three vertex label numbers, (fourth point is the origin)
def findtetraVolume(u,v,w):
	
	x1, y1, z1 = getVertexCoord(u)
	x2, y2, z2 = getVertexCoord(v)
	x3, y3, z3 = getVertexCoord(w)

	# Create vertices given their coordinates
	u1=[x1,y1,z1]
	v1=[x2,y2,z2]
	w1=[x3,y3,z3]

	# While we are already looking through each coordinate find the min/max values for X/Y/Z
	findBoundBox(u1)
	findBoundBox(v1)
	findBoundBox(w1)
	
	crossProduct=cross(v1,w1)
	dotProduct=dot(u1,crossProduct)
	tetraVolume=dotProduct/6

	return tetraVolume
	
# Compute cross product given vertices 'a' and 'b'	
def cross(a, b):
    product = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return product
	
# Compute dot product given vertices 'a' and 'b'	
def dot(a, b):
    product = a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    return product
	
# Keep track of min/max values fro X/Y/Z	
def findBoundBox(vert):

	global minX
	global maxX
	global minY
	global maxY
	global minZ
	global maxZ
	
	if(vert[0]<minX):
		minX=vert[0]
	if(vert[0]>maxX):
		maxX=vert[0]
		
	if(vert[1]<minY):
		minY=vert[1]
	if(vert[1]>maxY):
		maxY=vert[1]
		
	if(vert[2]<minZ):
		minZ=vert[2]
	if(vert[2]>maxZ):
		maxZ=vert[2]

# Converts either vertex or vertex normal into normal coordinates
def getListCoord(vertex, v):
	xCoord=float(vertex.lstrip(v).split(' ')[0])
	yCoord=float(vertex.lstrip(v).split(' ')[1])
	zCoord=float(vertex.lstrip(v).split(' ')[2])
	return (xCoord, yCoord, zCoord)

"""
	This is just for testing.
"""
def analyzeFD(filePath):
	global faceList, edgeList, vertexList
	global minX, maxX, minY, maxY, minZ, maxZ

	faceList.clear()
	edgeList.clear()
	vertexList.clear()
	minX=math.inf
	maxX=-math.inf
	minY=math.inf
	maxY=-math.inf
	minZ=math.inf
	maxZ=-math.inf

	# Get file name and handle incorrect/missing file names
	try:
		with open(filePath,'r') as file:
			text=file.read().splitlines()
			myCoral = Coral(filePath)
			print("Coral file " + myCoral.coralName + " found!")
	except IOError as e:
		print(filePath + " not found, please try another file:")
		return None
		
	# Start timer to analyze performance
	start_time = time.time()	

	print("Building list of all vertices.")
	# Build lists of all vertices and faces		
	for i in range(0, len(text)): 
		if len(text[i])>1:
			if text[i][0]=='v' and ' ' == text[i][1]:
				vertex = getListCoord(text[i], "v ")
				vertexList.append(vertex)
				findBoundBox(vertex)
	myCoral.vertexList = vertexList
	myCoral.boxDimensions = [minX, minY, minZ, maxX, maxY, maxZ]

	# Calculate fractal dimension
	myFD, myX, myY = findBucketFD(vertexList, myCoral.findBoundBox())
	myCoral.myFD = myFD
	myCoral.myXY = myX, myY
	
	myCoral.plotMyFD()
	myCoral.plotToPlateau()

	print(myCoral.myFD)

	return myCoral

def analyzeObject (filePath):

	global faceList, edgeList, vertexList
	global minX, maxX, minY, maxY, minZ, maxZ

	faceList.clear()
	edgeList.clear()
	vertexList.clear()
	surfaceArea=0
	volume=0
	minX=math.inf
	maxX=-math.inf
	minY=math.inf
	maxY=-math.inf
	minZ=math.inf
	maxZ=-math.inf

	# Get file name and handle incorrect/missing file names
	try:
		with open(filePath,'r') as file:
			text=file.read().splitlines()
			myCoral = Coral(filePath)
			print("Coral file " + myCoral.coralName + " found!")
	except IOError as e:
		print(filePath + " not found, please try another file:")
		return None
		
	# Start timer to analyze performance
	start_time = time.time()	

	print("Building list of all vertices and faces.")
	# Build lists of all vertices and faces		
	for i in range(0, len(text)): 
		if len(text[i])>1:
			if text[i][0]=='v' and ' ' == text[i][1]:
				vertexList.append(getListCoord(text[i], "v "))
			elif text[i][0]=='f':
				faceList.append(text[i])
	myCoral.vertexList = vertexList

	print("Calculating area and volume.")			
	for i in range(0, len(faceList)):
		# Break each face into the label numbers of each vertex
		vertex1=faceList[i].lstrip('f ').split(' ')[0].split('/')[0]
		vertex2=faceList[i].lstrip('f ').split(' ')[1].split('/')[0]
		vertex3=faceList[i].lstrip('f ').split(' ')[2].split('/')[0]
		
		# Surface area calculated by summing area of each triangular face
		surfaceArea+=triArea(vertex1,vertex2,vertex3)
		
		
		# Volume calculated by the sum of signed volumes of tetrahedrons. Each tetrahedron is formed by the three vertices of a face on the object; the fourth point is the origin
		volume+=findtetraVolume(vertex1,vertex2,vertex3)

		#We define each edge as a list of two vertices and sort so that duplicates can easily be deleted later
		edge1=sorted([vertex1, vertex2])
		edge2=sorted([vertex2, vertex3])
		edge3=sorted([vertex3, vertex1])
		
		# Add each edge to an edgeList
		edgeList.append(edge1)
		edgeList.append(edge3)
		edgeList.append(edge2)
			
	#Remove duplicates of edges
	edgeList.sort()
	edgeList=list(edgeList for edgeList,_ in itertools.groupby(edgeList))

	#Euler's Formula
	holes=int(-(len(vertexList)-len(edgeList)+len(faceList))/2+1)

	# Bounding Box distances
	length=abs(maxX-minX)
	width=abs(maxY-minY)
	height=abs(maxZ-minZ)
	boxDimensions = [minX, minY, minZ, maxX, maxY, maxZ]

	# Set coral object attributes
	if holes==1:
		myCoral.numHoles = 1
	elif holes==0:
		myCoral.numHoles = 0
	else:
		myCoral.numHoles = holes
	myCoral.numEdges = len(edgeList)
	myCoral.numVertices = len(vertexList)
	myCoral.numFaces = len(faceList)
	myCoral.boxDimensions = boxDimensions
	myCoral.surfaceArea = surfaceArea
	myCoral.volume = volume
	myCoral.analysisTime = time.time() - start_time

#	Some print statements to help with visualizing if writing to document doesn't work
	print("\n\nThere are " + str(len(vertexList)) + " vertices.")
	print("There are " + str(len(edgeList)) + " edges.")
	print("There are " + str(len(faceList)) + " faces.")
	if holes==1:
		print("There is one hole in the object.")
	elif holes==0:
		print("There are no holes in the object.")
	else:
		print("There are " + str(holes) + " holes in the object.")
	print ("\nThe bounding box dimensions are {:,.2f}".format(length) + "mm x " + "{:,.2f}".format(width) + "mm x " + "{:,.2f}".format(height) + "mm.")
	print ("The surface area is {:,.3f}".format(surfaceArea) + " square mm.")
	print ("The volume is {:,.3f}".format(volume) + " cubic mm.")

	print ("\n\n--- Elapsed time: {:,.2f}".format(time.time() - start_time) + " seconds ---")

	print("Calculating fractal dimension.")

	# Calculate fractal dimension using bucket fractal dimension
	myFD, myX, myY = findBucketFD(vertexList, myCoral.findBoundBox())
	myCoral.myFD = myFD
	myCoral.myXY = myX, myY
	myCoral.plotMyFD()
	myCoral.plotToPlateau()
	#myCoral.writeXYtoFile()


	# Using Jessica's fractal dimension
	fileFD, fileX, fileY = findFromFDFile(myCoral.jessicafilePath)
	myCoral.fileFD = fileFD
	myCoral.fileXY = fileX, fileY
	#myCoral.plotFileFD()
	
	return myCoral
	
#*********************************************************************
#								testingMain
#*********************************************************************

if __name__ == "__main__":
	main()
