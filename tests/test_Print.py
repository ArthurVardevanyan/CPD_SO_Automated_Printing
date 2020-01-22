# test_Print.py
__version__ = "v20200122"
import unittest
from unittest import mock
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Print
import order as o
import log


class Testing(unittest.TestCase):

    def test_order_selection(self):
        log.logInit("test")
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
        order = o.Order()
        order.PAGE_COUNTS = 0
        order.COPIES = 0
        self.assertFalse(Print.impression_counter(order, 0))
        order.PAGE_COUNTS = 0
        order.COPIES = 0
        self.assertTrue(Print.impression_counter(order, 1))
        order.PAGE_COUNTS = 9
        order.COPIES = 10
        self.assertTrue(Print.impression_counter(order, 2))
        order.PAGE_COUNTS = 9
        order.COPIES = 10
        self.assertFalse(Print.impression_counter(order, 2))

    def test_can_run(self):
        order = o.Order()
        order.PAPER = "8.5 x 11 Paper White"
        self.assertTrue(Print.can_run(order, 0, 0, 0))
        order.PAPER = "11 x 17 Paper White"
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.PAPER = "11 x 17 Paper White"
        self.assertFalse(Print.can_run(order, 1, 0, 0))
        order.PAPER = "8.5 x 11 Paper Blue"
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.PAPER = "8.5 x 11 Paper Blue"
        self.assertTrue(Print.can_run(order, 1, 0, 0))
        order.FRONT_COVER = "8.5 x 11 Paper Blue"
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.BACK_COVER = "8.5 x 11 Paper Blue"
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.FRONT_COVER = "8.5 x 11 Paper Blue"
        self.assertFalse(Print.can_run(order, 1, 0, 0))
        order.BACK_COVER = "8.5 x 11 Paper Blue"
        self.assertFalse(Print.can_run(order, 1, 0, 0))
        order.FRONT_COVER = ""
        order.BACK_COVER = ""
        order.PAPER = "8.5 x 11 Paper White"
        order.STAPLING_BOOL = True
        self.assertTrue(Print.can_run(order, 0, 0, 0))
        order.PAPER = "8.5 x 11 Paper White"
        order.STAPLING_BOOL = True
        self.assertTrue(Print.can_run(order, 0, 0, 0))
        order.PAPER = "8.5 x 11 Paper White"
        order.STAPLING_BOOL = True
        self.assertTrue(Print.can_run(order, 0, 0, 0))
        order.STAPLING_BOOL = False
        order.BOOKLET = "Yes"
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.BOOKLET = "Yes"
        self.assertTrue(Print.can_run(order, 1, 1, 0))
        order.SPECIAL_INSTRUCTIONS = "please print each file on a different color- the  specific color "
        self.assertFalse(Print.can_run(order, 0, 0, 0))
        order.SPECIAL_INSTRUCTIONS = "Please print in color."
        self.assertFalse(Print.can_run(order, 0, 0, 0))

    def test_printing(self):
        log.logInit("test")
        self.assertEqual(Print.printing([], "11344", "tests/SO", 1, 0, [], True, False, 0, 0, 0),
                         "SUCCESS SPI! : 162 : 11344-2704 First Last - Test 1")
        self.assertEqual(Print.printing([], "11345", "tests/SO", 1, 0, [], True, False, 0, 0, 0),
                         "SUCCESS SPI! : 162 : 11345-3704 First Last - Test 2")
        self.assertEqual(Print.printing([], "11349", "tests/SO", 1, 0, [], True, False, 0, 0, 0),
                         "SUCCESS SPI! : 162 : 11349-0311 First Last - Test 3")

    def test_main(self):
        with mock.patch('builtins.input', side_effect=[0, "run", 0]):
            self.assertEqual(Print.main(False, 0, 0, 0, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[0, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 0, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[0, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 1, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[1, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 0, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[2, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 1, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[1, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 1, 0, 0, 0), 1)
        with mock.patch('builtins.input', side_effect=[2, "run", 0]):
            self.assertEqual(Print.main(True, 0, 0, 1, 0, 0, 0), 1)
        for i in range(3):
            with mock.patch('builtins.input', side_effect=[i, "run", 0]):
                self.assertEqual(Print.main(True, 0, 0, 1, 0, 0, 0), 1)
            with mock.patch('builtins.input', side_effect=[i, "run", 0]):
                self.assertEqual(Print.main(True, 0, 1, 1, 0, 0, 0), 1)
            with mock.patch('builtins.input', side_effect=[i, 0, 0, 0]):
                self.assertEqual(Print.main(True, 1, 1, 1, 0, 0, 0), 1)
            with mock.patch('builtins.input', side_effect=[i, 0, 0, 0]):
                self.assertEqual(Print.main(True, 1, 0, 1, 0, 0, 0), 1)


if __name__ == '__main__':
    unittest.main()
