# PostScript.py
__version__ = "v20200109"

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

# Local Files
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


def postscript_conversion(ORDER_NUMBER, OUTPUT_DIRECTORY):
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = files.folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
            ORDER_NAME = i
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    try:
        # Creates the Directory for Output
        os.makedirs("".join([OUTPUT_DIRECTORY,
                             "/", ORDER_NAME, "/PostScript"]))
        print("Successfully created the directory ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PostScript")
    except OSError:
        print("Creation of the directory failed ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PostScript")

    for i in range(len(FILES)):
        # Processes the Conversion
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', OUTPUT_DIRECTORY, '"/"' +
                           ORDER_NAME, '"/PostScript/"', FILES[i], '.ps" "', OUTPUT_DIRECTORY, '"/"', ORDER_NAME, '"/"', FILES[i], '" -c quit']))
    return True


def file_merge(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE):
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    files_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', FILES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = files.page_count(
                    '/'.join([OUTPUT_DIRECTORY, ORDER_NAME, FILES[i]]))

            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PostScript/', FILES[i], '.ps"'])
                src = "".join(['"', OUTPUT_DIRECTORY, '/',
                               ORDER_NAME, '/', FILES[i], '"'])
                ghostscript_command = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage   -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                os.system(ghostscript_command)

    # Merges Files for Uncollated Printing with SlipSheets
    for FILES in FILES:
        files_path = "".join([files_path, '"', OUTPUT_DIRECTORY,
                              '/', ORDER_NAME, '/PostScript/', FILES, '.ps" '])
    print("These Files are being MERGED!!")
    output = "".join(
        [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write  -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', files_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def file_merge_manual(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE, FILES):
    files_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', FILES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = files.page_count(
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

    # Merges Files for Uncollated Printing with SlipSheets
    for FILES in FILES:
        files_path = "".join([files_path, '"', OUTPUT_DIRECTORY,
                              '/', ORDER_NAME, '/PostScript/', FILES, '.ps" '])
    print("These Files are being MERGED!!")
    output = "".join(
        [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage  -sOutputFile="', output, '" ', files_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def file_merge_n(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE):
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    files_path = ''
    if DUPLEX_STATE == 2:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            try:
                pdf = PyPDF2.PdfFileReader(
                    open("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PDF/', FILES[i]]), "rb"))
                pdf = pdf.getNumPages()
            except:
                pdf = files.page_count(
                    '/'.join([OUTPUT_DIRECTORY, ORDER_NAME, "PDF", FILES[i]]))

            if (int(pdf) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = "".join(
                    ['"', OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PostScriptn/', FILES[i], '.ps"'])
                src = "".join(['"', OUTPUT_DIRECTORY, '/',
                               ORDER_NAME, '/PDFn/', FILES[i], '"'])
                ghostscript_command = "".join(
                    [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write  -sOutputFile=', output, ' ', src, ' PJL_Commands/Blank.ps -c quit'])
                os.system(ghostscript_command)

    # Merges Files for Uncollated Printing with SlipSheets
    for FILES in FILES:
        files_path = "".join([files_path, '"', OUTPUT_DIRECTORY,
                              '/', ORDER_NAME, '/PostScriptn/', FILES, '.ps" '])
    print("These Files are being MERGED!!")
    output = "".join(
        [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, 'n.ps'])
    ghostscript_command = "".join(
        [GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write   -sOutputFile="', output, '" ', files_path, '  -c quit'])
    # Processes the Conversion
    os.system(ghostscript_command)
    return True


def pdf_conversion(ORDER_NUMBER, OUTPUT_DIRECTORY):
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = files.folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
            ORDER_NAME = i
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    try:
        # Creates the Directory for Output
        os.makedirs("".join([OUTPUT_DIRECTORY,
                             "/", ORDER_NAME, "/PDF"]))
        print("Successfully created the directory ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PDF")
    except OSError:
        print("Creation of the directory failed ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PDF")

    for i in range(len(FILES)):
        # Processes the Conversion
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="', OUTPUT_DIRECTORY, '"/"' +
                           ORDER_NAME, '"/PDF/"', FILES[i], '" "', OUTPUT_DIRECTORY, '"/"', ORDER_NAME, '"/PostScript/"', FILES[i], '".ps -c quit']))
    return True


def nupConversion(inFile, outFile):
    # https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py
    print("2-up input " + inFile)
    input1 = PdfFileReader(open(inFile, "rb"))
    output = PdfFileWriter()
    output1 = PdfFileWriter()

    for iter in range(0, input1.getNumPages()):
        lhs = input1.getPage(iter)
        rhs = input1.getPage(iter)
        lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
        output.addPage(lhs)
        print(str(iter) + " "),
        sys.stdout.flush()
    for iter in range(0, output.getNumPages()):
        page = output.getPage(iter)
        page.rotateClockwise(90)
        output1.addPage(page)
        sys.stdout.flush()

    print("writing " + outFile)
    outputStream = open(outFile, "wb")
    output1.write(outputStream)
    print("done.")


def nup(OUTPUT_DIRECTORY, ORDER_NUMBER):
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = files.folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
            ORDER_NAME = i
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    try:
        # Creates the Directory for Output
        os.makedirs("".join([OUTPUT_DIRECTORY,
                             "/", ORDER_NAME, "/PDFn"]))
        print("Successfully created the directory ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PDFn")
    except OSError:
        print("Creation of the directory failed ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PDFn")

    for i in range(len(FILES)):
        nupConversion("".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/PDF/', FILES[i]]), "".join([OUTPUT_DIRECTORY, '/' +
                                                                                                ORDER_NAME, '/PDFn/', FILES[i]]))

    try:
        # Creates the Directory for Output
        os.makedirs("".join([OUTPUT_DIRECTORY,
                             "/", ORDER_NAME, "/PostScriptn"]))
        print("Successfully created the directory ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PostScriptn")
    except OSError:
        print("Creation of the directory failed ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PostScriptn")

    for i in range(len(FILES)):
        # Processes the Conversion
        os.system("".join([GHOSTSCRIPT_PATH, ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="', OUTPUT_DIRECTORY, '"/"' +
                           ORDER_NAME, '"/PostScriptn/"', FILES[i], '.ps" "', OUTPUT_DIRECTORY, '"/"', ORDER_NAME, '"/PDFn/"', FILES[i], '" -c quit']))
