#!/usr/bin/env python3
__version__ = "v20190131"
import files
import printer
import Print
import log
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def main(ORDER_NUMBER,  OUTPUT_DIRECTORY, D110_IP, COLOR, AUTORUN, EMAILPRINT, BOOKLETS, COVERS, nup):
    print_que = []
    Orders = []
    output = Print.printing(Orders, str(ORDER_NUMBER), OUTPUT_DIRECTORY, D110_IP,
                            COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS, COVERS, nup)
    printer.print_processor(print_que)
    files.file_cleanup(Orders, OUTPUT_DIRECTORY)
    return output


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    log.logInit("webPrint")
    print = log.Print  # pylint: disable=unused-variable
    input = log.Input  # pylint: disable=unused-variable
    print(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
               sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]))
