# test_integrity.py
__version__ = "v20200625"
import unittest
import os
import sys
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import integrity


class Testing(unittest.TestCase):

    def test_lpr(self):
        self.assertTrue(integrity.lpr())

    def test_lpq(self):
        self.assertTrue(integrity.lpq())

    def test_ghostscript(self):
        self.assertTrue(integrity.ghostscript())

    def test_wkhtmltopdf(self):
        self.assertTrue(integrity.wkhtmltopdf())

    def test_ansicon(self):
        self.assertTrue(integrity.ansicon())

    def test_internet(self):
        self.assertTrue(integrity.internet())


if __name__ == '__main__':
    unittest.main()
