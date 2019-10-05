# test_Email.py
__version__ = "v20191005"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import Email


class Testing(unittest.TestCase):
    def test_subject_line(self):
        self.assertEqual(Email.subject_line(["OK", [[
            "(b'121234 (UID 121234 BODY[HEADER.FIELDS (Subject)] {00}'", "b'Subject: First Last - Copy Job - Test Job\r\n\r\n')"], "b')'"]]), "First Last - Test")
        remove = ("<", ">", "|", ".", ";", ":", "*", "?", "\\", "/", '"')
        for i in remove:
            self.assertEqual(Email.subject_line(["OK", [[
                "(b'121234 (UID 121234 BODY[HEADER.FIELDS (Subject)] {00}'", "b'Subject: First Last - Copy Job - Test "+i+"Job\r\n\r\n')"], "b')'"]]), "First Last - Test")

    def test_order_number_extract(self):
        with open('tests/SO/11344-2704 First Last - Test 1/11344-2704 First Last - Test 1.txt', 'r') as file:
            data = file.read()
        self.assertEqual(Email.order_number_extract(
            data, "-0351"), ('11344-0351', ""))

    def test_link_extractor(self):
        with open('Credentials/11349-0311.txt', 'r') as file:
            data = file.read()
        email_body = Email.link_extractor(str(data))
        self.assertEqual(len(email_body), 9)

    def test_link_cleanup(self):
        with open('Credentials/11349-0311.txt', 'r') as file:
            data = file.read()
        email_body = Email.link_extractor(str(data))
        self.assertEqual(len(Email.link_cleanup(email_body)), 9)

    def test_order_number_random(self):
        self.assertIn("-", Email.order_number_random())

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
