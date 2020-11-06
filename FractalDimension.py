#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from analyzeObj import analyzeObject
#from coralObject import Coral 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation



def main():
    #boxVertexList = createSolidBox(10, 200)
    findFromFDFile("D:\Members\Cathy\\box\\solidBox.txt")
    #my_fractal_dimension(boxVertexList, [10, 10, 10])
    #fd, X, Y = bucket_fractal_dimension(boxVertexList, [10, 10, 10])
    return None

def bucket_fractal_dimension(array, boxDimensions, n_samples = 30, max_box_size = None, min_box_size = 0.001):
    print("Doing bucket fractal dimension analysis")
    #determine the scales to measure on
    if max_box_size == None:
        #default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = (np.min(boxDimensions))
        print("Max box size: {} Min box size: {}".format(max_box_size, min_box_size))
    scales = np.geomspace(max_box_size, min_box_size, num = n_samples)
    scales = scales
    print("scales: {}".format(scales))

    X = []
    Y = []

    print("Number of vertices: {}".format(len(array)))
    
    for scale_index in range(len(scales)):
        scale = scales[scale_index]
        touched=0
        print("Current scale measuring on: {}".format(scale))
        numX = int(boxDimensions[0]/scale+1)
        numY = int(boxDimensions[1]/scale+1)
        numZ = int(boxDimensions[2]/scale+1)

        myArray = []
        for i in range(len(array)):
            vertex = array[i]
            x = int(vertex[0]/scale)
            y = int(vertex[1]/scale)
            z = int(vertex[2]/scale)
            myArray.append((x, y, z))
        touched = len(set(myArray))

        X.append(-np.log(scale/1000))
        Y.append(np.log(touched))
        print("Touched: {}".format(touched))
        if scale_index>3:
            if Y[scale_index]==Y[scale_index-2]:
                break
    coeffs = np.polyfit(X, Y, 1)
    fd = coeffs[0]
    print(fd)
    return fd, X, Y

def remove_vertices(x, y, z, scale, array):
    print("Before length: {}".format(len(array)))
    updatedArray = [vertex for vertex in array if not(
                    x*scale <= vertex[0] <= (x+1)*scale and
                    y*scale <= vertex[1] <= (y+1)*scale and
                    z*scale <= vertex[2] <= (z+1)*scale)]
    print("After length: {}".format(len(updatedArray)))
    return updatedArray

def my_fractal_dimension(array, boxDimensions, n_samples = 20, max_box_size = None, min_box_size = 0.001):
    #determine the scales to measure on
    if max_box_size == None:
        #default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = np.log2(np.min(boxDimensions))
    scales = np.logspace(max_box_size, min_box_size, num = n_samples, base =2)
    print("scales: {}".format(scales))

    X= []
    Y= []
    for scale in scales:
        print("Finding scale: {}".format(scale))
        touched=0
        #print("Current scale measuring on: {}".format(scale))
        numX = int(boxDimensions[0]/scale)+1
        numY = int(boxDimensions[1]/scale)+1
        numZ = int(boxDimensions[2]/scale)+1
        for x in range(numX):
            for y in range(numY):
                for z in range(numZ):
                    vertex_index = 0
                    got_one = 0
                    #print("X, y, z: {}, {}. {}".format(x, y, z))
                    while got_one==0 and vertex_index<(len(array)):
                        #print("{}, ".format(vertex_index), end = " ")
                        if vertex_resides_in_box(array[vertex_index], x, y, z, scale):
                            got_one = 1
                            touched += 1
                            #print("\n\n\n I got touched! ")
                        vertex_index += 1
                    #print(vertex_index)
                    got_one = 0
                    #print("X is between {} and {}".format(x*scale, (x+1)*scale))
                    #print("Y is between {} and {}".format(y*scale, (y+1)*scale))
                    #print("Z is between {} and {}".format(z*scale, (z+1)*scale))
                    #vertices_in_box = [vertex for vertex in updatedVertices if 
                    #                    x*scale <= vertex[0] <= (x+1)*scale and
                    #                    y*scale <= vertex[1] <= (y+1)*scale and
                    #                    z*scale <= vertex[2] <= (z+1)*scale]
                    #updatedVertices = [vertex for vertex in updatedVertices if vertex not in vertices_in_box]
                    
                    #if len(vertices_in_box)>0:
                    #    touched+=1
                    #    updatedVertices = [vertex for vertex in updatedVertices if vertex not in vertices_in_box]
        
        # Add x and y data
        X.append(-np.log(scale/1000))
        Y.append(np.log(touched))
        print("Touched: {}".format(touched))
    #print("scale: {}\nY: {}".format(X, Y))
    coeffs = np.polyfit(X, Y,1)
    fd = coeffs[0]
    return fd, X, Y

def vertex_resides_in_box(vertex, x, y, z, scale):
    if (x*scale <= vertex[0] <= (x+1)*scale and
        y*scale <= vertex[1] <= (y+1)*scale and
        z*scale <= vertex[2] <= (z+1)*scale):
        return True

# Code found online; doesn't work        
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

