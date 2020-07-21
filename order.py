__version__ = "v20200721"
import colorama
from termcolor import colored
import termcolor
import files
import json
import SchoolDataJson
import os
import log
import GDrive
import EmailPrint
import instructions
import PostScript
print = log.Print
input = log.Input


class Files:
    # Contains the list of files and how many pages each file is.
    NAME = ""
    PAGE_COUNT = ""


class Order:
    # Contains all the details regarding the order.
    OD = ""
    UID = ""
    status = ""
    RESULT = ""
    NAME = ""
    NUMBER = ""
    SUBJECT = ""
    COPIES = 0
    DUPLEX = ""
    COLLATION = ""
    STAPLING = ""
    STAPLING_BOOL = False
    DRILLING = ""
    FOLDING = ""
    CUTTING = ""
    BOOKLET = ""
    FRONT_COVER = ""
    BACK_COVER = ""
    SLIPSHEETS = ""
    SPECIAL_INSTRUCTIONS = ""
    PAPER = ""
    PAPER_SIZE = ""
    PAPER_COLOR = ""
    PAPER_WEIGHT = ""
    DATE = ""
    FIRST_NAME = ""
    LAST_NAME = ""
    EMAIL = ""
    PHONE = ""
    BILL_TO = ""
    DELIVER_TO_NAME = ""
    DELIVER_TO_ADDRESS = ""
    PAGE_COUNTS = ""
    PAGE_COUNTS_LIST = ""
    FILE_NAMES = []

    def __init__(self):
        self.FILES = []
    COST = 0


def order_initialization(order, JOB_INFO):
    """
    This initializes the order from the local json file into a runtime object.

    Parameters: 
        order  (object)   : The object containing all the information for the current order.
        json   (json/dict): The json/dict containing all the information for the current order.

    Returns: 
        object: The object containing all the information for the current order.
    """
    order.UID = JOB_INFO.get('Email_ID', False)
    order.status = JOB_INFO.get('Status', False)
    order.NUMBER = JOB_INFO.get('Order Number', False)
    order.SUBJECT = JOB_INFO.get('Order Subject', False)
    order.COPIES = int(JOB_INFO.get('Copies', False))
    order.DUPLEX = JOB_INFO.get('Duplex', False)
    order.COLLATION = JOB_INFO.get('Collation', False)
    order.STAPLING = JOB_INFO.get('Stapling', False)
    order.DRILLING = JOB_INFO.get('Drilling', False)
    order.FOLDING = JOB_INFO.get('Folding', False)
    order.CUTTING = JOB_INFO.get('Cutting', False)
    order.BOOKLET = JOB_INFO.get('Booklets', False)
    order.FRONT_COVER = JOB_INFO.get('Front Cover', False)
    order.BACK_COVER = JOB_INFO.get('Back Cover', False)
    order.SLIPSHEETS = JOB_INFO.get('Slip Sheets / Shrink Wrap', False)
    order.SPECIAL_INSTRUCTIONS = JOB_INFO.get('Special Instructions', False)
    order.PAPER = JOB_INFO.get('Paper', False)
    order.DATE = JOB_INFO.get('Date Ordered', False)
    order.FIRST_NAME = JOB_INFO.get('First Name', False)
    order.LAST_NAME = JOB_INFO.get('Last Name', False)
    order.EMAIL = JOB_INFO.get('Email', False)
    order.PHONE = JOB_INFO.get('Phone Number', False)
    order.DELIVER_TO_NAME = JOB_INFO.get('Deliver To Name', False)
    order.DELIVER_TO_ADDRESS = JOB_INFO.get('Deliver To Address', False)
    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    for FILE in JOB_INFO_FILES:
        FILE_INFO = JOB_INFO_FILES.get(str(FILE), 0)
        F = Files()
        F.NAME = str(FILE_INFO.get('File Name', 0))
        F.PAGE_COUNT = int(FILE_INFO.get('Page Count', 0))
        order.FILES.append(F)
    order.FILE_NAMES = [i.NAME for i in order.FILES]
    order.PAGE_COUNTS, order.PAGE_COUNTS_LIST = files.page_counts(order)
    if(any(s in str(order.STAPLING) for s in ("Upper Left - portrait",  "Upper Left - landscape",  "Double Left - portrait",  "None"))):
        order.STAPLING_BOOL = True
    return order


