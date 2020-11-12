__version__ = "v20200709"
import colorama
from termcolor import colored
import termcolor
import os
# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
from shutil import which
from urllib.request import urlopen
import log
print = log.Print
input = log.Input


def lpr():
    # Check if LPR for Line printer Daemon (LPD) is enabled on the System
    if(os.name == "posix"):
        LPR_PATH = 'lpr'
        output = which(LPR_PATH) is not None
    else:
        LPR_PATH = 'C:/Windows/System32/lpr.exe'
        output = os.path.exists(LPR_PATH)
    if(not output):
        print(colored("lpr Integrity Check Failed", "yellow"))
    return output


def lpq():
    # Check if LPQ for Line printer Daemon (LPD) is enabled on the System
    if(os.name == "posix"):
        LPQ_PATH = 'lpq'
        output = which(LPQ_PATH) is not None
    else:
        LPQ_PATH = 'C:/Windows/System32/lpq.exe'
        output = os.path.exists(LPQ_PATH)
    if(not output):
        print(colored("lpq Integrity Check Failed", "yellow"))
    return output


def ghostscript():
    # Check if Ghostscript is Installed
    if(os.name == "posix"):
        GHOSTSCRIPT_PATH = 'gs'
        output = which(GHOSTSCRIPT_PATH) is not None
    else:
        GHOSTSCRIPT_VERSION = os. listdir('C:/Program Files/gs/')[-1]
        GHOSTSCRIPT_PATH = 'C:/Program Files/gs/'+GHOSTSCRIPT_VERSION+'/bin/gswin64c.exe'
        output = os.path.exists(GHOSTSCRIPT_PATH)
    if(not output):
        print(colored("Ghostscript Integrity Check Failed", "yellow"))
    return output


def wkhtmltopdf():
    # Check if wkhtmltopdf is Installed
    if(os.name == "posix"):
        WKHTMLTOPDF_PATH = 'gs'
        output = which(WKHTMLTOPDF_PATH) is not None
    else:
        WKHTMLTOPDF_PATH = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        output = os.path.exists(WKHTMLTOPDF_PATH)
    if(not output):
        print(colored("wkhtmltopdf Integrity Check Failed", "yellow"))
    return output


def ansicon():
    # Check if ansicon (Terminal Color) is Installed
    if(os.name == "posix"):
        output = True  # Not Relevant for Linux
    else:
        ANSICON_PATH = 'C:/ansi189-bin/x64/ansicon.exe'
        output = os.path.exists(ANSICON_PATH)
    if(not output):
        print(colored("ansicon Integrity Check Failed", "yellow"))
    return output


def internet():
    #Check if Valid Internet Connection
    # https://stackoverflow.com/questions/50558000/test-internet-connection-for-python3
    try:
        urlopen('https://8.8.8.8', timeout=10)
        return True
    except:
        print(colored("Internet Connection could not be Established", "yellow"))
        return False


def integrity():
    integrityChecks = []
    integrityChecks.append(lpr())
    integrityChecks.append(lpq())
    integrityChecks.append(ghostscript())
    integrityChecks.append(wkhtmltopdf())
    #integrityChecks.append(internet()) #TODO Sometimes Failing on Windows
    if(False in integrityChecks):
        print(colored(
            "Please resolve the above the error\nThe Software will now Exit", "red"))
        input("Press Any Key to Exit")
        exit()
    else:
        return True


def main():
    log.logInit("Integrity")
    from log import logger
    print = log.Print  # pylint: disable=unused-variable
    input = log.Input  # pylint: disable=unused-variable
    integrity()


if __name__ == "__main__":
    main()
