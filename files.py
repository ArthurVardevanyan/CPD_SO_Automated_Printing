# files.py
__version__ = "v20200122"

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

if(os.name == "posix"):
    GHOSTSCRIPT_PATH = 'gs'
else:
    GHOSTSCRIPT_PATH = 'C:/Program Files (x86)/gs/gs9.27/bin/gswin32c.exe'

# use Colorama to make Termcolor work on Windows too
colorama.init()


def folder_list(folder):
    # Grabs the list of folders
    # Gathers all the Folders
    fileList = sorted(glob.glob("".join([folder, "/*"])))
    # Strips the file path data to leave just the foldername
    Stripped_List = [os.path.basename(x) for x in fileList]
    return Stripped_List  # Returns the Stripped List to Main Function


def file_list(order):
    # Grabs the PDF's in the requested order
    fileList = sorted(glob.glob("".join([order.OD, "/", order.NAME, "/*.pdf"]))
                      )  # Gathers all the Files
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
    print("\n")
    for i in range(len(files)):
        try:
            pdf = PyPDF2.PdfFileReader(
                open("".join([order.OD, '/', order.NAME, '/', files[i]]), "rb"))
            pdf = pdf.getNumPages()
        except:
            log.logger.exception("")
            pdf = page_count(
                '/'.join([order.OD, '/', order.NAME, '/', files[i]]))
        print("Page Count: ", colored(str(pdf),
                                      "magenta"), " FileName: ", files[i])
        counts = counts + pdf
    return counts


def page_count(path):
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
    try:
        for order in Orders:
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PostScript/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PSP/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/Tickets/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join(
                [OUTPUT_DIRECTORY, "/", order, "/", order, ".ps"])
            if os.path.exists(filePath):
                os.remove(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PDF/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PDFn/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PostScriptn/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join([OUTPUT_DIRECTORY, "/", order, "/PSPn/"])
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            filePath = "".join(
                [OUTPUT_DIRECTORY, "/", order, "/", order, "n.ps"])
            if os.path.exists(filePath):
                os.remove(filePath)
        Orders = []
        return True
    except:
        log.logger.exception("")
        print("File Cleanup Failed")
        return False
