# PostScript.py
__version__ = "v20190928"

# Built-In Libraries
import json
import os
import glob
import sys
import locale

# Downloaded Libraries
import PyPDF2

# Local Files
import files

GHOSTSCRIPT_PATH = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'


def ticket_conversion(PATH):
    # Processes the Conversion
    os.system(GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="' +
              PATH+'.ps" "'+PATH+'" -c quit')


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
        os.makedirs(OUTPUT_DIRECTORY +
                    "/"+ORDER_NAME + "/PostScript")
        print("Successfully created the directory " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PostScript")
    except OSError:
        print("Creation of the directory failed " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PostScript")

    for i in range(len(FILES)):
        # Processes the Conversion
        os.system(GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="'+OUTPUT_DIRECTORY+'"/"' +
                  ORDER_NAME+'"/PostScript/"'+FILES[i]+'.ps" "'+OUTPUT_DIRECTORY+'"/"'+ORDER_NAME+'"/"'+FILES[i]+'" -c quit')


def file_merge(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE):
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    files_path = ''
    if DUPLEX_STATE == True:  # Adds blanks for doublesided uncollated printing
        for i in range(len(FILES)):
            pdf = PyPDF2.PdfFileReader(
                open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+FILES[i], "rb"))
            if (int(pdf.getNumPages()) % 2) != 0:  # If odd number pages, add blank page
                print("Adding Blank Page!")
                output = '"' + OUTPUT_DIRECTORY+'/'+ORDER_NAME + \
                    '/PostScript/'+FILES[i] + '.ps"'
                src = '"' + OUTPUT_DIRECTORY+'/' + \
                    ORDER_NAME + '/'+FILES[i] + '"'
                ghostscript_command = GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile=' + \
                    output+' '+src + ' PJL_Commands/Blank.ps -c quit'
                os.system(ghostscript_command)

    # Merges Files for Uncollated Printing with SlipSheets
    for FILES in FILES:
        files_path = files_path + '"' + OUTPUT_DIRECTORY + \
            '/'+ORDER_NAME + '/PostScript/'+FILES + '.ps" '
    print("These Files are being MERGED!!")
    output = OUTPUT_DIRECTORY+'/'+ORDER_NAME + '/'+ORDER_NAME + '.ps'
    ghostscript_command = GHOSTSCRIPT_PATH + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="' + \
        output+'" ' + files_path + '  -c quit'
    # Processes the Conversion
    os.system(ghostscript_command)
    return True
