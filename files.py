import os
import glob
from PyPDF2 import PdfFileReader


def folder_list(folder):
    # Grabs the list of folders
    fileList = glob.glob(folder+"/*")  # Gathers all the Folders
    # Strips the file path data to leave just the foldername
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def file_list(folder, OName):
    # Grabs the PDF's in the requested order
    fileList = glob.glob(folder+"/"+OName+"/*.pdf")  # Gathers all the Files
    # Strips the file path data to leave just the filename
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def postscript_list(folder, OName, sub):
    # Addes Sub Folder to look for Postscript Files
    fileList = glob.glob(folder+"/"+OName+"/"+sub+"/" + "*.ps")
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function

def page_counts(OUTPUT_DIRECTORY, ORDER_NAME):
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)
    page_count = 0
    for i in range(len(files)):
        pdf = PdfFileReader(
            open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+files[i], "rb"))
        page_count = page_count + pdf.getNumPages()
    return page_count