from analyzeObj import analyzeObject
from FractalDimension import fractal_dimension
from coralObject import *
import unittest

#coral2505 = analyzeObject("D:\Members\Cathy\\2505\\2505.obj")


class testsAnalyzeObj(unittest.TestCase):
    # Make sure that if a file isn't found, the code returns None
    def test_invalidFile(self):
        file = "randomFile"
        res = analyzeObject(file)
        self.assertEqual(res, None)
    
    # Make sure that if a file is found, code executes and returns a coral object
    def test_workingCoralFile(self):
        file = "D:\Members\Cathy\\box\\box.obj"
        res = analyzeObject(file)
        if res != None:
            res = True
        self.assertEqual(res, True)
    
    def test_sphere(self):
        file = "D:\Members\Cathy\\sphere\\sphere.obj"
        res = analyzeObject(file)
        print(res)


if __name__ == '__main__':
    unittest.main()