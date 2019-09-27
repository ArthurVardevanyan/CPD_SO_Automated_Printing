import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class TestCalc(unittest.TestCase):

    def test_pass(self):
        self.assertEqual(spi.Special_Instructions({
            "Copies": "100",
        }), (1, 100))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "88",
            "Slip Sheets / Shrink Wrap": "Slip Sheets every 22 copies",
            "Special Instructions": "Please Deliver by Friday, September 27th",
        }), (4, 22))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "15",
            "Special Instructions": "Please Deliver by Friday, September 27th",
        }), (1, 15))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "125",
            "Special Instructions": "Please make 25 copies of each page, UNCOLLATED. Please separate the copied pages with a colored slip sheet. Please make 5 sets of the copied pages.",
        }), (5, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "125",
            "Slip Sheets / Shrink Wrap": "Please insert a colored slip sheet between  every 25 copies.",
        }), (5, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "120",
            "Special Instructions": "Please sort into 4 groups of 30 each with a divider between each set of 30.",
        }), (4, 30))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "120",
            "Slip Sheets / Shrink Wrap": "please make 4 sets of 30 of the file. each page separated with a colored sheet",
        }), (4, 30))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "30",
            "Slip Sheets / Shrink Wrap": "Insert a colorful slip sheet between each file.",
            "Special Instructions": "Please ship with Topic 4",
        }), (1, 30))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "297",
            "Slip Sheets / Shrink Wrap": "Place a slip sheet after every 27 pages.",
        }), (11, 27))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "140",
            "Slip Sheets / Shrink Wrap": "please put a divider between every 28th copy",
        }), (5, 28))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please place a single slip sheet after each set of 25 copies.",
        }), (4, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "30",
            "Slip Sheets / Shrink Wrap": "slip sheets between documents (30 copies of each document)",
        }), (1, 30))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "28",
            "Slip Sheets / Shrink Wrap": "No sheets necessary",
        }), (1, 28))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "90",
            "Slip Sheets / Shrink Wrap": "Please make 3 sets of 30, going to 3 different people",
        }), (3, 30))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "between 25",
        }), (4, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "125",
            "Slip Sheets / Shrink Wrap": "Please shrink wrap every 25",
            "Special Instructions": "Please shrink wrap every 25",
        }), (5, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please separate into into two groups of 50",
        }), (2, 50))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "35",
            "Slip Sheets / Shrink Wrap": "Please insert a different colored slip sheet between every 7 copies",
        }), (5, 7))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "25",
            "Slip Sheets / Shrink Wrap": "Shrink Wrap set of 25 pages if possible. At least, slip sheet between every 25 pages.",
        }), (1, 25))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "160",
            "Slip Sheets / Shrink Wrap": "2 group of 80",
            "Special Instructions": "2 groups of 80",
        }), (2, 80))
        

    def test_manual_input(self):
        self.assertEqual(spi.Special_Instructions({
            "Copies": "180",
            "Slip Sheets / Shrink Wrap": "Please insert a colored paper between sets. And between jobs.",
            "Special Instructions": "ONE SET OF 100 COPIES, AND ONE SET OF 80 COPIES.",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "155",
            "Special Instructions": "Page 1 Front: 3.1, Page 1 Back: 3.2, Page 2 Front: 3.3, Page 2 Back: 3.4",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "240",
            "Slip Sheets / Shrink Wrap": "insert slip sheet after 120 copies",
            "Special Instructions": "can send with other ch. 2 orders",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "88",
            "Slip Sheets / Shrink Wrap": "SLIP SHEETS between sets of 22 copies",
            "Special Instructions": "Please copy each page in the file front to back then make 90 of each of those.",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied.",
            "Special Instructions": "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied.",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "415",
            "Slip Sheets / Shrink Wrap": "Insert slip sheet between every 25 copies.",
        }), (0, 0))
        self.assertEqual(spi.Special_Instructions({
            "Copies": "160",
            "Slip Sheets / Shrink Wrap": "Can each file be sorted into 2 groups of 60.",
            "Special Instructions": "Each file in 2 groups of 60",
        }), (0, 0))
        


if __name__ == '__main__':
    import spi
    unittest.main()
