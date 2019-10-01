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


if __name__ == '__main__':
    unittest.main()
