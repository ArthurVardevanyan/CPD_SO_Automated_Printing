# PostScript.py
__version__ = "v2020026"
# Built-In Libraries
from pdfImposer import pdfImposer
import files
from PyPDF2.pdf import PageObject
from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2
import json
import os
import glob
import sys
import locale
import subprocess
import log
print = log.Print
input = log.Input
if(os.name == "posix"):
    GHOSTSCRIPT_PATH = 'gs'
else:
    GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'
# Grayscale Ghostscript Parameter
# https://gist.github.com/firstdoit/6390547


def ghostscript(gsCMD):
    output = subprocess.Popen(gsCMD, stdout=subprocess.PIPE, shell=True)
    (out, err) = output.communicate()  # pylint: disable=unused-variable
    out = str(out).replace("b'GPL Ghostscript 9.27 (2019-04-04)\\nCopyright (C) 2018 Artifex Software, Inc.  All rights reserved.\\nThis software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:\\nsee the file COPYING for details.\\n", "")
    out = out.split("\\n")
    for line in out:
        log.logger.debug(line)
    return 1


def ticket_conversion(PATH):
    # https://stackoverflow.com/questions/39574096/how-to-delete-pages-from-pdf-file-using-python
    pdf = PyPDF2.PdfFileReader(PATH, "rb")
    output = PyPDF2.PdfFileWriter()
    if (int(pdf.getNumPages())) > 1:
        output.addPage(pdf.getPage(0))
        with open(PATH, 'wb') as f:
            output.write(f)
    # Processes the Conversion
    gsCMD = "".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="',
                     PATH, '.ps" "', PATH, '" "', PATH, '" -c quit'])
    ghostscript(gsCMD)


def postscript_conversion(order):
    F = "".join([order.OD,
                 "/", order.NAME, "/PostScript"])
    try:
        # Creates the Directory for Output
        if not os.path.exists(F):
            os.makedirs(F)
            print("".join(["Successfully created the directory ", F]))
    except OSError:
        print("".join(["Creation of the directory failed ", F]))
    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        gsCMD = "".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', order.OD, '"/"' +
                         order.NAME, '"/PostScript/"', order.FILE_NAMES[i], '.ps" "', order.OD, '"/"', order.NAME, '"/"', order.FILE_NAMES[i], '" -c quit'])
        ghostscript(gsCMD)
    return True


def file_merge(order, DUPLEX_STATE):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(order.FILE_NAMES)):
            try:
                f = open(
                    '/'.join([order.OD, order.NAME, order.FILE_NAMES[i]]), "rb")
                pdf = PyPDF2.PdfFileReader(f)
                pdf = pdf.getNumPages()
                f.close()
            except:
                log.logger.exception("")
                pdf = order.PAGE_COUNTS
            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', order.OD, '/', order.NAME, '/PostScript/', order.FILE_NAMES[i], '.ps"'])
                src = "".join(['"', order.OD, '/',
                               order.NAME, '/', order.FILE_NAMES[i], '"'])
                gsCMD = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                ghostscript(gsCMD)
    # Merges order.FILE_NAMES for Uncollated Printing with SlipSheets
    for FILE in order.FILE_NAMES:
        FILES_path = "".join([FILES_path, '"', order.OD,
                              '/', order.NAME, '/PostScript/', FILE, '.ps" '])
    print("These Files are being MERGED!!")
    output = "".join(
        [order.OD, '/', order.NAME, '/', order.NAME, '.ps'])
    gsCMD = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    ghostscript(gsCMD)
    return True


