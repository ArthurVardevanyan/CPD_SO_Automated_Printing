# test_tests.py
__version__ = "v20191005"

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest

# https://stackoverflow.com/a/1732477

testmodules = [
    'test_GDrive',
    'test_EmailPrint',
    'test_PostScript',
    'test_files',
    'test_SchoolDataJson',
    'test_instructions',
    'test_Email',
    'test_Print',
]
# RUN AT LEAST ONCE BEFORE CHECKING RESULTS
# FIRST RUN WILL GENERATE FILES NEEDED FOR SOME TESTS

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
