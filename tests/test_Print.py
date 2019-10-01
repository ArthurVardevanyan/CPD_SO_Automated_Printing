import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Print


class Testing(unittest.TestCase):

    def test_folder_list(self):
        self.assertEqual(Print.printing("11344", "tests/SO", "162", 0, [], True, False),
                         "SUCCESS SPI! : 162 : 11344-2704 First Last - Test 1")


if __name__ == '__main__':
    unittest.main()
