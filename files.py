# files.py
__version__ = "v20200721"
# Built-In Libraries
import os
import glob
# Downloaded Libraries
import PyPDF2
from termcolor import colored
import colorama
import subprocess
import shutil
# Local Files
import log
from PostScript import GHOSTSCRIPT_PATH
# use Colorama to make Termcolor work on Windows too
colorama.init()


def folder_list(folder):
    """
    Grabs the list of folders in the requested directory.

    Parameters: 
        folder    (str): The folder to search
        
    Returns: 
        list: The list of folders.
    """
    fileList = sorted(glob.glob("".join([folder, "/*"])))
    # Strips the file path data to leave just the foldername
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def file_list(order):
    """
    Grabs the list of all pdfs for the requested order.

    Parameters: 
        order   (object): The object containing all the information for the current order.
        
    Returns: 
        list: The list of all pdfs for requested order..
    """
    # Grabs the PDF's in the requested order
    fileList = sorted(
        glob.glob("".join([order.OD, "/", order.NAME, "/*.pdf"])))
    # Strips the file path data to leave just the filename
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def postscript_list(folder, OName, sub):
    """
    Looks for postscript files in a sub folder inside the order.

    The function will either look for the converted postscript files,
    or the Print Ready Postscript files. Depending on which sub folder is passed to it.

    Parameters: 
        folder  :(str) The directory where all orders are located.
        OName   :(str) The Name of the folder that the current order resides in.
        sub     :(str) The sub folder to look inside within the current order.
        
    Returns: 
        list: The list of all postscript files in the requested sub folder for requested order..
    """
    # 
    fileList = sorted(
        glob.glob("".join([folder, "/", OName, "/", sub, "/", "*.ps"])))
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def page_counts(order):
    """
    Generates Page Counts for an Order

    Parameters: 
        order   (object): The object containing all the information for the current order.
        
    Returns: 
        counts      (int) : Total page Count of entire order.
        orderCounts (list): The page count for each file.
    """
    files = file_list(order)
    counts = 0
    orderCounts = []
    for i in range(len(files)):
        try:
            f = open("".join([order.OD, '/', order.NAME, '/', files[i]]), "rb")
            pdf = PyPDF2.PdfFileReader(f)
            pdf = pdf.getNumPages()
            f.close()
        except:
            log.logger.exception("Using Alternative Page Count Generator")
            pdf = page_count(
                '/'.join([order.OD, '/', order.NAME, '/', files[i]]))
        orderCounts.append("".join(["Page Count: ", colored(str(pdf),
                                                            "magenta"), " FileName: ", files[i]]))
        counts = counts + pdf
    return counts, orderCounts


def page_count(path):
    """
    Alternative Method to Calculating Document Page Count

    Uses a differenet method to calculate the page count of a single file.
    This is used if the primary method of calculating page counts fail.

    Parameters: 
        path   (str): Path to the file that needs page counts calculated.
        
    Returns: 
        out (int): The page count
    """
    args = [GHOSTSCRIPT_PATH, "-q", "-dNODISPLAY", '-c',
            '"('+path + ') (r) file runpdfbegin pdfpagecount = quit"']
    if(os.name == "posix"):
        status = subprocess.Popen(args, stdout=subprocess.PIPE)
    else:
        status = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = status.communicate()  # pylint: disable=unused-variable
    out = out.strip()
    out = [int(s) for s in out.split() if s.isdigit()]
    return out[0]


def file_cleanup(Orders, OUTPUT_DIRECTORY):
    """
    Cleans up unnecessary files after the order has successfully finished running.

    Parameters: 
        Orders              (list): The object containing all the information for the current order.
        OUTPUT_DIRECTORY    (str) : The directory where all orders are located.
        
    Returns: 
        bool: unused return
    """
    try:
        for order in Orders:
            orderPath = "".join([OUTPUT_DIRECTORY, "/", order])
            deleteList = ("/PostScript/", "/PSP/", "/Tickets/", "".join(
                [order, ".ps"]), "/PDF/", "/PDFn/", "/PostScriptn/", "PSPn", "".join([order, "n.ps"]))
            for item in deleteList:
                filePath = "".join([orderPath, item])
                if os.path.exists(filePath):
                    shutil.rmtree(filePath)
        Orders = []
        return True
    except:
        log.logger.exception("")
        print("File Cleanup Failed")
        return False