def findMyFD(vertexList, boxDimensions):
    fd, X, Y = my_fractal_dimension(vertexList, boxDimensions)
    print("My fractal dimension: " + str(fd))
    return fd, X, Y

def findBucketFD(vertexList, boxDimensions):
    fd, X, Y = bucket_fractal_dimension(vertexList, boxDimensions)
    print("My fractal dimension: " + str(fd))
    return fd, X, Y

#Given a list of vertices, convert it to 3D numpy array 
def convertToNumpyArray(vertexList, shapeDimension):
    # First create the 3D array of vertices
    vertexArray = filledArray = np.zeros(shape = (shapeDimension))
    for vertex in vertexList:
        vertexArray[vertex]=1

    return vertexArray

def findOnlineFD(vertexList, boundBox, boxDimensions, sa):
    print("\nDoing online fractal dimension analysis")
    #find dilation
    numVertices = len(vertexList)
    dilation = numVertices/sa
    print("The dilation is: {}".format(dilation))
    dilation = 5
    shapeDimension = [int(x*dilation)+5 for x in boundBox]
    newVertexList = translateandScaleVertices(vertexList, boxDimensions[0:3], dilation)
    coralModel = convertToNumpyArray(newVertexList, shapeDimension)

    fd, X, Y = fractal_dimension(coralModel, dilation, n_offsets=10)

    print("Online fractal dimension: " + str(fd))
    return fd, X, Y

def findFromFDFile(filePath):
    print("\nFinding Jessica's fractal dimension")
    X, Y = [], []
    m = 0

    try:
        with open(filePath, 'r') as file:
            for line in file:
                values = [float(s) for s in line.split()]
                #r=1 is 0.2mm, so convert the radius from 0.2mm to 1m
                X.append(np.log(values[1]/2))
                Y.append(values[3])
            m, b = np.polyfit(X, Y, 1)
            print("Jessica's fractal dimension of " + filePath.split('\\')[-1].strip(".txt") + " : " + str(3-m))
            return (3-m), X, Y
    except IOError as e:
        print(filePath + " not found, please try another file:")
        return m, [0], [0]

def plot_3D_dataset(vertices):
    X=[]
    Y=[]
    Z=[]
    for vertex in vertices:
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

def plot_3D_numpy_array(array):
    xlen, ylen, zlen = array.shape
    x, y, z = array.nonzero()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, zdir='z', c= 'red')
    plt.show()

def createSolidBox(length, numVertices):
    outputFile = "D:\Members\Cathy\\box\\solidBox.obj"
    stepSize = length/numVertices
    vList=[]

    with open(outputFile, 'a') as boxFile:
        boxFile.truncate(0)
        boxFile.write('#box created manually\n\n')
        for i in range(numVertices):
            for j in range(numVertices):
                for k in range(numVertices):
                    vList.append((i*stepSize, j*stepSize, k*stepSize))
                    v = f'v {i*stepSize} {j*stepSize} {k*stepSize}'
                    boxFile.write(f'{v}\n')
        for x in range(numVertices*numVertices*numVertices):
            if x%3==0:
                boxFile.write("\nf")
            boxFile.write(" {}/{}".format(str(x), str(x)))
        return vList

def createEmptyBox(length, numVertices):
    outputFile = "D:\Members\Cathy\\box\\emptyBox.obj"
    stepSize = length/numVertices
    vList=[]

    with open(outputFile, 'a') as boxFile:
        boxFile.truncate(0)
        boxFile.write('#box created manually\n\n')
        for i in range(numVertices):
            for j in range(numVertices):
                vBot= f'v {i*stepSize} {j*stepSize} 0'
                vList.append((i*stepSize, j*stepSize, 0))

                vTop=f'v {i*stepSize} {j*stepSize} {length}'
                vList.append((i*stepSize, j*stepSize, length))

                vLeft=f'v 0 {j*stepSize} {i*stepSize}'
                vList.append((0, j*stepSize, i*stepSize))

                vRight=f'v {length} {i*stepSize} {j*stepSize}'
                vList.append((length, i*stepSize, j*stepSize))

                vFront=f'v {i*stepSize} 0 {j*stepSize}'
                vList.append((i*stepSize, 0, j*stepSize))

                vBack=f'v {i*stepSize} {length} {j*stepSize}'
                vList.append((i*stepSize, length, j*stepSize))

                boxFile.write(f'{vBot}\n{vTop}\n{vLeft}\n{vRight}\n{vFront}\n{vBack}\n')
        for x in range(6*numVertices*numVertices):
            if x%3==0:
                boxFile.write("\nf")
            boxFile.write(" {}/{}".format(str(x+1), str(x)))
        return vList

if __name__ == "__main__":
    main()
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


"""
box = np.zeros(shape = (10,10,10))

box[0:9, 0:9, 0] = 1
box[0, 0:9, 0:9] = 1
box[0:9, 0, 0:9] = 1
box[0:9, 0:9, 9] = 1
box[9, 0:9, 0:9] = 1
box[0:9, 9, 0:9] = 1
plot_3D_numpy_array(box)
print(fractal_dimension(box, 1))
"""