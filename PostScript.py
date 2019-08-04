# PostScript.py
__version__ = "v20190726"

# Built-In Libraries
import json
import os
import glob
import sys
import locale

# Downloaded Libraries
from PyPDF2 import PdfFileReader

# Local Files
from files import folder_list
from files import file_list


def ticket_conversion(PATH):
    # Windows
    GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'
    #GHOSTSCRIPT_PATH = 'gs' #Linux
    # This gets the number of pages for every pdf file for the job.
    os.system(GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="' +
              PATH+'.ps" "'+PATH+'" -c quit')


def postscript_conversion(ORDER_NUMBER, OUTPUT_DIRECTORY):
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
            ORDER_NAME = i
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    try:
        os.makedirs(OUTPUT_DIRECTORY +
                    "/"+ORDER_NAME + "/PostScript")
        print("Successfully created the directory " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PostScript")
    except OSError:
        print("Creation of the directory failed " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PostScript")

    # Windows
    GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'
    # GHOSTSCRIPT_PATH = 'gs' #Linux
    # This gets the number of pages for every pdf file for the job.
    for i in range(len(files)):
        os.system(GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="'+OUTPUT_DIRECTORY+'"/"' +
                  ORDER_NAME+'"/PostScript/"'+files[i]+'.ps" "'+OUTPUT_DIRECTORY+'"/"'+ORDER_NAME+'"/"'+files[i]+'" -c quit')


def file_merge(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE):
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    # Windows
    GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'
    # GHOSTSCRIPT_PATH = 'gs' #Linux
    files_path = ''
    if DUPLEX_STATE == True:  # Adds blanks for doublesided uncollated printing
        for i in range(len(files)):
            pdf = PdfFileReader(
                open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+files[i], "rb"))
            if (int(pdf.getNumPages()) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = '"' + OUTPUT_DIRECTORY+'/'+ORDER_NAME + \
                    '/PostScript/'+files[i] + '.ps"'
                src = '"' + OUTPUT_DIRECTORY+'/' + \
                    ORDER_NAME + '/'+files[i] + '"'
                ghostscript_command = GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile=' + \
                    output+' '+src + ' PJL_Commands/Blank.ps -c quit'
                os.system(ghostscript_command)

    # Merges Files for Uncollated Printing with SlipSheets
    for files in files:
        files_path = files_path + '"' + OUTPUT_DIRECTORY + \
            '/'+ORDER_NAME + '/PostScript/'+files + '.ps" '
    print("These Files are being MERGED!!")
    output = OUTPUT_DIRECTORY+'/'+ORDER_NAME + '/'+ORDER_NAME + '.ps'
    ghostscript_command = GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="' + \
        output+'" ' + files_path + '  -c quit'
    os.system(ghostscript_command)
    return True
