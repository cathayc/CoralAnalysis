"""
    The file that finds fractal dimension.
    Also included in the file are functions to plot solid boxes and empty boxes.
        createSolidBox
        createEmptyBox
    Of course, you would expect to find the fd to be close to 3 for the solid box and close to 2 for the empty box.

    You will also find methods that plot the 3d object given vertices
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# from coralObject import Coral

current_directory = os.getcwd()

def main():
    # Create only if you don't already have the solid and shell vertices
    solidVertexList = createSolidBox(10, 200)
    # shellVertexList = createShellBox(10, 200)
    # findFromReichartFile("D:\Members\Cathy\\box\\solidBox.txt")
    # myCoral = Coral("/Users/cathychang/Desktop/Projects/CoralAnalysis/input/shellBox.obj")
    # fd, X, Y = myCoral.bucketFD()
    return None

# Doing bucket fractal dimension. We can change the number of samples here
def bucket_fractal_dimension(array, boxDimensions, n_samples = 30, max_box_size = None, min_box_size = 0.001):
    print("Doing bucket fractal dimension analysis. ")
    # determine the scales to measure on
    if max_box_size == None:
        #default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = (np.min(boxDimensions))
        print("Max box size: {} Min box size: {}".format(max_box_size, min_box_size))
    scales = np.geomspace(max_box_size, min_box_size, num = n_samples)
    scales = scales
    print("scales: {}".format(scales))

    X = []
    Y = []

    print("Starting to measure boxes")
    
    for scale_index in range(len(scales)):
        scale = scales[scale_index]
        touched=0
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

        if scale_index>5:
            if Y[scale_index]==Y[scale_index-5]:
                break
    coeffs = np.polyfit(X, Y, 1)
    fd = coeffs[0]
    print("Fractal dimension: {}".format(fd))
    return fd, X, Y

# Find fractal dimension using the box counting method
def findBucketFD(vertexList, boxDimensions):
    print("BOX DIMENSIONS: {}".format(boxDimensions))
    fd, X, Y = bucket_fractal_dimension(vertexList, boxDimensions)
    print("My fractal dimension: " + str(fd))
    return fd, X, Y

# Find fractal dimension using Reichart's file
def findFromReichartFile(filePath):
    print("\nFinding Reichart's fractal dimension")
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
            print("Reichart's fractal dimension of " + filePath.split('\\')[-1].strip(".txt") + " : " + str(3-m))
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

# Create a solid box in the input directory
def createSolidBox(length, numVertices):
    outputFile = os.path.join(current_directory, "input", "solidBox.obj")
    stepSize = length/numVertices
    vList=[]

    with open(outputFile, 'a') as boxFile:
        boxFile.truncate(0)
        for i in range(numVertices):
            for j in range(numVertices):
                for k in range(numVertices):
                    vList.append((i*stepSize, j*stepSize, k*stepSize))
                    v = f'v {i*stepSize} {j*stepSize} {k*stepSize}'
                    boxFile.write(f'{v}\n')
        for x in range(numVertices*numVertices*numVertices-1):
            if x%3==0:
                boxFile.write("\nf")
            boxFile.write(" {}/{}".format(str(x), str(x)))
        return vList

def createShellBox(length, numVertices):
    outputFile = os.path.join(current_directory, "input", "shellBox.obj")
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
    print("hi")