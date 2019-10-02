import unittest
import os
import sys
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import GDrive


class Testing(unittest.TestCase):

    # This Test May Fail if environment is not setup to run as in production.
    def test_GDrive(self):
        PATH = "tests/SO/00000 Drive Download Tests"
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        count = 0
        file_links = [line.rstrip('\n') for line in open(
            "Credentials/Sample_Drive_ID's.txt")]
        for ids in file_links:
            count += 1
            self.assertEqual(GDrive.Google_Drive_Downloader(
                ids, "00000", "tests/SO", "Drive Download Tests", count, ""), 1)
        shutil.rmtree(PATH)


if __name__ == '__main__':
    unittest.main()
