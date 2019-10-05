# test_SchoolDataJason.py
__version__ = "v20191005"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import SchoolDataJson


class Testing(unittest.TestCase):

    def test_school_data(self):
        self.assertEqual(SchoolDataJson.school_data_json("11344-2704", "First Last - Test 1", "tests/SO"),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11344-2704",
            "Order Subject": "First Last - Test 1",
            "Files": {
                "File 1": {
                    "File Name": "11344-2704.01 Test File.pdf",
                    "Page Count": "9"
                }
            },
            "Date Ordered": "Sep 28, 2019",
            "Ran": "False",
            "Email": "flast@domain.us",
            "Last Name": "Last",
            "First Name": "First",
            "Phone Number": "000-000-0000",
            "Building": "1",
            "Copies": "120",
            "Duplex": "Two-sided (back to back)",
            "Collation": "Collated",
            "Paper": "8.5 x 11 Paper White",
            "Stapling": "Upper Left - portrait",
            "Slip Sheets / Shrink Wrap": "Shrink wrap every 30 sets",
            "Deliver To Name": "Address="
        })
        self.assertEqual(SchoolDataJson.school_data_json("11345-3704", "First Last - Test 2", "tests/SO"),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11345-3704",
            "Order Subject": "First Last - Test 2",
            "Files": {
                "File 1": {
                    "File Name": "11345-3704.01 First Last - Test 2.pdf",
                    "Page Count": "9"
                }
            },
            "Date Ordered": "Sep 28, 2019",
            "Ran": "False",
            "Email": "flast@domain.us",
            "Last Name": "Last",
            "First Name": "First",
            "Phone Number": "000-000-0000",
            "Building": "1",
            "Copies": "125",
            "Duplex": "One-sided",
            "Collation": "Uncollated",
            "Paper": "8.5 x 11 Paper White",
            "Special Instructions": "Please make 25 copies of each page, UNCOLLATED. Please    separate the copied pages with a colored slip sheet. Please make 5 sets of the copied pages. Please separate the 5  sets with a different colored sheet of paper.",
            "Deliver To Name": "Address="
        })
        self.assertEqual(SchoolDataJson.school_data_json("11349-0311", "First Last - Test 3", "tests/SO"),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11349-0311",
            "Order Subject": "First Last - Test 3",
            "Files": {
                "File 1": {
                    "File Name": "11349-0311.01 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 2": {
                    "File Name": "11349-0311.02 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 3": {
                    "File Name": "11349-0311.03 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 4": {
                    "File Name": "11349-0311.04 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 5": {
                    "File Name": "11349-0311.05 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 6": {
                    "File Name": "11349-0311.06 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 7": {
                    "File Name": "11349-0311.07 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 8": {
                    "File Name": "11349-0311.08 First Last - Test File.pdf",
                    "Page Count": "1"
                },
                "File 9": {
                    "File Name": "11349-0311.09 First Last - Test File.pdf",
                    "Page Count": "1"
                }
            },
            "Date Ordered": "Sep 28, 2019",
            "Ran": "False",
            "Email": "flast@domain.us",
            "Last Name": "Last",
            "First Name": "First",
            "Phone Number": "000-000-0000",
            "Building": "1",
            "Copies": "100",
            "Duplex": "One-sided",
            "Collation": "Uncollated",
            "Paper": "8.5 x 11 Paper White",
            "Slip Sheets / Shrink Wrap": "between every 25",
            "Special Instructions": "Please make 4 complete class sets.",
            "Deliver To Name": "Address="

        })


if __name__ == '__main__':
    unittest.main()
