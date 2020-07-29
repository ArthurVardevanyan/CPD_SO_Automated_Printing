# test_SchoolDataJason.py
__version__ = "v20200128"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import jsonData
import order as o


class Testing(unittest.TestCase):
    def test_json_data(self):
        self.maxDiff = None
        order = o.Order()
        order.OD = "tests/SO"
        order.NUMBER = "11344-2704"
        order.SUBJECT = "First Last - Test 1"
        order.NAME = "".join([ order.NUMBER, " ",  order.SUBJECT])
        self.assertEqual(jsonData.json_data(order),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11344-2704",
            "Order Subject": "First Last - Test 1",
            "Email ID": "0000000000000000000000000001",
            "Files": {
                "File 1": {
                    "File Name": "11344-2704.01 Test File.pdf",
                    "Page Count": "9"
                }
            },
            "Status":order.status,
            "Date Ordered": "Sep 28, 2019",
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
            "Deliver To Name": "First Last",
            "Deliver To Address": "Address1",
            "Cost": order.COST
        })
        order.OD = "tests/SO"
        order.NUMBER = "11345-3704"
        order.SUBJECT = "First Last - Test 2"
        order.NAME = "".join([ order.NUMBER, " ",  order.SUBJECT])
        self.assertEqual(jsonData.json_data(order),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11345-3704",
            "Order Subject": "First Last - Test 2",
            "Email ID": "0000000000000000000000000002",
            "Files": {
                "File 1": {
                    "File Name": "11345-3704.01 First Last - Test 2.pdf",
                    "Page Count": "9"
                }
            },
            "Status":order.status,
            "Date Ordered": "Sep 28, 2019",
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
            "Deliver To Name": "First Last",
            "Deliver To Address": "Address1",
            "Cost": order.COST
        })
        order.OD = "tests/SO"
        order.NUMBER = "11349-0311"
        order.SUBJECT = "First Last - Test 3"
        order.NAME = "".join([ order.NUMBER, " ",  order.SUBJECT])
        self.assertEqual(jsonData.json_data(order),
                         {
            "Account ID": "CHANGE ME",
            "Order Number": "11349-0311",
            "Order Subject": "First Last - Test 3",
            "Email ID": "0000000000000000000000000003",
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
            "Status":order.status,
            "Date Ordered": "Sep 28, 2019",
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
            "Deliver To Name": "First Last",
            "Deliver To Address": "Address1",
            "Cost": order.COST
        })


if __name__ == '__main__':
    unittest.main()
