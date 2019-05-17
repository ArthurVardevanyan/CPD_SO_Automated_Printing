import json
import os
import glob
import sys
from files import FolderList
from files import FilesList
import sys
import locale


def Postscript(OrderNumber, folder):
    OName = " " #This is the Order Name taken from the subject line.
    Folders = FolderList(folder) #Calls a function in files.py, which gets a list of all the orders downladed
    for i in Folders: #Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i
    Files = FilesList(folder, OName) #Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    path = os.getcwd()  # Current Path
    try:
        os.makedirs(path + "/" +folder+"/"+OName+ "/PostScript")
        print("Successfully created the directory " +path + "/" +folder+"/"+OName+ "/PostScript")
    except OSError:
        print("Creation of the directory failed " + path + "/" +folder+"/"+OName+ "/PostScript")
    
    #GSP = 'gs'
    GSP = 'C:/"Program Files (x86)"/gs/gs9.27/bin/gswin32c.exe'


    for i in range(len(Files)): #This gets the number of pages for every pdf file for the job.
       os.system(GSP + ' -dNOPAUSE -dBATCH -sDEVICE=ps2write -sOutputFile="'+folder+'"/"'+OName+'"/PostScript/"'+Files[i]+'.ps" "'+folder+'"/"'+OName+'"/"'+Files[i]+'" -c quit')
        



#Postscript("8985 TEACHER NAME - flood recovery", "School_Orders")
