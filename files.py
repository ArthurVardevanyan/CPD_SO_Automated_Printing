import os
import glob


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
