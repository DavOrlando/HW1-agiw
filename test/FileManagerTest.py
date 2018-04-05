'''
Created on 05 apr 2018

@author: davideorlando
'''
import os
import unittest

import src.FileManager as fileman


class Test(unittest.TestCase):
    
    
    def setUp(self):
        self.fm = fileman.FileManager()
        self.path="../resources"

    def tearDown(self):
        os.rmdir(self.path)
        pass


    def testMakeDir(self):
        self.fm.makeDir(self.path)
        self.assertTrue("resources" in os.listdir("../"),"Test makeDir fail")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()