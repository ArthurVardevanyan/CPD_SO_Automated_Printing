import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Testing(unittest.TestCase):

    def test_folder_list(self):
        self.assertEqual(files.folder_list('tests/SO/11344-2704 First Last - Test 1/Tickets/11344-2704 First Last - Test 1.pdf'),
                         ["11344-2704 First Last - Test 1"])

   

if __name__ == '__main__':
    import files
    unittest.main()