def file_merge_manual(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE, FILES):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            try:
                f = open(
                    "".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', FILES[i]]), "rb")
                pdf = PyPDF2.PdfFileReader(f)
                pdf = pdf.getNumPages()
                f.close()
            except:
                log.logger.exception("")
                pdf = FILES.page_count(
                    '/'.join([OUTPUT_DIRECTORY, ORDER_NAME, FILES[i]]))
            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PostScript/', FILES[i], '.ps"'])
                src = "".join(['"', OUTPUT_DIRECTORY, '/',
                               ORDER_NAME, '/', FILES[i], '"'])
                gsCMD = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                ghostscript(gsCMD)
    # Merges FILES for Uncollated Printing with SlipSheets
    for FILES in FILES:
        FILES_path = "".join([FILES_path, '"', OUTPUT_DIRECTORY,
                              '/', ORDER_NAME, '/PostScript/', FILES, '.ps" '])
    print("These FILES are being MERGED!!")
    output = "".join(
        [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.ps'])
    gsCMD = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    ghostscript(gsCMD)
    return True


def file_merge_n(order, DUPLEX_STATE):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(order.FILE_NAMES)):
            try:
                f = open("".join([order.OD, '/',  order.NAME,
                                  '/PDF/', order.FILE_NAMES[i]]), "rb")
                pdf = PyPDF2.PdfFileReader(f)
                pdf = pdf.getNumPages()
                f.close()
            except:
                log.logger.exception("")
                pdf = order.FILE_NAMES.page_count(
                    '/'.join([order.OD,  order.NAME, "PDF", order.FILE_NAMES[i]]))
            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', order.OD, '/',  order.NAME, '/PostScriptn/', order.FILE_NAMES[i], '.ps"'])
                src = "".join(['"', order.OD, '/',
                               order.NAME, '/PDFn/', order.FILE_NAMES[i], '"'])
                gsCMD = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write  -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                ghostscript(gsCMD)
    # Merges FILES for Uncollated Printing with SlipSheets
    for FILES in order.FILE_NAMES:
        FILES_path = "".join([FILES_path, '"', order.OD,
                              '/',  order.NAME, '/PostScriptn/', FILES, '.ps" '])
    print("These FILES are being MERGED!!")
    output = "".join(
        [order.OD, '/', order.NAME, '/',  order.NAME, 'n.ps'])
    gsCMD = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    ghostscript(gsCMD)
    return True


def pdf_conversion(order):
    F = "".join([order.OD,
                 "/", order.NAME, "/PDF"])
    try:
        # Creates the Directory for Output
        if not os.path.exists(F):
            os.makedirs(F)
            print(
                "".join(["Successfully created the directory ", F]))
    except OSError:
        print("".join(["Creation of the directory failed ", F]))
    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        gsCMD = "".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', order.OD, '/' +
                         order.NAME, '/PDF/', order.FILE_NAMES[i], '" "', order.OD, '/', order.NAME, '/PostScript/', order.FILE_NAMES[i], '.ps" -c quit'])
        ghostscript(gsCMD)
    return True


def nupConversion(inFile, outFile):
    # https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py
    log.logger.debug("2-up input " + inFile)
    pdfImposer.ledgerSimplexTwoUp(inFile, outFile)
    log.logger.debug("writing " + outFile)
    log.logger.debug("done.")


def nup(order):
    F = "".join([order.OD,
                 "/", order.NAME, "/PDFn"])
    try:
        # Creates the Directory for Output
        if not os.path.exists(F):
            os.makedirs(F)
            print("".join(["Successfully created the directory ", F]))
    except OSError:
        print("".join(["Creation of the directory failed ", F]))
    for i in range(len(order.FILE_NAMES)):
        nupConversion("".join([order.OD, '/', order.NAME, '/PDF/', order.FILE_NAMES[i]]), "".join([order.OD, '/' +
                                                                                                   order.NAME, '/PDFn/', order.FILE_NAMES[i]]))
    F = "".join([order.OD,
                 "/", order.NAME, "/PostScriptn"])
    try:
        # Creates the Directory for Output
        if not os.path.exists(F):
            os.makedirs(F)
            print("".join(["Successfully created the directory ", F]))
    except OSError:
        print("".join(["Creation of the directory failed ", F]))
    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        gsCMD = "".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="', order.OD, '"/"' +
                         order.NAME, '"/PostScriptn/"', order.FILE_NAMES[i], '.ps" "', order.OD, '"/"', order.NAME, '"/PDFn/"', order.FILE_NAMES[i], '" -c quit'])
        ghostscript(gsCMD)