def process_Email(order, email_body, error_state=""):
    """
    The handles all the functions that process the email during download.

    Parameters: 
        order       (object): Empty Order Object
        email_body  (str)   : The body of the email for the current order.
        error_state (str)   : The flag that determines where to store the order.

    Returns: 
        object: The object containing all the information for the current order.
    """
    try:
        # Downloads Files
        GDrive.Drive_Downloader(str(email_body), order.NUMBER,
                                order.OD, order.SUBJECT, error_state)
    except:
        log.logger.exception("")
        print("Drive Download Failed")
        return
    try:
        # Create JSON file with Job Requirements
        JOB_INFO = SchoolDataJson.school_data_json(order)
        # Creates the Object from the Dictionary/JSON
        order = order_initialization(order, JOB_INFO)
    except:
        log.logger.exception("")
        print("JSON File Failed")
    if(error_state == "Error/"):
        order.OD = order.OD + "/Error/"
    try:
        # Create PostScript File(s)
        PostScript.postscript_conversion(order)
    except:
        log.logger.exception("")
        print("PostScript Conversion Failed")
    try:
        # Merge Uncollated Files
        if(instructions.merging(order)):
            PostScript.file_merge(order, instructions.duplex_state(order))
    except:
        log.logger.exception("")
        print("File Merge Failure")
    try:
        # Create Email Html Pdf & PS
        EmailPrint.Email_Printer(order.OD, order.NAME, error_state)
    except:
        log.logger.exception("")
        print("Ticket Conversion Failed")
    return order


def notStarted():
    """
    Checks for orders that have not been started yet.

    Main purpose is to print all unprinted tickets.

    Parameters: 
        N/A

    Returns: 
        list: The orders that have not yet been printed, or had thier tickets printed.
    """
    import sys
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    OD = "SO/"
    folders = files.folder_list(OD)
    orders = []
    for i in range(len(folders)):
        if ("Error" in folders[i] or "Archive" in folders[i]):
            folders.pop(i)
    for folder in folders:
        order = Order()
        order.OD = OD
        order.NAME = folder
        order.NUMBER = folder.split(" ", 1)[0]
        order.SUBJECT = folder.split(" ", 1)[1]
        # Create JSON file with Job Requirements
        JSON_PATH = "".join(
            [order.OD, '/', order.NAME, '/', order.NAME, '.json'])
        if (os.path.exists(JSON_PATH)):
            with open(JSON_PATH) as json_file:
                JOB_INFO = json.load(json_file)
        else:
            JOB_INFO = SchoolDataJson.school_data_json(order)
        order.status = JOB_INFO.get("Status", "")
        #order = order_initialization(order, JOB_INFO)
        if(order.status == "NotStarted"):
            orders.append(order.NAME)
    return orders


def integrityCheckCheck(OUTPUT_DIRECTORY, folders):
    """
    Checks to make sure cirtical files for orders exist.

    Main purpose is to print all unprinted tickets.

    Parameters: 
        OUTPUT_DIRECTORY (str)  : The location of the orders.
        folders          (list) : List of all the orders currently downloaded.

    Returns: 
        list: The orders that have issues.
    """
    orders = []
    for folder in folders:
        filePath = "".join(
            [OUTPUT_DIRECTORY, "/", folder, "/",  folder, ".json"])
        if(not os.path.exists(filePath)):
            orders.append(folder)
    return orders


def integrityCheck(OUTPUT_DIRECTORY):
    """
    Checks to make sure cirtical files for orders exist.

    Attempts to "recover" orders with issues.

    Parameters: 
        OUTPUT_DIRECTORY (str)  : The location of the orders.

    Returns: 
        void: Unused Return.
    """

    folders = files.folder_list(OUTPUT_DIRECTORY)
    for i in range(len(folders)):
        if ("Error" in folders[i] or "Archive" in folders[i]):
            folders.pop(i)
    orders = integrityCheckCheck(OUTPUT_DIRECTORY, folders)
    if(len(orders) > 0):
        print(colored("The Following Orders Failed Their Integrity Check:", "yellow"))
        for o in orders:
            print(o)
        while True:
            try:
                fix = int(
                    input(''.join(["Attempt Fix: (", colored("1", "cyan"), "), Ignore (", colored("0", "cyan"), "): "])))
                if fix == 1 or fix == 0:
                    if fix == 0:
                        return
                    break
                else:
                    pass
            except:
                log.logger.exception("")
                pass
        for folder in folders:
            order = Order()
            order.OD = OUTPUT_DIRECTORY
            filePath = "".join(
                [OUTPUT_DIRECTORY, "/", folder, "/",  folder, ".json"])
            if(not os.path.exists(filePath)):
                files.file_cleanup([folder], OUTPUT_DIRECTORY)
                order.NAME = folder
                folder = folder.split(" ", 1)
                order.NUMBER, order.SUBJECT = folder
                with open("".join([order.OD, '/', order.NAME, '/', order.NAME, ".txt"]), "r") as f:
                    email_body = f.read()
                process_Email(order, email_body)
        orders = integrityCheckCheck(OUTPUT_DIRECTORY, folders)
        if(len(orders) > 0):
            print(colored(
                "Please make note of the following orders below that failed thier recovery attempt:", "red"))
            for o in orders:
                print(o)
        else:
            print(colored("Orders Fixed Successfully", "green"))
    else:
        print(colored("Order Integrity Check Successful", "green"))


if __name__ == "__main__":
    log.logInit("Order")
    integrityCheck("SO/")
