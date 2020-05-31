#! /usr/bin/env python

import unittest
from ambercalculator import AmberSnapshot
import os
import numpy as np
import math
import copy


######################################################################################################################

class TestAmberSnapshot(unittest.TestCase):

    # number of atoms of the test
    _NATOMS = 42

    # names of the files that will be used to write the input
    _CRDFILENAME1 = "amber01.crd"
    _CRDFILENAME2 = "amber02.crd"
    _CRDFILENAME3 = "amber03.crd"

    # ================================================================================================================

    def setUp(self):

        # create sets of random numbers to fill the instances of AmberSnapshots
        coordinates = np.random.uniform(-100., 100., self._NATOMS*3).reshape((-1, 3)).transpose()
        velocities = np.random.uniform(-1.e-6, 1.e-6, self._NATOMS*3).reshape((-1, 3)).transpose()
        angles = np.array([109.4712190, 109.4712190, 109.4712190]) / 180. * math.pi
        unitcell = np.concatenate((np.random.uniform(0., 500., 3), angles))

        # create different variants of snapshots files
        self.testSnapshot1 = AmberSnapshot(coords=coordinates, unitcell=unitcell, velocity=velocities)
        self.testSnapshot2 = AmberSnapshot(coords=coordinates, unitcell=unitcell, velocity=None)
        self.testSnapshot3 = AmberSnapshot(coords=coordinates, unitcell=None, velocity=None)

        # write the different crd's to files
        with open(self._CRDFILENAME1, "w") as f:
            f.write(self.testSnapshot1.crdtext)
        with open(self._CRDFILENAME2, "w") as f:
            f.write(self.testSnapshot2.crdtext)
        with open(self._CRDFILENAME3, "w") as f:
            f.write(self.testSnapshot3.crdtext)

    # ================================================================================================================

    def test_equality_complete(self):
        """Test the AmberSnapshot equality with a full instance including also velocity and unitcell"""

        # make an identical copy of self.testSnapshot1
        identicalCopy = copy.deepcopy(self.testSnapshot1)
        # and test that the two instances are equal
        self.assertEqual(self.testSnapshot1, identicalCopy)

    # ================================================================================================================

    def test_equality_coordsandunit(self):
        """Test the AmberSnapshot equality with an instance including coordinates and unitcell"""

        # make an identical copy of self.testSnapshot1
        identicalCopy = copy.deepcopy(self.testSnapshot2)
        # and test that the two instances are equal
        self.assertEqual(self.testSnapshot2, identicalCopy)

    # ================================================================================================================

    def test_equality_coordsonly(self):
        """Test the AmberSnapshot equality with an instance including only coordinates"""

        # make an identical copy of self.testSnapshot1
        identicalCopy = copy.deepcopy(self.testSnapshot3)
        # and test that the two instances are equal
        self.assertEqual(self.testSnapshot3, identicalCopy)

    # ================================================================================================================

    def test_crd1_consistency(self):
        """Test the consistency of crd reading and writing, using an instance with coords, vel.s and unitcell"""

        # read the first input file and create a new instance of AmberInput
        with open(self._CRDFILENAME1, "r") as f:
            readCrd = AmberSnapshot.readcrd(f.read())
        # check if the new instance and the old instance are identical
        self.assertEqual(readCrd, self.testSnapshot1)

    # ================================================================================================================

    def test_crd2_consistency(self):
        """Test the consistency of crd reading and writing, using an instance with coords and unitcell"""

        # read the first input file and create a new instance of AmberInput
        with open(self._CRDFILENAME2, "r") as f:
            readCrd = AmberSnapshot.readcrd(f.read())
        # check if the new instance and the old instance are identical
        self.assertEqual(readCrd, self.testSnapshot2)

    # ================================================================================================================

    def test_crd3_consistency(self):
        """Test the consistency of crd reading and writing, using an instance with coords only"""

        # read the first input file and create a new instance of AmberInput
        with open(self._CRDFILENAME3, "r") as f:
            readCrd = AmberSnapshot.readcrd(f.read())
        # check if the new instance and the old instance are identical
        self.assertEqual(readCrd, self.testSnapshot3)

    # ================================================================================================================

    def tearDown(self):
        del self.testSnapshot1, self.testSnapshot2, self.testSnapshot3
        # remove files that have been written during test
        os.remove(self._CRDFILENAME1)
        os.remove(self._CRDFILENAME2)
        os.remove(self._CRDFILENAME3)

    ######################################################################################################################


if __name__ == '__main__':
    unittest.main(verbosity=2)
