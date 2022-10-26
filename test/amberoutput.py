#! /usr/bin/env python

import unittest
from ambercalculator import AmberOutput, AmberSnapshot
import os
import tarfile


######################################################################################################################

class TestAmberOutput(unittest.TestCase):

    # Name of the archives containing the output of the two calculations: one MM optimization and one MD run
    _TEST_MD_ARCHIVE = "testMD.tgz"
    _TEST_OPT_ARCHIVE = "testOpt.tgz"
    # Names of the directories where the files from the archives will be extracted to
    _TEST_MD_DIR = "testMD"
    _TEST_OPT_DIR = "testOpt"

    # ================================================================================================================

    @classmethod
    def setUpClass(cls):

        # define the path to the Test directory, where it is expected to find a test topology file
        testpath = os.path.dirname(os.path.realpath(__file__))
        # extract output files from the archives _TEST_MD_ARCHIVE and _TEST_OPT_ARCHIVE
        with tarfile.open(os.path.join(testpath, cls._TEST_MD_ARCHIVE), "r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
        with tarfile.open(os.path.join(testpath, cls._TEST_OPT_ARCHIVE), "r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)

        # now parse output files with the AmberOutput class
        # when disposing the instance objects the directories will be removed (storeFiles=False)
        cls.MDOutput = AmberOutput(cls._TEST_MD_DIR, storeFiles=False)
        cls.OptOutput = AmberOutput(cls._TEST_OPT_DIR, storeFiles=False)

    # ================================================================================================================

    def test_optimizationplot(self):
        """Test the AmberOutput method that plots the information for an MM optimization run"""

        # write the plot to the pdf file "optimization.pdf"
        self.OptOutput.optimizationPlot(pdfFileName="optimization.pdf")
        # check whether the file is present in the working directory
        self.assertTrue(os.path.isfile("optimization.pdf"))

    # ================================================================================================================

    def test_equilibrationplot(self):
        """Test the AmberOutput method that plots the information for an MD equilibration run"""

        # write the plot to the pdf file "optimization.pdf"
        self.MDOutput.dynamicsPlot(pdfFileName="equilibration.pdf")
        # check whether the file is present in the working directory
        self.assertTrue(os.path.isfile("equilibration.pdf"))

    # ================================================================================================================

    def test_getgradient(self):
        """Test the AmberOutput method that extracts the energy gradient in the last snapshot of the MD run"""

        # compare the shape only of the gradient with the expected one, the gradient is too large to be
        # hard-coded here, and the extraction operated by AmberOutput is quite straightforward
        self.assertEqual(self.MDOutput.gradient.shape, (100, 5223, 3))

    # ================================================================================================================

    def test_getattribute(self):
        """Test the AmberOutput __getattr__ magic method that is used to access the data stored in dataDict"""

        # extract a tuple with the calculation types for the two tests
        types = (self.OptOutput.type, self.MDOutput.type)
        # this tuple should be equal to ("opt", "MD")
        self.assertEqual(types, ("opt", "MD"))

    # ================================================================================================================

    def test_getitem(self):
        """Test the AmberOutput __getitem__ magic method that is used to access the data stored in dataDict"""

        # extract a tuple with the calculation types for the two tests
        types = (self.OptOutput["type"], self.MDOutput["type"])
        # this tuple should be equal to ("opt", "MD")
        self.assertEqual(types, ("opt", "MD"))

    # ================================================================================================================

    def test_finalsnapshotopt(self):
        """Test the AmberOutput snapshot method with an optimization run to extract the final snapshot"""

        # extract the snaphot using .snapshot()
        extractSnap = self.OptOutput.snapshot(-1)
        # check that an AmberSnapshot instance was obtained
        self.assertEqual(type(extractSnap), AmberSnapshot)

    # ================================================================================================================

    def test_finalsnapshotMD(self):
        """Test the AmberOutput snapshot method with an MD run to extract the final snapshot"""

        # extract the snaphot using .snapshot()
        extractSnap = self.MDOutput.snapshot(-1)
        # check that an AmberSnapshot instance was obtained
        self.assertEqual(type(extractSnap), AmberSnapshot)

    # ================================================================================================================

    def test_intermsnapshotopt(self):
        """Test the AmberOutput snapshot method with an optimization run to extract an intermediate snapshot"""

        # extract the snaphot using .snapshot()
        extractSnap = self.OptOutput.snapshot(17)
        # check that an AmberSnapshot instance was obtained
        self.assertEqual(type(extractSnap), AmberSnapshot)

    # ================================================================================================================

    def test_intermsnapshotMD(self):
        """Test the AmberOutput snapshot method with an MD run to extract an intermediate snapshot"""

        # extract the snaphot using .snapshot()
        extractSnap = self.MDOutput.snapshot(54)
        # check that an AmberSnapshot instance was obtained
        self.assertEqual(type(extractSnap), AmberSnapshot)

    # ================================================================================================================

    @classmethod
    def tearDownClass(cls):
        del cls.MDOutput
        del cls.OptOutput


######################################################################################################################

if __name__ == '__main__':
    unittest.main(verbosity=2)
