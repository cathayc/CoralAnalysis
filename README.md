# Introduction #
Corals are mysterious creatures with highly complex, higher-dimensional structures. This project aims to analyze and characterize corals based on their fractal dimension, rather than the community standard of trait-based categorization. Fractal dimension offers a singular continuous variable for capturing the repetitive, fractial-nature, highly irregular corals.

Since most objects (e.g. trees, cauliflower, lungs, seashells, coastlines) found in nature are irregular, self-similar, and cannot be easily described by classical geometry, fractal geometry provides a useful perspective to analyze and model natural objects. Additionally, fractal dimension D is both orientation and size invariant, making re-scaling and re-orienting unnecessary. In recent years, the use of fractal dimension D with different calculation methods: Minkowski-Bouligand method, variation, and structure function method. 

This repository focuses on analysis of corals based on Minkowski-Bouligand method. This research is conducted with the [https://www.dipintothereef.com/people.html](Functioanl Reef Ecology Lab) in Taiwan, which is headed by [http://www.oc.ntu.edu.tw/oceng/?teacher=vianney-denis](Professor Vianney Dennis).

# Suggested Walkthrough #
1. Open up `analyzeFromFile`
2. Change `output_filepath` on line 5 to `____coral–research-directory____/Outputs/output.txt`
3. Run `analyzeFromFile`, and input `____coral–research-directory____/CoralFiles/1493.obj`

The result will show itself on thee output file in Outputs directory, as well as 2 png files of the fractal dimension graph in thee CoralFiles directory.

# Description of each file #
* `analyzeFromFile.py`: Given a file, analyze all its components, including fractal dimension using analyzeObj
* `analyzeObj.py`: Actual analysis of the obj file. The file that analyzeFromFile depends on.
* `coralObject.py`: The object that stores all the coral information each time a coral is created. 
* `fractalDimension.py`: File that calculates fractal dimension
* `FDOutputGraphRevision.py`: Revises the graph so that it’s plotted to the plateau point.
* `extraVariableCalculation.py`: Currently used to calculate sphericity, but can also calculate some other things.
* `analyzeFromDrive.py` : Since most of the .obj files are transferred via google drive, there is an `analyzeFromDrive.py` file. This file iterates through all the files in the folder and outputs the research, similarly, on a .txt file.

# Examples #
## .obj files used in research ##
The corals are kept in alreadyCutIncludePNG.zip. This includes all the coral files as well as the ones that have been cut to eliminate their non-characteristic parts. 

## Output Data ##
`MasterData`: result of running the program directly.

# Original paper manuscript #
https://drive.google.com/file/d/1GjFXoJbpzT6qxme6W0jr7Peh5jjzYSRD/view?usp=sharing
