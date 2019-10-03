import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Email


class Testing(unittest.TestCase):
    def test_order_number_random(self):
        self.assertIn("101234-", Email.order_number_random("101234"))

    def test_duplex_test(self):
        self.assertEqual(Email.duplex_state(
            {"Duplex": "Two-sided (back to back)"}), 2)
        self.assertEqual(Email.duplex_state({"Duplex": "One-Sided"}), 1)

    def test_merging(self):
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
            },
            "Collation": "Uncollated",
        }, 11), 0)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Uncollated",
            "Stapling": "Upper Left - portrait",
        }, 3), 0)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Collated",
            "Stapling": "Upper Left - portrait",
        }, 3), 0)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Uncollated",
            "Stapling": "Upper Left - portrait",
        }, 3), 0)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Uncollated",
        }, 11), 1)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Duplex": "Two-sided (back to back)",
            "Collation": "Uncollated",
        }, 20), 1)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Uncollated",
        }, 20), 0)
        self.assertEqual(Email.merging({
            "Files": {
                "File 1": {},
                "File 2": {},
            },
            "Collation": "Collated",
        }, 11), 0)


if __name__ == '__main__':
    unittest.main()
