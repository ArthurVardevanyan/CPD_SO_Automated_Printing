import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Print


class Testing(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
