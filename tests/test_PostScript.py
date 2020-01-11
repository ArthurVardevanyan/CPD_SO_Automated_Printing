# test_PostScript.py
__version__ = "20200111"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import order as o
import PostScript


class Testing(unittest.TestCase):

    def test_folder_list(self):
        order = o.Order()
        order.OD = "tests/SO"
        order.NUMBER = "11344-2704"
        self.assertTrue(PostScript.postscript_conversion(order))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11344-2704 First Last - Test 1/PostScript/11344-2704.01 Test File.pdf.ps"))
        order.NUMBER = "11345-3704"
        self.assertTrue(PostScript.postscript_conversion(order))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11344-2704 First Last - Test 2/PostScript/11345-3704.01 Test File.pdf.ps"))
        order.NUMBER = "11349-0311"
        self.assertTrue(PostScript.postscript_conversion(order))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11349-0311 First Last - Test 3.txt/PostScript/11349-0311.01 Test File.pdf.ps"))

    def test_file_merge(self):
        order = o.Order()
        order.OD = "tests/SO"
        order.NUMBER = "11349-0311"
        order.NAME = "11349-0311 First Last - Test 3"
        self.assertTrue(PostScript.file_merge(order, 1))


if __name__ == '__main__':
    unittest.main()
