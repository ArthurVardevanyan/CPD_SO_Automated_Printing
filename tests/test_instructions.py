# test_instructions.py
__version__ = "v20191109"

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import instructions


class Testing(unittest.TestCase):

    def test_pass(self):
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "100",
        }), (1, 100))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "88",
            "Slip Sheets / Shrink Wrap": "Slip Sheets every 22 copies",
            "Special Instructions": "Please Deliver by Friday, September 27th",
        }), (4, 22))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "15",
            "Special Instructions": "Please Deliver by Friday, September 27th",
        }), (1, 15))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "125",
            "Special Instructions": "Please make 25 copies of each page, UNCOLLATED. Please separate the copied pages with a colored slip sheet. Please make 5 sets of the copied pages.",
        }), (5, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "125",
            "Slip Sheets / Shrink Wrap": "Please insert a colored slip sheet between  every 25 copies.",
        }), (5, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "120",
            "Special Instructions": "Please sort into 4 groups of 30 each with a divider between each set of 30.",
        }), (4, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "120",
            "Slip Sheets / Shrink Wrap": "please make 4 sets of 30 of the file. each page separated with a colored sheet",
        }), (4, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "30",
            "Slip Sheets / Shrink Wrap": "Insert a colorful slip sheet between each file.",
            "Special Instructions": "Please ship with Topic 4",
        }), (1, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "297",
            "Slip Sheets / Shrink Wrap": "Place a slip sheet after every 27 pages.",
        }), (11, 27))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "140",
            "Slip Sheets / Shrink Wrap": "please put a divider between every 28th copy",
        }), (5, 28))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please place a single slip sheet after each set of 25 copies.",
        }), (4, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "30",
            "Slip Sheets / Shrink Wrap": "slip sheets between documents (30 copies of each document)",
        }), (1, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "28",
            "Slip Sheets / Shrink Wrap": "No sheets necessary",
        }), (1, 28))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "90",
            "Slip Sheets / Shrink Wrap": "Please make 3 sets of 30, going to 3 different people",
        }), (3, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "between 25",
        }), (4, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "125",
            "Slip Sheets / Shrink Wrap": "Please shrink wrap every 25",
            "Special Instructions": "Please shrink wrap every 25",
        }), (5, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please separate into into two groups of 50",
        }), (2, 50))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "35",
            "Slip Sheets / Shrink Wrap": "Please insert a different colored slip sheet between every 7 copies",
        }), (5, 7))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "25",
            "Slip Sheets / Shrink Wrap": "Shrink Wrap set of 25 pages if possible. At least, slip sheet between every 25 pages.",
        }), (1, 25))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "160",
            "Slip Sheets / Shrink Wrap": "2 group of 80",
            "Special Instructions": "2 groups of 80",
        }), (2, 80))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "60",
            "Special Instructions": "2sided   Please divide the 60 copies in to 2 complete sets of 30 and slip sheet between each page within the file. UNCOLLATED 2 SIDED",
        }), (2, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "120",
            "Special Instructions": "2sided   Please divide the 120 copies in to 4 complete sets of 30 and slip sheet between each page within the file. UNCOLLATED 2 SIDED",
        }), (4, 30))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "360  ",
            "Special Instructions": "Please place colored slip sheets between  every 90 copies. (4 groups total)",
        }), (4, 90))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "150",
            "Slip Sheets / Shrink Wrap": "two stacks of 75",
            "Special Instructions": "two stacks of 75",
        }), (2, 75))
        

    def test_manual_input(self):
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "180",
            "Slip Sheets / Shrink Wrap": "Please insert a colored paper between sets. And between jobs.",
            "Special Instructions": "ONE SET OF 100 COPIES, AND ONE SET OF 80 COPIES.",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "155",
            "Special Instructions": "Page 1 Front: 3.1, Page 1 Back: 3.2, Page 2 Front: 3.3, Page 2 Back: 3.4",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "240",
            "Slip Sheets / Shrink Wrap": "insert slip sheet after 120 copies",
            "Special Instructions": "can send with other ch. 2 orders",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "88",
            "Slip Sheets / Shrink Wrap": "SLIP SHEETS between sets of 22 copies",
            "Special Instructions": "Please copy each page in the file front to back then make 90 of each of those.",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "100",
            "Slip Sheets / Shrink Wrap": "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied.",
            "Special Instructions": "Please shrink wrap each document into sets of 100. I only need pages 6-49 copied.",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "415",
            "Slip Sheets / Shrink Wrap": "Insert slip sheet between every 25 copies.",
        }), (0, 0))
        self.assertEqual(instructions.Special_Instructions({
            "Copies": "160",
            "Slip Sheets / Shrink Wrap": "Can each file be sorted into 2 groups of 60.",
            "Special Instructions": "Each file in 2 groups of 60",
        }), (0, 0))

    def test_default(self):
        self.assertEqual(instructions.default({"Order Number": "11344-2704"}),
                         str.encode('@PJL XCPT <value syntax="enum">3</value>\n'))
        self.assertEqual(instructions.default({
            "Stapling": "Upper Left - portrait",
        }), str.encode(''))
        self.assertEqual(instructions.default({
            "Stapling": "Upper Left - landscape",
        }), str.encode(''))
        self.assertEqual(instructions.default({
            "Drilling": "Yes",
        }), str.encode(''))
        self.assertEqual(instructions.default({
            "Drilling": "Yes",
            "Stapling": "Upper Left - landscape",
        }), str.encode(''))
        self.assertEqual(instructions.default({
            "Drilling": "Yes",
            "Stapling": "Upper Left - portrait",
        }), str.encode(''))

    def test_collation(self):
        self.assertEqual(instructions.collation({"Collation": "Collated"}, 1),
                         str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n'))
        self.assertEqual(instructions.collation({"Collation": "Uncollated"}, 1),
                         str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n'))

    def test_duplex(self):
        self.assertEqual(instructions.duplex({"Duplex": "Two-sided (back to back)"}),
                         (str.encode('@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n'), 2))
        self.assertEqual(instructions.duplex({"Duplex": "one-sided"}),
                         (str.encode('@PJL XCPT <sides syntax="keyword">one-sided</sides>\n'), 1))

    def test_stapling(self):
        self.assertEqual(instructions.stapling({}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode(''), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling({}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode(''), str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling({"Stapling": "Upper Left - portrait"}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">20</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling({"Stapling": "Upper Left - portrait"}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">20</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

        self.assertEqual(instructions.stapling({"Stapling": "Upper Left - landscape"}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">21</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))
        self.assertEqual(instructions.stapling({"Stapling": "Upper Left - landscape"}, str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')),
                         (str.encode('@PJL XCPT <value syntax="enum">21</value>\n'), str.encode('@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')))

    def test_drilling(self):
        self.assertEqual(instructions.drilling({"Drilling": "Yes"}),
                         str.encode('@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n'))
        self.assertEqual(instructions.drilling({}),
                         str.encode(''))

    def test_weight_extract(self):
        self.assertEqual(instructions.weight_extract({"Paper": "8.5 x 11 Paper White"}),
                         str.encode('@PJL XCPT <media-type syntax="keyword">use-ready</media-type>\n'))

        self.assertEqual(instructions.weight_extract({"Paper": "8.5 x 11 Card Stock White"}),
                         str.encode('@PJL XCPT <media-type syntax="keyword">stationery-heavyweight</media-type>\n'))

    def test_color_extract(self):
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper White"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">white</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Cad Stock White"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">white</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Canary"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">yellow</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Yellow"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">yellow</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Pink"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">pink</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Green"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">green</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Blue"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">blue</media-color>\n'))
        self.assertEqual(instructions.color_extract({"Paper": "8.5 x 11 Paper Ivory"}),
                         str.encode('@PJL XCPT <media-color syntax="keyword">ivory</media-color>\n'))

    def test_pjl_insert(self):
        self.assertFalse(instructions.pjl_insert({
            "Files": {
                "File 1": {
                    "File Name": "11344-2704.01 Test File.pdf",
                    "Page Count": "9"
                }
            },
            "Duplex": "Two-sided (back to back)",
            "Collation": "Collated",
            "Paper": "8.5 x 11 Paper White",
            "Stapling": "Upper Left - portrait",
        }, 30, 9))
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
