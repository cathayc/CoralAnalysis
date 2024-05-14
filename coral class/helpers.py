'''
A ".obj" file is one way to represent a 3d object - it has all the relevant information needed for 3d computing programs to 
generate a 3d model including xyz corrdinates of every vertex, the vertex normals, and which three vertices form a face.
This program takes an OBJ file and returns relevant geometric features about the model such as the surface area, the volume,
and whether there are any holes in the object. 
'''

import itertools
import time
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


#*********************************************************************
#                               Methods
#*********************************************************************

# Find volume of a triangle given three vertex label numbers 
def triArea(u,v,w, vertexList):
	x1, y1, z1 = getVertexCoord(u, vertexList)
	x2, y2, z2 = getVertexCoord(v, vertexList)
	x3, y3, z3 = getVertexCoord(w, vertexList)

	a=dist(x1,y1,z1,x2,y2,z2)
	b=dist(x2,y2,z2,x3,y3,z3)
	c=dist(x3,y3,z3,x1,y1,z1)
	
	#Use Heron's Formula
	s=(a+b+c)/2
	area=math.sqrt(s*(s-a)*(s-b)*(s-c))
	return area

# Returns the X, Y, and Z coordinates of a vertex given its label number
def getVertexCoord(vert, vertexList):
	coord = vertexList[int(vert)-1]
	return coord
	
# Calculate Euclidean distance	
def dist(a,b,c,d,e,f): 
	distance=math.sqrt((a-d)**2+(b-e)**2+(c-f)**2)
	return distance
	
# Find volume of a tetrahedron given three vertex label numbers, (fourth point is the origin)
def findtetraVolume(u,v,w, vertexList):
	x1, y1, z1 = getVertexCoord(u, vertexList)
	x2, y2, z2 = getVertexCoord(v, vertexList)
	x3, y3, z3 = getVertexCoord(w, vertexList)

	# Create vertices given their coordinates
	u1=[x1,y1,z1]
	v1=[x2,y2,z2]
	w1=[x3,y3,z3]
	
	crossProduct=cross(v1,w1)
	dotProduct=dot(u1,crossProduct)
	tetraVolume=dotProduct/6

	return tetraVolume

def findMinMaxCoord(vertexList):
	minX=math.inf
	maxX=-math.inf
	minY=math.inf
	maxY=-math.inf
	minZ=math.inf
	maxZ=-math.inf
	for vert in vertexList:
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
	return minX, maxX, minY, maxY, minZ, maxZ
	
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

# Converts either vertex or vertex normal into normal coordinates
def getListCoord(vertex, v):
	# In the case of faceList
	# Break each face into the label numbers of each vertex
	if v == 'f ':
		xCoord=float(vertex.lstrip('f ').split(' ')[0].split('/')[0])
		yCoord=float(vertex.lstrip('f ').split(' ')[1].split('/')[0])
		zCoord=float(vertex.lstrip('f ').split(' ')[2].split('/')[0])
	# Otherwise it's usually vertexList
	else:
		xCoord=float(vertex.lstrip(v).split(' ')[0])
		yCoord=float(vertex.lstrip(v).split(' ')[1])
		zCoord=float(vertex.lstrip(v).split(' ')[2])
	return (xCoord, yCoord, zCoord)

# Removes the duplicate edges on the edgeList
def removeDuplicateEdges(edgeList):
	edgeList.sort()
	edgeList=list(edgeList for edgeList,_ in itertools.groupby(edgeList))
	return edgeList

# Builds the vertextList and faceList from the obj file
def buildVertexFaceList(text, vertexList, faceList):
	for i in range(0, len(text)):
		if len(text[i])>1:
			if text[i][0]=='v' and ' ' == text[i][1]:
				vertexList.append(getListCoord(text[i], "v "))
			elif text[i][0]=='f':
				faceList.append(getListCoord(text[i], "f "))
	return vertexList, faceList

# Find the area and volume using faceList and edgeList
def findAreaVolume(faceList, edgeList, vertexList):
	surfaceArea = 0
	volume = 0
	for i in range(0, len(faceList)):
		vertex1, vertex2, vertex3 = faceList[i]
		
		# Surface area calculated by summing area of each triangular face
		surfaceArea+=triArea(vertex1,vertex2,vertex3, vertexList)
		
		# Volume calculated by the sum of signed volumes of tetrahedrons. Each tetrahedron is formed by the three vertices of a face on the object; the fourth point is the origin
		volume+=findtetraVolume(vertex1, vertex2, vertex3, vertexList)

		#We define each edge as a list of two vertices and sort so that duplicates can easily be deleted later
		edge1=sorted([vertex1, vertex2])
		edge2=sorted([vertex2, vertex3])
		edge3=sorted([vertex3, vertex1])
		
		# Add each edge to an edgeList
		edgeList.append(edge1)
		edgeList.append(edge3)
		edgeList.append(edge2)
	return surfaceArea, volume

# Find the number of holes in the obj file
def findNumHoles(vertexList, edgeList, faceList):
	# use Euler's Formula
	holes=int(-(len(vertexList)-len(edgeList)+len(faceList))/2+1)
	return holes

# Sphericity is an extra variable
def calculateSphericity(volume, surfaceArea):
    # Calculate the surface area of a sphere with the same volume as object
    r = (3/4*volume/math.pi)**(1/3)
    sa_sphere = 4*math.pi*r**2
    sphericity = sa_sphere/surfaceArea
    return sphericity

# Minscale is an extra variable
def determineMinScale(myX, plateauPoint):
    x = myX[plateauPoint]
    minscale = math.e**(-x)*1000
    return minscale