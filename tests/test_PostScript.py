import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import PostScript


class Testing(unittest.TestCase):

    def test_folder_list(self):
        self.assertIsNone(PostScript.postscript_conversion("11344-2704", "tests/SO"))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11344-2704 First Last - Test 1/PostScript/11344-2704.01 Test File.pdf.ps"))
        self.assertIsNone(PostScript.postscript_conversion("11345-3704", "tests/SO"))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11344-2704 First Last - Test 2/PostScript/11345-3704.01 Test File.pdf.ps"))
        self.assertIsNone(PostScript.postscript_conversion("11349-0311", "tests/SO"))
        self.assertTrue(True, os.path.exists(
            "tests/SO/11349-0311 First Last - Test 3.txt/PostScript/11349-0311.01 Test File.pdf.ps"))

    def test_file_merge(self):
        self.assertTrue(PostScript.file_merge("tests/SO", "11349-0311 First Last - Test 3", 1))
        
if __name__ == '__main__':
    unittest.main()
