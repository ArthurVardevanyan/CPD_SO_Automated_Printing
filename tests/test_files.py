import unittest
import os
import sys
import files
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Testing(unittest.TestCase):

    def test_folder_list(self):
        self.assertEqual(files.folder_list("tests/SO"),
                         ["11344-2704 First Last - Test 1"])

    def test_file_list(self):
        self.assertEqual(files.file_list("tests/SO", "11344-2704 First Last - Test 1"),
                         ["11344-2704.01 Test File.pdf"])

    def test_postscript_list(self):
        self.assertEqual(files.postscript_list("tests/SO", "11344-2704 First Last - Test 1", "PSP"),
                         ["11344-2704.01 Test File.ps"])

    def test_page_counts(self):
        self.assertEqual(files.page_counts(
            "tests/SO", "11344-2704 First Last - Test 1"), 9)


if __name__ == '__main__':
    unittest.main()
