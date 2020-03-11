# test_Email.py
__version__ = "v20200310"

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

    def test_order_number_random(self):
        self.assertIn("-", Email.order_number_random())


if __name__ == '__main__':
    unittest.main()
