import json
import os
import glob
import sys
from files import FolderList
from files import FilesList
import sys
import locale


def Postscript(OrderNumber, folder):
    OName = " "  # This is the Order Name taken from the subject line.
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = FolderList(folder)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i
    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    Files = FilesList(folder, OName)
    path = os.getcwd()  # Current Path
    try:
        os.makedirs(path + "/" + folder+"/"+OName + "/PostScript")
        print("Successfully created the directory " +
              path + "/" + folder+"/"+OName + "/PostScript")
    except OSError:
        print("Creation of the directory failed " +
              path + "/" + folder+"/"+OName + "/PostScript")

    #GSP = 'gs'
    GSP = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'

    # This gets the number of pages for every pdf file for the job.
    for i in range(len(Files)):
        os.system(GSP + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sPAPERSIZE=letter -dFIXEDMEDIA  -dPDFFitPage -sOutputFile="'+folder+'"/"' +
                  OName+'"/PostScript/"'+Files[i]+'.ps" "'+folder+'"/"'+OName+'"/"'+Files[i]+'" -c quit')


#Postscript("8985 TEACHER NAME - flood recovery", "School_Orders")
