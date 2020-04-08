# test_instructions.py
__version__ = "v20200401"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import order as o
import instructions


class Testing(unittest.TestCase):

    def test_duplex_test(self):
        order = o.Order()
        order.DUPLEX = "Two-sided (back to back)"
        self.assertEqual(instructions.duplex_state(order), 2)
        order.DUPLEX = "One-Sided"
        self.assertEqual(instructions.duplex_state(order), 1)

    def test_merging(self):
        order = o.Order()
        FILE = o.Files()
        order.FILES.append(FILE)
        order.COLLATION = "Uncollated"
        order.PAGE_COUNTS = 11
        self.assertEqual(instructions.merging(order), 0)
        order.FILES.append(FILE)
        order.STAPLING = "Upper Left - portrait"
        order.PAGE_COUNTS = 3
        self.assertEqual(instructions.merging(order), 0)
        order.COLLATION = "Collated"
        order.PAGE_COUNTS = 3
        self.assertEqual(instructions.merging(order), 0)
        order.STAPLING = ""
        order.COLLATION = "Uncollated"
        order.PAGE_COUNTS = 11
        self.assertEqual(instructions.merging(order), 0)
        order.DUPLEX = "Two-sided (back to back)"
        order.PAGE_COUNTS = 20
        self.assertEqual(instructions.merging(order), 0)
        order.DUPLEX = "One-sided"
        order.COLLATION = "Uncollated"
        order.PAGE_COUNTS = 20
        self.assertEqual(instructions.merging(order), 0)
        order.COLLATION = "Collated"
        order.PAGE_COUNTS = 11
        self.assertEqual(instructions.merging(order), 0)

    def test_pass(self):
        order = o.Order()
        order.COPIES = 100
        self.assertEqual(instructions.Special_Instructions(order), (1, 100))
        order = o.Order()
        order.COPIES = 88
        order.SLIPSHEETS = 'Slip Sheets every 22 copies'
        order.SPECIAL_INSTRUCTIONS = "Please Deliver by Friday, September 27th"
        self.assertEqual(instructions.Special_Instructions(order), (4, 22))
        order = o.Order()
        order.COPIES = 15
        order.SPECIAL_INSTRUCTIONS = "Please Deliver by Friday, September 27th"
        self.assertEqual(instructions.Special_Instructions(order), (1, 15))
        order = o.Order()
        order.COPIES = 125
        order.SPECIAL_INSTRUCTIONS = "Please make 25 copies of each page, UNCOLLATED. Please separate the copied pages with a colored slip sheet. Please make 5 sets of the copied pages."
        self.assertEqual(instructions.Special_Instructions(order), (5, 25))
        order = o.Order()
        order.COPIES = 125
        order.SLIPSHEETS = "Please insert a colored slip sheet between  every 25 copies."
        self.assertEqual(instructions.Special_Instructions(order), (5, 25))
        order = o.Order()
        order.COPIES = 120
        order.SPECIAL_INSTRUCTIONS = "Please sort into 4 groups of 30 each with a divider between each set of 30."
        self.assertEqual(instructions.Special_Instructions(order), (4, 30))
        order = o.Order()
        order.COPIES = 120
        order.SLIPSHEETS = "please make 4 sets of 30 of the file. each page separated with a colored sheet"
        self.assertEqual(instructions.Special_Instructions(order), (4, 30))
        order = o.Order()
        order.COPIES = 30
        order.SLIPSHEETS = "Insert a colorful slip sheet between each file."
        order.SPECIAL_INSTRUCTIONS = "Please ship with Topic 4"
        self.assertEqual(instructions.Special_Instructions(order), (1, 30))
        order = o.Order()
        order.COPIES = 297
        order.SLIPSHEETS = "Place a slip sheet after every 27 pages."
        self.assertEqual(instructions.Special_Instructions(order), (11, 27))
        order = o.Order()
        order.COPIES = 140
        order.SLIPSHEETS = "please put a divider between every 28th copy"
        self.assertEqual(instructions.Special_Instructions(order), (5, 28))
        order = o.Order()
        order.COPIES = 100
        order.SLIPSHEETS = "Please place a single slip sheet after each set of 25 copies."
        self.assertEqual(instructions.Special_Instructions(order), (4, 25))
        order = o.Order()
        order.COPIES = 30
        order.SLIPSHEETS = "slip sheets between documents (30 copies of each document)"
        self.assertEqual(instructions.Special_Instructions(order), (1, 30))
        order = o.Order()
        order.COPIES = 28
        order.SLIPSHEETS = "No sheets necessary"
        self.assertEqual(instructions.Special_Instructions(order), (1, 28))
        order = o.Order()
        order.COPIES = 90
        order.SLIPSHEETS = "Please make 3 sets of 30, going to 3 different people"
        self.assertEqual(instructions.Special_Instructions(order), (3, 30))
        order = o.Order()
        order.COPIES = 100
        order.SLIPSHEETS = "between 25"
        self.assertEqual(instructions.Special_Instructions(order), (4, 25))
        order = o.Order()
        order.COPIES = 125
        order.SLIPSHEETS = "Please shrink wrap every 25"
        order.SPECIAL_INSTRUCTIONS = "Please shrink wrap every 25"
        self.assertEqual(instructions.Special_Instructions(order), (5, 25))
        order = o.Order()
        order.COPIES = 100
        order.SLIPSHEETS = "Please separate into into two groups of 50"
        self.assertEqual(instructions.Special_Instructions(order), (2, 50))
        order = o.Order()
        order.COPIES = 35
        order.SLIPSHEETS = "Please insert a different colored slip sheet between every 7 copies"
        self.assertEqual(instructions.Special_Instructions(order), (5, 7))
        order = o.Order()
        order.COPIES = 25
        order.SLIPSHEETS = "Shrink Wrap set of 25 pages if possible. At least, slip sheet between every 25 pages."
        self.assertEqual(instructions.Special_Instructions(order), (1, 25))
        order = o.Order()
        order.COPIES = 160
        order.SLIPSHEETS = "2 group of 80"
        order.SPECIAL_INSTRUCTIONS = "2 group of 80"
        self.assertEqual(instructions.Special_Instructions(order), (2, 80))
        order = o.Order()
        order.COPIES = 60
        order.SPECIAL_INSTRUCTIONS = "2sided   Please divide the 60 copies in to 2 complete sets of 30 and slip sheet between each page within the file. UNCOLLATED 2 SIDED"
        self.assertEqual(instructions.Special_Instructions(order), (2, 30))
        order = o.Order()
        order.COPIES = 120
        order.SPECIAL_INSTRUCTIONS = "2sided   Please divide the 120 copies in to 4 complete sets of 30 and slip sheet between each page within the file. UNCOLLATED 2 SIDED"
        self.assertEqual(instructions.Special_Instructions(order), (4, 30))
        order = o.Order()
        order.COPIES = 360
        order.SPECIAL_INSTRUCTIONS = "Please place colored slip sheets between  every 90 copies. (4 groups total)"
        self.assertEqual(instructions.Special_Instructions(order), (4, 90))
        order = o.Order()
        order.COPIES = 150
        order.SLIPSHEETS = "two stacks of 75"
        order. SPECIAL_INSTRUCTIONS = "two stacks of 75"
        self.assertEqual(instructions.Special_Instructions(order), (2, 75))
        order = o.Order()
        order.COPIES = 150
        order.SLIPSHEETS = "two sets of 75"
        self.assertEqual(instructions.Special_Instructions(order), (2, 75))
        order = o.Order()
        order.COPIES = 100
        order.SLIPSHEETS = "Please wrap into 4 sets of 25!"
        self.assertEqual(instructions.Special_Instructions(order), (4, 25))
        order = o.Order()
        order.COPIES = 90
        order.SLIPSHEETS = "Please divide into 3 sets going to 3 different teachers."
        order.SPECIAL_INSTRUCTIONS = "both are 2-sided"
        self.assertEqual(instructions.Special_Instructions(order), (3, 30))

    def test_manual_input(self):
        order = o.Order()
        order.COPIES = 180
        order.SLIPSHEETS = "Please insert a colored paper between sets. And between jobs."
        order.SPECIAL_INSTRUCTIONS = "ONE SET OF 100 COPIES, AND ONE SET OF 80 COPIES."
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 155
        order.SPECIAL_INSTRUCTIONS = "Page 1 Front: 3.1, Page 1 Back: 3.2, Page 2 Front: 3.3, Page 2 Back: 3.4"
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 240
        order.SLIPSHEETS = "insert slip sheet after 120 copies"
        order.SPECIAL_INSTRUCTIONS = "can send with other ch. 2 orders"
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 88
        order.SLIPSHEETS = "SLIP SHEETS between sets of 22 copies"
        order.SPECIAL_INSTRUCTIONS = "Please copy each page in the file front to back then make 90 of each of those."
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 100
        order.SLIPSHEETS = "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied."
        order.SPECIAL_INSTRUCTIONS = "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied."
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 415
        order.SLIPSHEETS = "Insert slip sheet between every 25 copies."
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 160
        order.SLIPSHEETS = "Can each file be sorted into 2 groups of 60."
        order.SPECIAL_INSTRUCTIONS = "Each file in 2 groups of 60"
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))
        order = o.Order()
        order.COPIES = 60
        order.SPECIAL_INSTRUCTIONS = "After cutting, please shrinkwrap in packs of 30. There should be 4 shrinkwrapped packs of 30 per file."
        self.assertEqual(instructions.Special_Instructions(order), (0, 0))

    def test_default(self):
        order = o.Order()
        order.NUMBER = "11344-2704"
        order.STAPLING_BOOL = False
        self.assertEqual(instructions.default(order),
                         str.encode('@PJL XCPT <value syntax="enum">3</value>\n'))
        order.STAPLING_BOOL = True
        self.assertEqual(instructions.default(order), str.encode(''))
        order.STAPLING_BOOL = True
        self.assertEqual(instructions.default(order), str.encode(''))
        order.STAPLING_BOOL = False
        order.DRILLING = "Yes"
        self.assertEqual(instructions.default(order), str.encode(''))
        order.STAPLING_BOOL = True
        self.assertEqual(instructions.default(order), str.encode(''))
        order.STAPLING_BOOL = True
        self.assertEqual(instructions.default(order), str.encode(''))

    def test_collation(self):
        order = o.Order()
        order.COLLATION = "Collated"
        self.assertEqual(instructions.collation(order),
                         str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n'))
        order.COLLATION = "Uncollated"
        self.assertEqual(instructions.collation(order),
                         str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n'))

    def test_duplex(self):
        order = o.Order()
        order.DUPLEX = "Two-sided (back to back)"
        self.assertEqual(instructions.duplex(order),
                         (str.encode('@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n'), 2))
        order.DUPLEX = "One-sided"
        self.assertEqual(instructions.duplex(order),
                         (str.encode('@PJL XCPT <sides syntax="keyword">one-sided</sides>\n'), 1))

    def test_stapling(self):
        order = o.Order()
        order.STAPLING = ""
        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode(''), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode(''), str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')))
        order.STAPLING = "Upper Left - portrait"
        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">20</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">20</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))
        order.STAPLING = "Upper Left - landscape"
        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">21</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))
        self.assertEqual(instructions.stapling(order, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">21</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

    def test_drilling(self):
        order = o.Order()
        order.DRILLING = "Yes"
        self.assertEqual(instructions.drilling(order),
                         str.encode('@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n'))
        order.DRILLING = ""
        self.assertEqual(instructions.drilling(order),
                         str.encode(''))

    def test_weight_extract(self):
        order = o.Order()
        order.PAPER = "8.5 x 11 Paper White"
        self.assertEqual(instructions.weight_extract(order),
                         str.encode('@PJL XCPT <media-type syntax="keyword">use-ready</media-type>\n'))
        order.PAPER = "8.5 x 11 Card Stock White"
        self.assertEqual(instructions.weight_extract(order),
                         str.encode('@PJL XCPT <media-type syntax="keyword">stationery-heavyweight</media-type>\n'))

    def test_color_extract(self):
        order = o.Order()
        order.PAPER = "8.5 x 11 Paper White"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">white</media-color>\n'))
        order.PAPER = "8.5 x 11 Card Stock White"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">white</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Canary"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">yellow</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Yellow"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">yellow</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Pink"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">pink</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Green"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">green</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Blue"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">blue</media-color>\n'))
        order.PAPER = "8.5 x 11 Paper Ivory"
        self.assertEqual(instructions.color_extract(order),
                         str.encode('@PJL XCPT <media-color syntax="keyword">ivory</media-color>\n'))

    def test_pjl_insert(self):
        order = o.Order()
        order.DUPLEX = "Two-sided (back to back)"
        order.COLLATION = "Collated"
        order.PAPER = "8.5 x 11 Paper White"
        order. STAPLING = "Upper Left - portrait"
        order.STAPLING_BOOL = True
        FILE = o.Files()
        FILE.NAME = "11344-2704.01 Test File.pdf"
        FILE.PAGE_COUNT = "9"
        order.PAGE_COUNTS = 9
        order.FILES.append(FILE)
        self.assertFalse(instructions.pjl_insert(order, 30))
        with open('PJL_Commands/input.ps', 'r') as f:
            data = f.readlines()
        count = 0
        for line in data:
            if '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>' in line:
                count += 1
            if '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>' in line:
                count += 1
            if '@PJL XCPT <media-type syntax="keyword">user-ready<media-type>' in line:
                count += 1
            if '@PJL XCPT <media-color syntax="keyword">white</media-color>' in line:
                count += 1
            if '@PJL XCPT <value syntax="enum">20</value>' in line:
                count += 1
        try:
            os.remove("PJL_Commands/input.ps")  # remove temp file
        except:
            self.fail("No File")
        if count != 4:
            self.fail(count)


if __name__ == '__main__':
    unittest.main()
