from analyzeObj import analyzeObject
from coralObject import Coral
from FractalDimension import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mycoral2505 = analyzeObject("D:\Members\Cathy\\2505\\2505.obj")
vertexList = mycoral2505.getVertexList()
minmaxXYZ = mycoral2505.boxDimensions
numVertices = mycoral2505.numVertices