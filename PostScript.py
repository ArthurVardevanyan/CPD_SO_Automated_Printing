# PostScript.py
__version__ = "v20200721"
# Built-In Libraries
from PJL_Commands.PJL_PS import blank
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
    # TODO, Remove absolute version number.
    GHOSTSCRIPT_PATH = 'C:/"Program Files"/gs/gs9.53.2/bin/gswin64c.exe'


def ghostscript(gsCMD):
    """
    Processes the requested ghostscript command through the ghostscript program.

    Parameters: 
        gsCMD (str): The Ghostscript command to be processed.

    Returns: 
        bool: Unused output.
    """
    output = subprocess.Popen(gsCMD, stdout=subprocess.PIPE, shell=True)
    (out, err) = output.communicate()  # pylint: disable=unused-variable
    out = str(out).replace("b'GPL Ghostscript 9.27 (2019-04-04)\\nCopyright (C) 2018 Artifex Software, Inc.  All rights reserved.\\nThis software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:\\nsee the file COPYING for details.\\n", "")
    out = out.split("\\n")
    for line in out:
        log.logger.debug(line)
    return 1


def ticket_conversion(PATH):
    """
    Converts the Tickets from PDF TO PS

    Parameters: 
        PATH (str): The Path of the PDF Ticket to be Converted.

    Returns: 
        void: Unused output
    """
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
    """
    Converts order PDF files to PS

    During Email download, pdf files are converted to postscript.

    Parameters: 
        order  (object)   : The object containing all the information for the current order.

    Returns: 
        bool: Unused output
    """
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
    """
    If needed, merges multiple files together

    Some orders get all files merged into one big file.
    If duplex, blank pages are added to the end of all odd number documents.

    Parameters: 
        order           (object): The object containing all the information for the current order.
        DUPLEX_STATE    (str)   : Whether the order is duplex or not.

    Returns: 
        bool: Unused output
    """
    with open('Blank.ps', 'wb') as f:
        f.write(blank)
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
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile=', output, ' ', src, ' Blank.ps -c quit'])
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
