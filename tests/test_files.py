# test_files.py
__version__ = "v20200208"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import log
import files
import order as o


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
        self.assertEqual(files.page_counts(order), (9, [
                         'Page Count: \x1b[35m9\x1b[0m FileName: 11344-2704.01 Test File.pdf']))
        order.NAME = "11345-3704 First Last - Test 2"
        self.assertEqual(files.page_counts(order), (9, [
                         'Page Count: \x1b[35m9\x1b[0m FileName: 11345-3704.01 First Last - Test 2.pdf']))
        order.NAME = "11349-0311 First Last - Test 3"
        self.assertEqual(files.page_counts(order), (9, [
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.01 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.02 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.03 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.04 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.05 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.06 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.07 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.08 First Last - Test File.pdf",
            "Page Count: \x1b[35m1\x1b[0m FileName: 11349-0311.09 First Last - Test File.pdf",
        ]))


if __name__ == '__main__':
    unittest.main()
