#! /usr/bin/env python

import unittest
from ambercalculator import AmberInput
import os


######################################################################################################################

class TestAmberInput(unittest.TestCase):

    # names of the files that will be used to write the input
    _INPUTFILENAME1 = "amber01.in"
    _INPUTFILENAME2 = "amber02.in"

    # ================================================================================================================

    def setUp(self):

        # create an input file with default values
        self.testInput1 = AmberInput()
        # write the input text to file
        with open(self._INPUTFILENAME1, "w") as f:
            f.write(self.testInput1.inputtext)

        # create another input file with non-default values
        self.testInput2 = AmberInput(minimize=False, nrSteps=100, deltaT=0.002, temperature=300., pressure=1.,
                                     cutoff=9.0, freezeH=True, nprntsteps=10, usevelocity=True, usePBC=True)
        # write the input text to file
        with open(self._INPUTFILENAME2, "w") as f:
            f.write(self.testInput2.inputtext)

    # ================================================================================================================

    def test_input1_consistency(self):
        """Test the consistency of input reading and writing, using an input with default values"""

        # read the first input file and create a new instance of AmberInput
        with open(self._INPUTFILENAME1, "r") as f:
            readInput = AmberInput.readinput(f.read())
        # check if the new instance and the old instance are identical
        self.assertEqual(readInput, self.testInput1)

    # ================================================================================================================

    def test_input2_consistency(self):
        """Test the consistency of input reading and writing, using an input with non-default values"""

        # read the first input file and create a new instance of AmberInput
        with open(self._INPUTFILENAME2, "r") as f:
            readInput = AmberInput.readinput(f.read())
        # check if the new instance and the old instance are identical
        self.assertEqual(readInput, self.testInput2)

    # ================================================================================================================

    def test_getandsetitem(self):
        """Check whether the __getitem__ and __setitem__ magic methods are correctly defined"""

        # new instance of amberinput
        testInput1 = AmberInput()
        # modify some existing keyword and create a new one
        testInput1["cut"] = "200"  # existing keyword
        testInput1["pippo"] = "pluto"  # new keyword
        # now extract the values assigned to the two keywords
        valuelist = [testInput1["cut"], testInput1["pippo"]]
        # and check that the value correspond
        self.assertEqual(valuelist, ["200", "pluto"])

    # ================================================================================================================

    def tearDown(self):
        del self.testInput1, self.testInput2
        # remove files that have been written during test
        os.remove(self._INPUTFILENAME1)
        os.remove(self._INPUTFILENAME2)


######################################################################################################################

if __name__ == '__main__':
    unittest.main(verbosity=2)
