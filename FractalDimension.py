#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:47:15 2019
@author: daniel
"""
#from analyzeObj import analyzeObject
#from coralObject import Coral

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def fractal_dimension(array, dilation, max_box_size = None, min_box_size = 1, n_samples = 20, n_offsets = 0):
    """Calculates the fractal dimension of a 3D numpy array.
    
    Args:
        array (np.ndarray): The array to calculate the fractal dimension of.
        max_box_size (int): The largest box size, given as the power of 2 so that
                            2**max_box_size gives the sidelength of the largest box.                     
        min_box_size (int): The smallest box size, given as the power of 2 so that
                            2**min_box_size gives the sidelength of the smallest box.
                            Default value 1.
        n_samples (int): number of scales to measure over.
        n_offsets (int): number of offsets to search over to find the smallest set N(s) to
                       cover  all voxels>0.
        plot (bool): set to true to see the analytical plot of a calculation.
                            
        
    """
    #determine the scales to measure on
    if max_box_size == None:
        #default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = int(np.floor(np.log2(np.min(array.shape))))
    scales = np.floor(np.logspace(max_box_size,min_box_size, num = n_samples, base =2 ))
    scales = np.unique(scales) #remove duplicates that could occur as a result of the floor
    
    #get the locations of all non-zero pixels
    locs = np.where(array > 0)
    voxels = np.array([(x,y,z) for x,y,z in zip(*locs)])
    
    #count the minimum amount of boxes touched
    Ns = []
    #loop over all scales
    for scale in scales:
        touched = []
        if n_offsets == 0:
            offsets = [0]
        else:
            offsets = np.linspace(0, scale, n_offsets)
        #search over all offsets
        for offset in offsets:
            bin_edges = [np.arange(0, i, scale) for i in array.shape]
            bin_edges = [np.hstack([0-offset,x + offset]) for x in bin_edges]
            H1, e = np.histogramdd(voxels, bins = bin_edges)
            touched.append(np.sum(H1>0))
        Ns.append(touched)
    Ns = np.array(Ns)
    
    #From all sets N found, keep the smallest one at each scale
    Ns = Ns.min(axis=1)

    #Only keep scales at which Ns changed
    scales  = np.array([np.min(scales[Ns == x]) for x in np.unique(Ns)])
    
    Ns = np.unique(Ns)
    Ns = Ns[Ns > 0]
    scales = scales[:len(Ns)]
    #perform fit
    #rescale from dilation and mm to m
    X = -np.log((scales/dilation/1000))
    Y = np.log(np.unique(Ns))
    coeffs = np.polyfit(X, np.log(Ns),1)
    fd = coeffs[0]
    return fd, X, Y

def translateandScaleVertices(vertexList, translationCoordinates, dilation):
    [minX, minY, minZ] = translationCoordinates
    newVertexList = [(int((x-minX)*dilation), int((y-minY)*dilation), int((z-minZ)*dilation)) for (x, y, z) in vertexList]
    return newVertexList

def findOnlineFD(vertexList, boundBox, boxDimensions):
    dilation = 20
    shapeDimension = [int(x*dilation)+5 for x in boundBox]
    newVertexList = translateandScaleVertices(vertexList, boxDimensions[0:3], dilation)
    coralModel = np.zeros(shape = (shapeDimension))

    for vertex in newVertexList:
        coralModel[vertex]=1
    fd, X, Y = fractal_dimension(coralModel, dilation, n_offsets=10)

    print("Online fractal dimension: " + str(fd))
    return fd, X, Y

def findFromFDFile(filename):
    X, Y = [], []
    file = open(filename, 'r')
    for line in file:
        values = [float(s) for s in line.split()]
        #r=1 is 0.2mm, so convert the radius from 0.2mm to 1m
        X.append(np.log(values[1]/2))
        Y.append(values[3])
    file.close()
    m, b = np.polyfit(X, Y, 1)
    print("Jessica's fractal dimension of " + filename.split('\\')[-2] + " : " + str(3-m))
    return (3-m), X, Y

def createBox(length, numVertices):
    outputFile = "D:\Members\Cathy\\box\\box.obj"
    stepSize = length/numVertices
    box=[]

    with open(outputFile, 'a') as boxFile:
        boxFile.truncate(0)
        boxFile.write('#box created manually\n\n')
        for i in range(numVertices):
            for j in range(numVertices):
                vBot= f'v {i*stepSize} {j*stepSize} 0'
                vTop=f'v {i*stepSize} {j*stepSize} {length-1}'
                vLeft=f'v 0 {j*stepSize} {i*stepSize}'
                vRight=f'v {length-1} {i*stepSize} {j*stepSize}'
                vFront=f'v {i*stepSize} 0 {j*stepSize}'
                vBack=f'v {i*stepSize} {length-1} {j*stepSize}'
                boxFile.write(f'{vBot}\n{vTop}\n{vLeft}\n{vRight}\n{vFront}\n{vBack}\n')
        
        for x in range(6*numVertices*numVertices):
            if x%3==0:
                boxFile.write("\nf ")
            boxFile.write(str(x+1) + " ")

createBox(10, 1000)

def plot_3D_dataset(vertices):
    X=[]
    Y=[]
    Z=[]
    for vertex in vertices[:9999]:
        X.append(vertex[0])
        Y.append(vertex[1])
        Z.append(vertex[2])
    
    # Creating figure 
    fig = plt.figure(figsize = (10, 7)) 
    ax = plt.axes(projection ="3d") 
    
    # Creating plot 
    ax.scatter(X, Y, Z); 
    plt.title("simple 3D scatter plot") 
    
    # show plot 
    plt.show()

#createBox(10, 100)
"""
def checkOutOfBounds(newVertexList, oldVertexList, shapeDimension):
    for i in range(len(newVertexList)):
        [newX, newY, newZ] = newVertexList[i]
        if newX>shapeDimension[0]:
            print("x is out of bounds! " + str(newVertexList[i]) + " by this much " +str(newX-shapeDimension[0]))
        if newY>shapeDimension[1]: 
            print("y is out of bounds! " + str(newVertexList[i])+ " by this much " +str(newY-shapeDimension[1]))
        if newZ>shapeDimension[2]:
            print("z is out of bounds! " + str(newVertexList[i])+ " by this much " +str(newZ-shapeDimension[2]))


box = np.zeros(shape = (100,100,100))
box[20:80,20:80,20:80] = 1

fd = fractal_dimension(box, 10, n_offsets=10, plot = True)
print(f"Fractal Dimension of the box: {fd}")
plt.show()
"""