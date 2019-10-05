# test_Print.py
__version__ = "v20191005"

import unittest
from unittest import mock
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Print


class Testing(unittest.TestCase):

    def test_order_selection(self):
        import files
        Folders = files.folder_list("tests/SO")
        Folders.pop()
        Folders.pop()
        for i in Folders:
            self.assertEqual(Print.order_selection(i[:5], Folders, True), i)
            with mock.patch('builtins.input', return_value=1):
                self.assertEqual(Print.order_selection(
                    i[:5], Folders, False), i)
            with mock.patch('builtins.input', return_value=0):
                self.assertEqual(Print.order_selection(
                    i[:5], Folders, False), "Aborted @ CO#: " + i)
            self.assertEqual(Print.order_selection(
                i[:5], "", True), "Order DNE: No Order Selected")
            self.assertEqual(Print.order_selection(
                i[:5], "", False), "ON Not Valid : " + i[:5])
        for i in Folders:
            self.assertEqual(Print.order_selection(i[:10], Folders, True), i)
            with mock.patch('builtins.input', return_value=1):
                self.assertEqual(Print.order_selection(
                    i[:10], Folders, False), i)
            with mock.patch('builtins.input', return_value=0):
                self.assertEqual(Print.order_selection(
                    i[:10], Folders, False), "Aborted @ CO#: " + i)
            self.assertEqual(Print.order_selection(
                i[:10], "", True), "Order DNE: No Order Selected")
            self.assertEqual(Print.order_selection(
                i[:10], "", False), "ON Not Valid : " + i[:10])
        for i in Folders:
            test = "invalid input"
            self.assertEqual(Print.order_selection(
                test, Folders, True), "Aborted @ INT: " + test)
            self.assertEqual(Print.order_selection(
                test, Folders, False), "Aborted @ INT: " + test)
        # Still need to test duplicate order numbers

    def test_impression_counter(self):
        self.assertFalse(Print.impression_counter(0, 0, 0))
        self.assertTrue(Print.impression_counter(0, 0, 1))
        self.assertTrue(Print.impression_counter(9, 10, 2))
        self.assertFalse(Print.impression_counter(9, 10, 2))

    def test_can_run(self):
        self.assertTrue(Print.can_run({"Paper": "8.5 x 11 Paper White"}, 0))
        self.assertFalse(Print.can_run({"Paper": "11 x 17 Paper White"}, 0))
        self.assertFalse(Print.can_run({"Paper": "11 x 17 Paper White"}, 1))
        self.assertFalse(Print.can_run({"Paper": "8.5 x 11 Paper Blue"}, 0))
        self.assertTrue(Print.can_run({"Paper": "8.5 x 11 Paper Blue"}, 1))
        self.assertFalse(Print.can_run(
            {"Front Cover": "8.5 x 11 Paper Blue"}, 0))
        self.assertFalse(Print.can_run(
            {"Back Cover": "8.5 x 11 Paper Blue"}, 0))
        self.assertFalse(Print.can_run(
            {"Front Cover": "8.5 x 11 Paper Blue"}, 1))
        self.assertFalse(Print.can_run(
            {"Back Cover": "8.5 x 11 Paper Blue"}, 1))
        self.assertTrue(Print.can_run(
            {"Paper": "8.5 x 11 Paper White", "Stapling": "Upper Left - portrait"}, 0))
        self.assertTrue(Print.can_run(
            {"Paper": "8.5 x 11 Paper White", "Stapling": "Upper Left - landscape"}, 0))
        self.assertFalse(Print.can_run(
            {"Paper": "8.5 x 11 Paper White", "Stapling": "Double Left - portrait"}, 0))
        self.assertFalse(Print.can_run({"Booklets": "Yes"}, 0))
        self.assertFalse(Print.can_run({"Booklets": "Yes"}, 1))

    def test_printing(self):
        self.assertEqual(Print.printing("11344", "tests/SO", "162", 0, [], True, False),
                         "SUCCESS SPI! : 162 : 11344-2704 First Last - Test 1")
        self.assertEqual(Print.printing("11345", "tests/SO", "162", 0, [], True, False),
                         "SUCCESS SPI! : 162 : 11345-3704 First Last - Test 2")
        self.assertEqual(Print.printing("11349", "tests/SO", "162", 0, [], True, False),
                         "SUCCESS SPI! : 162 : 11349-0311 First Last - Test 3")

    def test_main(self):
        with mock.patch('builtins.input', side_effect=[0,0,"run", 0]):
            self.assertEqual(Print.main(False), 1)
        with mock.patch('builtins.input', side_effect=[0,0,"run", 0]):
            self.assertEqual(Print.main(True), 1)
        with mock.patch('builtins.input', side_effect=[1,0,"run", 0]):
            self.assertEqual(Print.main(True), 1)
        with mock.patch('builtins.input', side_effect=[0,1,"run", 0]):
            self.assertEqual(Print.main(True), 1)
        with mock.patch('builtins.input', side_effect=[0,2,"run", 0]):
            self.assertEqual(Print.main(True), 1)
        with mock.patch('builtins.input', side_effect=[1,1,"run", 0]):
            self.assertEqual(Print.main(True), 1)
        with mock.patch('builtins.input', side_effect=[1,2,"run", 0]):
            self.assertEqual(Print.main(True), 1)
            
if __name__ == '__main__':
    unittest.main()
