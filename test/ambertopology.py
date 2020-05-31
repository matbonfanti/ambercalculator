#! /usr/bin/env python

import unittest
from ambercalculator import AmberTopology
import os
import numpy as np
import math
import copy


######################################################################################################################

class TestAmberTopology(unittest.TestCase):

    # Name of the test topology file
    _TESTTOPOLOGYNAME = "parm.top"

    # mix and max number of line for the sections of the file with ATOM_NAME and CHARGE
    _CHARGELINES = (277, 1321)
    _ATOMNAMELINES = (6605, 6866)

    # ================================================================================================================

    def setUp(self):

        # define the path to the Test directory, where it is expected to find a test topology file
        testpath = os.path.dirname(os.path.realpath(__file__))
        # read the content of the topology file
        with open(os.path.join(testpath, self._TESTTOPOLOGYNAME)) as f:
            topotext = f.read()

        # extract the CHARGE and ATOM_NAME sections using the given line numbers
        self.atomnames, self.charge = [], []
        for line in topotext.splitlines()[self._ATOMNAMELINES[0]-1: self._ATOMNAMELINES[1]]:
            self.atomnames += line.split()
        for line in topotext.splitlines()[self._CHARGELINES[0]-1: self._CHARGELINES[1]]:
            # in the case of charge, there is also a conversion factor to trasform charges to AU
            self.charge += [float(c) / math.sqrt(332.0) for c in line.split()]

        # now create a AmberTopology instance with the content of this file
        self.testTopology = AmberTopology(topotext)

    # ================================================================================================================

    def test_getcharge(self):
        """Test the AmberTopology method that extracts values for charge from the topology file"""

        # compare the list of charges that has been "manually" extracted in setUp with the one from .charges attribute
        # compare the list of charges using the allclose function from numpy, to avoid problems
        # with numerical precision of the machine
        self.assertTrue(np.allclose(np.array(self.testTopology.charges),
                                    np.array(self.charge), atol=1.e-06))

    # ================================================================================================================

    def test_getatomnames(self):
        """Test the AmberTopology method that extracts atom names from the topology file"""

        # compare the list of atom names "manually" extracted in setUp with the one from .atoms attribute
        # the values are string, so there is no problem with representation of floating point numbers
        self.assertEqual(self.testTopology.atoms, self.atomnames)

    # ================================================================================================================

    def test_modifycharges(self):
        """Test the AmberTopology method that modify the list of charges in the topology file"""

        # first define a new list of random charges to include in the topology
        newcharges = list(np.random.uniform(-1., 1., len(self.charge)))
        # and now create a copy of the test topology with the charges modified
        copyTopology = self.testTopology.substitutecharges(newcharges)

        # now compare the charges defined in copyTopology with the one that have been given to substitutecharges
        self.assertTrue(np.allclose(np.array(copyTopology.charges),
                                    np.array(newcharges), atol=1.e-06))

    # ================================================================================================================

    def tearDown(self):
        del self.testTopology, self.atomnames, self.charge


######################################################################################################################

if __name__ == '__main__':
    unittest.main(verbosity=2)
