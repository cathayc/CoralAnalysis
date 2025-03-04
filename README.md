# Introduction #
Corals are mysterious creatures with highly complex, higher-dimensional structures. This project aims to analyze and characterize corals based on their fractal dimension, rather than the community standard of trait-based categorization. Fractal dimension offers a singular continuous variable for capturing the repetitive, fractial-nature, highly irregular corals.

Since most objects found in nature (e.g. trees, cauliflower, lungs, seashells, coastlines) are irregular, self-similar, and cannot be easily described by classical geometry, fractal geometry provides a useful perspective to analyze and model natural objects. Additionally, fractal dimension D is both orientation and size invariant, making re-scaling and re-orienting unnecessary. In recent years, the use of fractal dimension D with different calculation methods: Minkowski-Bouligand method, variation, and structure function method. 

This repository focuses on analysis of corals based on Minkowski-Bouligand method. This study is an individual project conducted in collaboration with [Professor Vianney Dennis](http://www.oc.ntu.edu.tw/oceng/?teacher=vianney-denis) at the [Functional Reef Ecology Lab](https://www.dipintothereef.com/people.html) at Institute of Oceanography, National Taiwan University.

# Suggested Walkthrough #
## Create and activate your virtual environment ##
1. Create a virtual environment by running `python3 -m venv .venv`
2. Activate your virtual environment: `source .venv/bin/activate`
3. Install the required packages: `pip install -r requirements.txt `

## Test run the analysis file ##
1. Open up `analyzeFromFile`
2. Run `analyzeFromFile`, and input `____coral-directory____/input/1029.obj`

The result will show itself on the output file `____coral-directory____/output/output.txt`, as well as 2 png files of the fractal dimension graph in the CoralFiles directory (`output/unrevised/__output-png__` and `output/plateau.__output-png__`).

# Description of each file #
* `analyzeFromFile.py`: Given a file, analyze all its components (fractal dimension, sphericity, surface area, volume, etc.)
* `coralObject.py`: The Coral object that stores all the coral information each time a coral is created, and performs analysis such as outputting a fractal dimension graph, visualizing the coral graph
* `analysisHelpers.py`: Helpers for coralObject.py to perform basic analysis on surface area, volume, bounding boxes
* `FractalDimension.py`: File that calculates fractal dimension
* `FDOutputGraphRevision.py`: Revises the graph so that it’s plotted to the plateau point.
* `analyzeFromDrive.py` : Since most of the .obj files are transferred via google drive, there is an `analyzeFromDrive.py` file. This file iterates through all the files in the folder and outputs the research, similarly, on a .txt file.

# Examples #
## .obj files used in research ##
The corals are kept in alreadyCutIncludePNG.zip. This includes all the coral files as well as the ones that have been cut to eliminate their non-characteristic parts. 

## Output Data ##
`output/output.txt`: result of running the program directly.
