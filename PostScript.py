# PostScript.py
__version__ = "v20200121"

# Built-In Libraries
import json
import os
import glob
import sys
import locale
import subprocess

# Downloaded Libraries
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject

# Local order.FILE_NAMES
import files

if(os.name == "posix"):
    GHOSTSCRIPT_PATH = 'gs'
else:
    GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'

# Grayscale Ghostscript Parameter
# https://gist.github.com/firstdoit/6390547


def ticket_conversion(PATH):
    # https://stackoverflow.com/questions/39574096/how-to-delete-pages-from-pdf-file-using-python
    pdf = PyPDF2.PdfFileReader(PATH, "rb")
    output = PyPDF2.PdfFileWriter()

    if (int(pdf.getNumPages())) > 1:
        output.addPage(pdf.getPage(0))
        with open(PATH, 'wb') as f:
            output.write(f)
    # Processes the Conversion
    os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="',
                       PATH, '.ps" "', PATH, '" "', PATH, '" -c quit']))


def postscript_conversion(order):

    try:
        # Creates the Directory for Output
        os.makedirs("".join([order.OD,
                             "/", order.NAME, "/PostScript"]))
        print("Successfully created the directory ",
              "/", order.OD, "/", order.NAME, "/PostScript")
    except OSError:
        print("Creation of the directory failed ",
              "/", order.OD, "/", order.NAME, "/PostScript")

    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', order.OD, '"/"' +
                           order.NAME, '"/PostScript/"', order.FILE_NAMES[i], '.ps" "', order.OD, '"/"', order.NAME, '"/"', order.FILE_NAMES[i], '" -c quit']))
    return True


