# test_files.py
__version__ = "v20200111"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import order as o
import files


class Testing(unittest.TestCase):

    def test_folder_list(self):
        self.assertEqual(files.folder_list("tests/SO"), [
            "11344-2704 First Last - Test 1",
            "11345-3704 First Last - Test 2",
            "11349-0311 First Last - Test 3",
            "Archive",  "Error"])

    def test_file_list(self):
        order = o.Order()
        order.OD = "tests/SO"
        order.NAME = "11344-2704 First Last - Test 1"
        self.assertEqual(files.file_list(order),
                         ["11344-2704.01 Test File.pdf"])

    def test_postscript_list(self):
        self.assertEqual(files.postscript_list("tests/SO", "11344-2704 First Last - Test 1", "PSP"),
                         ["11344-2704.01 Test File.ps"])

    def test_page_counts(self):
        order = o.Order()
        order.OD = "tests/SO"
        order.NAME = "11344-2704 First Last - Test 1"
        self.assertEqual(files.page_counts(order), 9)
        order.NAME = "11345-3704 First Last - Test 2"
        self.assertEqual(files.page_counts(order), 9)
        order.NAME = "11349-0311 First Last - Test 3"
        self.assertEqual(files.page_counts(order), 9)


if __name__ == '__main__':
    unittest.main()
