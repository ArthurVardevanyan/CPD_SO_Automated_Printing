import os
import glob


def FolderList(folder):
    # Grabs the Files (Contains the Date Modifer metedata as well)

    fileList = glob.glob(folder+"/*")  # Gathers all the Files
    # fileList.sort(key=os.path.getmtime)  # Sorts Oldset to Newest
    # Strips the file path data to leave just the filename
    # Strip filepath to filename.
    Stripped_List = [os.path.basename(x) for x in fileList]

    return Stripped_List  # Returns the Stripped List to Main Function


def FilesList(folder, OName):
    # Grabs the Files (Contains the Date Modifer metedata as well)

    fileList = glob.glob(folder+"/"+OName+"/*.pdf")  # Gathers all the Files
    # fileList.sort(key=os.path.getmtime)  # Sorts Oldset to Newest
    # Strips the file path data to leave just the filename
    # Strip filepath to filename.
    Stripped_List = [os.path.basename(x) for x in fileList]

    return Stripped_List  # Returns the Stripped List to Main Function


def PostList(folder, OName, sub):
    # Grabs the Files (Contains the Date Modifer metedata as well)

    fileList = glob.glob(folder+"/"+OName+"/"+sub+"/"+"*.ps")  # Gathers all the Files
    # fileList.sort(key=os.path.getmtime)  # Sorts Oldset to Newest
    # Strips the file path data to leave just the filename
    # Strip filepath to filename.
    Stripped_List = [os.path.basename(x) for x in fileList]

    return Stripped_List  # Returns the Stripped List to Main Function