def file_merge(order, DUPLEX_STATE):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(order.FILE_NAMES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', order.FILE_NAMES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = order.PAGE_COUNTS

            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', order.OD, '/', order.NAME, '/PostScript/', order.FILE_NAMES[i], '.ps"'])
                src = "".join(['"', order.OD, '/',
                               order.NAME, '/', order.FILE_NAMES[i], '"'])
                ghostscript_command = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage   -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                os.system(ghostscript_command)

    # Merges order.FILE_NAMES for Uncollated Printing with SlipSheets
    for FILE in order.FILE_NAMES:
        FILES_path = "".join([FILES_path, '"', order.OD,
                              '/', order.NAME, '/PostScript/', FILE, '.ps" '])
    print("These Files are being MERGED!!")
    output = "".join(
        [order.OD, '/', order.NAME, '/', order.NAME, '.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write  -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def file_merge_manual(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE, FILES):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', FILES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = FILES.page_count(
                    '/'.join([OUTPUT_DIRECTORY, ORDER_NAME, FILES[i]]))

            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PostScript/', FILES[i], '.ps"'])
                src = "".join(['"', OUTPUT_DIRECTORY, '/',
                               ORDER_NAME, '/', FILES[i], '"'])
                ghostscript_command = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                os.system(ghostscript_command)

    # Merges FILES for Uncollated Printing with SlipSheets
    for FILES in FILES:
        FILES_path = "".join([FILES_path, '"', OUTPUT_DIRECTORY,
                              '/', ORDER_NAME, '/PostScript/', FILES, '.ps" '])
    print("These FILES are being MERGED!!")
    output = "".join(
        [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def file_merge_n(order, DUPLEX_STATE):
    FILES_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(order.FILE_NAMES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([order.OD, '/',  order.NAME, '/PDF/', order.FILE_NAMES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = order.FILE_NAMES.page_count(
                    '/'.join([order.OD,  order.NAME, "PDF", order.FILE_NAMES[i]]))

            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', order.OD, '/',  order.NAME, '/PostScriptn/', order.FILE_NAMES[i], '.ps"'])
                src = "".join(['"', order.OD, '/',
                               order.NAME, '/PDFn/', order.FILE_NAMES[i], '"'])
                ghostscript_command = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write  -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                os.system(ghostscript_command)

    # Merges FILES for Uncollated Printing with SlipSheets
    for FILES in order.FILE_NAMES:
        FILES_path = "".join([FILES_path, '"', order.OD,
                              '/',  order.NAME, '/PostScriptn/', FILES, '.ps" '])
    print("These FILES are being MERGED!!")
    output = "".join(
        [order.OD, '/', order.NAME, '/',  order.NAME, 'n.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sOutputFile="', output, '" ', FILES_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def pdf_conversion(order):

    try:
        # Creates the Directory for Output
        os.makedirs("".join([order.OD,
                             "/", order.NAME, "/PDF"]))
        print("Successfully created the directory ",
              "/", order.OD, "/", order.NAME, "/PDF")
    except OSError:
        print("Creation of the directory failed ",
              "/", order.OD, "/", order.NAME, "/PDF")

    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        ghostscript_command = "".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', order.OD, '/' +
                                       order.NAME, '/PDF/', order.FILE_NAMES[i], '" "', order.OD, '/', order.NAME, '/PostScript/', order.FILE_NAMES[i], '.ps" -c quit'])
        os.system(ghostscript_command)
    return True


def nupConversion(inFile, outFile):
    # https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py
    print("2-up input " + inFile)
    input1 = PdfFileReader(open(inFile, "rb"))
    output = PdfFileWriter()
    output1 = PdfFileWriter()
    scaled = PdfFileWriter()

    for iter in range(0, input1.getNumPages()):
        page = input1.getPage(iter)
        doc = PageObject.createBlankPage(
            page, page.mediaBox.getWidth(),  page.mediaBox.getHeight())
        leftmargin = (page.mediaBox.getWidth() * .03 / 2)
        bottommargin = (page.mediaBox.getHeight() * .03 / 2)
        doc.mergeScaledTranslatedPage(page, .97, leftmargin, bottommargin)
        sys.stdout.flush()
        scaled.addPage(doc)
    for iter in range(0, scaled.getNumPages()):
        page = scaled.getPage(iter)
        orientation = scaled.getPage(iter).mediaBox
        if orientation.getUpperRight_x() - orientation.getUpperLeft_x() < orientation.getUpperRight_y() - orientation.getLowerRight_y():
            # https://stackoverflow.com/a/46017058
            page.rotateClockwise(90)
        output.addPage(page)
        sys.stdout.flush()
    for iter in range(0, output.getNumPages()):
        lhs = output.getPage(iter)
        rhs = output.getPage(iter)
        lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
        output1.addPage(lhs)
        print(str(iter) + " "),
        sys.stdout.flush()

    print("writing " + outFile)
    outputStream = open(outFile, "wb")
    output1.write(outputStream)
    print("done.")


def nup(order):

    try:
        # Creates the Directory for Output
        os.makedirs("".join([order.OD,
                             "/", order.NAME, "/PDFn"]))
        print("Successfully created the directory ",
              "/", order.OD, "/", order.NAME, "/PDFn")
    except OSError:
        print("Creation of the directory failed ",
              "/", order.OD, "/", order.NAME, "/PDFn")

    for i in range(len(order.FILE_NAMES)):
        nupConversion("".join([order.OD, '/', order.NAME, '/PDF/', order.FILE_NAMES[i]]), "".join([order.OD, '/' +
                                                                                                   order.NAME, '/PDFn/', order.FILE_NAMES[i]]))

    try:
        # Creates the Directory for Output
        os.makedirs("".join([order.OD,
                             "/", order.NAME, "/PostScriptn"]))
        print("Successfully created the directory ",
              "/", order.OD, "/", order.NAME, "/PostScriptn")
    except OSError:
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="', order.OD, '"/"' +
                           order.NAME, '"/PostScriptn/"', order.FILE_NAMES[i], '.ps" "', order.OD, '"/"', order.NAME, '"/PDFn/"', order.FILE_NAMES[i], '" -c quit']))

    for i in range(len(order.FILE_NAMES)):
        # Processes the Conversion
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="', order.OD, '"/"' +
                           order.NAME, '"/PostScriptn/"', order.FILE_NAMES[i], '.ps" "', order.OD, '"/"', order.NAME, '"/PDFn/"', order.FILE_NAMES[i], '" -c quit']))
