#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:47:15 2019
@author: daniel
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def fractal_dimension(array, max_box_size = None, min_box_size = 1, n_samples = 20, n_offsets = 0, plot = False):
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
    coeffs = np.polyfit(np.log(1/scales), np.log(Ns),1)
    
    #make plot
    if plot:
        fig, ax = plt.subplots(figsize = (8,6))
        ax.scatter(np.log(1/scales), np.log(np.unique(Ns)), c = "teal", label = "Measured ratios")
        ax.set_ylabel("$\log N(\epsilon)$")
        ax.set_xlabel("$\log 1/ \epsilon$")
        fitted_y_vals = np.polyval(coeffs, np.log(1/scales))
        ax.plot(np.log(1/scales), fitted_y_vals, "k--", label = f"Fit: {np.round(coeffs[0],3)}X+{coeffs[1]}")
        ax.legend();
    return(coeffs[0])


def getVertexCoord(vert):
	xCoord=float(vert.lstrip('v ').split(' ')[0])
	yCoord=float(vert.lstrip('v ').split(' ')[1])
	zCoord=float(vert.lstrip('v ').split(' ')[2])
	
	return(xCoord,yCoord,zCoord)

def findVertices (fileName, vertexList):
    text = ""
    try:
        with open(fileName,'r') as file:
            text=file.read().splitlines()
            print("Coral file " + fileName + " found!")
    except IOError as e:
        print(fileName + " not found, please try another file:")

    # Build lists of all vertices and faces		
    for i in range(0, len(text)): 
        if len(text[i])>1:
            if text[i][0]=='v' and ' ' == text[i][1]:
                vertexList.append(getVertexCoord(text[i]))
                #vertexList.append(text[i])
    return vertexList

def plotFromFDFile(filename):
    X, Y = [], []
    for line in open(filename, 'r'):
        values = [float(s) for s in line.split()]
        #print(values)
        X.append(values[2])
        Y.append(values[3])
    m, b = np.polyfit(X, Y, 1)
    print("Fractal dimension of " + filename.split('/')[-2] + " : " + str(round(3-m, 3)))
    #print(b)
    #plt.plot(X, Y, 'o')
    #plt.plot(X, m*X[0] + b)
    #plt.show()

def plot_3D_dataset(vertices):
    X=[]
    Y=[]
    Z=[]
    for vertex in vertexList[:9999]:
        X.append(vertex[0]*100)
        Y.append(vertex[1]*100)
        Z.append(vertex[2]*100)
    
    # Creating figure 
    fig = plt.figure(figsize = (10, 7)) 
    ax = plt.axes(projection ="3d") 
    
    # Creating plot 
    ax.scatter(X, Y, Z); 
    plt.title("simple 3D scatter plot") 
    
    # show plot 
    plt.show() 


# -------------------------------
#           Main method
# -------------------------------

plotFromFDFile("D:\Members\Cathy/2512/2512.txt")
plotFromFDFile("D:\Members\Cathy/1358/1358.txt")
plotFromFDFile("D:\Members\Cathy/1493/1493.txt")
plotFromFDFile("D:\Members\Cathy/1600/1600.txt")
weirdarray=np.ones((2, 3, 4))
print(weirdarray)

#test data
box = np.zeros(shape = (100,100,100))
box[20:80,20:80,20:80] = 1
print(box.sum())

fd = fractal_dimension(box, n_offsets=10, plot = True)
print(f"Fractal Dimension of the box: {fd}")
plt.show()

#scale by 1000
vertexList = findVertices("D:\Members\Cathy/2512/2512.obj", [])*1000
#print(vertexList)
#plot_3D_dataset(vertexList)
