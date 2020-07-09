# files.py
__version__ = "v20200709"
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
    # Grabs the list of folders
    fileList = sorted(glob.glob("".join([folder, "/*"])))
    # Strips the file path data to leave just the foldername
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def file_list(order):
    # Grabs the PDF's in the requested order
    fileList = sorted(
        glob.glob("".join([order.OD, "/", order.NAME, "/*.pdf"])))
    # Strips the file path data to leave just the filename
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def postscript_list(folder, OName, sub):
    # Add's Sub Folder to look for Postscript Files
    fileList = sorted(
        glob.glob("".join([folder, "/", OName, "/", sub, "/", "*.ps"])))
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def page_counts(order):
    # Returns the total page counts for an Order
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
            log.logger.exception("Using Alternative Page Count Source")
            pdf = page_count(
                '/'.join([order.OD, '/', order.NAME, '/', files[i]]))
        orderCounts.append("".join(["Page Count: ", colored(str(pdf),
                                                            "magenta"), " FileName: ", files[i]]))
        counts = counts + pdf
    return counts, orderCounts


def page_count(path):
    # Alternative Method to Calculating Document Page Count
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
    # Cleans up Temporary Files after order finishes.
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
