# Print.py
__version__ = "v20200801"
# Local Files
import integrity
import files
import BannerSheet
import instructions
import EmailPrint
import printer
import PostScript
import jsonData
import order as o
import log
import booklet
# Built-In Libraries
import os
import glob
import json
import datetime
# Downloaded Libraries
import PyPDF2
from termcolor import colored
import colorama
# use Colorama to make Termcolor work on Windows too
colorama.init()
# Global Variables
# Load Balancing
D110_162 = 0  # Impressions ran on this machine
D110_156 = 1  # Impressions ran on this machine


def impression_counter(order, PRINTER):
    """
    Keeps Track of how many impressions (copies) are sent to each printer. 
    Used when load balancing.

    Parameters: 
        order   (object): The object containing all the information for the current order.
        PRINTER (int)   : Determines which printer to use, or both.

    Returns: 
        bool: Return which printer to use.
    """
    if PRINTER == 0:
        return 0
    if PRINTER == 1:
        return 1
    # Counts the number of impressions that are sent to each printer for load balancing
    global D110_156
    global D110_162
    if D110_156 < D110_162:
        D110_156 += order.PAGE_COUNTS * order.COPIES
        return 0
    if D110_162 < D110_156:
        D110_162 += order.PAGE_COUNTS * order.COPIES
        return 1


def can_run(order, COLOR, BOOKLETS):
    """
    Determines if jobs is able to be ran automatically or not.

    Color / Heavyweight Paper, and Booklet overrides exist, 
    so under normal conditions they do not get attempted to run accidentally.

    Parameters: 
        order       (object): The object containing all the information for the current order.
        COLOR       (bool)  : Color / HeavyWeight Paper Override
        BOOKLETS    (bool)  : Booklet Printing Overide.

    Returns: 
        bool: Whether the order can be ran or not.
    """
    if(order.status == "True"):
        return False
    if(order.STAPLING):
        if(order.STAPLING_BOOL):
            None
        else:
            return False
    if(order.FRONT_COVER):
        return False
    if(order.BACK_COVER):
        return False
    if(order.BOOKLET == "Yes" and BOOKLETS == 0):
        return False
    if("11 x 17" in order.PAPER):
        return False
    if(order.PAPER != "8.5 x 11 Paper White" and COLOR == 0):
        return False
    if("color" in str.lower(str(order.SLIPSHEETS)) and ("print" in str.lower(str(order.SLIPSHEETS)) or "copy" in str.lower(str(order.SLIPSHEETS)))):
        return False
    if("color" in str.lower(str(order.SPECIAL_INSTRUCTIONS)) and ("print" in str.lower(str(order.SPECIAL_INSTRUCTIONS)) or "copy" in str.lower(str(order.SPECIAL_INSTRUCTIONS)))):
        return False
    if("cover" in str.lower(str(order.SPECIAL_INSTRUCTIONS))):
        return False
    return True


def order_selection(ORDER_NUMBER, Folders, AUTORUN):
    """
    Finds and returns the intended order.

    Parameters: 
        ORDER_NUMBER   (str)    : The inputted order number to look for.
        Folders        (list)   : All the orders currently downloaded.
        AUTORUN        (int)    : The autorun flag, that skips any input requests.

    Returns: 
        str: Returns the Order Name, or an Error Message
    """
    ORDER_NAME = "No Order Selected"  # Default Value
    ORDER_NAMES = []
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if(i == "Archive" or i == "Error"):
            continue
        try:
            if int(ORDER_NUMBER[:5]) == int(i[:5]):
                if str(ORDER_NUMBER) in i:
                    ORDER_NAMES.append(i)
        except:
            log.logger.exception("")
            return "".join(["Aborted @ INT: ", ORDER_NUMBER])
    if(not AUTORUN):
        if(len(ORDER_NAMES) == 0):
            print(ORDER_NUMBER, " Order Number is not Valid")
            return "".join(["ON Not Valid : ", ORDER_NUMBER])
        if(len(ORDER_NAMES) == 1):
            ORDER_NAME = ORDER_NAMES[0]
            print(ORDER_NAME)
            while True:
                try:
                    if(int(input("".join(["Confirm Order Yes : (", colored("1", "cyan"), ") | No : (", colored("0", "cyan"), ") "]))) == 0):
                        return "".join(["Aborted @ CO#: ", ORDER_NAME])
                    return ORDER_NAME
                except:
                    pass
        if(len(ORDER_NAMES) > 1):
            print(colored(
                "!--WARNING--! - DUPLICATE ORDER NUMBERS - PROCEED WITH CAUTION", "red"))
            for order_name in ORDER_NAMES:
                while True:
                    try:
                        print(order_name)
                        if(int(input("".join(["Confirm Order Yes : (", colored("1", "cyan"), ") | No : (", colored("0", "cyan"), ") "]))) == 0):
                            break
                        else:
                            return order_name
                    except:
                        pass
                if(ORDER_NAME != "No Order Selected"):
                    break
            if(ORDER_NAME == "No Order Selected"):
                return "".join(["Aborted @ CO#: ", ORDER_NUMBER, " ", ORDER_NAME])
    else:
        try:
            return str(ORDER_NAMES[0])
        except:
            return "".join(["Order DNE: ", ORDER_NAME])


def printing(Orders, ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER, COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS):
    """
    The Main function for handling printing.

    Parameters: 
        Orders              (list)  : List of Orders that are successfully ran.
        ORDER_NUMBER        (str)   : The inputted order number to look for.
        OUTPUT_DIRECTORY    (str)   : The directory where all the order reside.
        PRINTER             (int)   : Flag for which printer or printer(s) to use.
        COLOR               (bool)  : Color / HeavyWeight Paper Override
        print_que           (list)  : The list of files that need will need to be printed.
        AUTORUN             (int)   : The autorun flag, that skips any input requests.
        EMAILPRINT          (bool)  : Email/Ticket Printing Printing Overide.
        BOOKLETS            (bool)  : Booklet Printing Overide.      

    Returns: 
        str: Returns the output status of the job.
    """
    # Runs the bulk of code
    order = o.Order()
    order.OD = OUTPUT_DIRECTORY
    order.RESULT = ''  # Used for Status Output
    order.NUMBER = ORDER_NUMBER
    # Calls a function in files.py, which gets a list of all the orders downladed
    FOLDERS = files.folder_list(order.OD)
    order.NAME = order_selection(order.NUMBER, FOLDERS, AUTORUN)
    if(any(str in order.NAME for str in ("Order DNE", "Aborted @ CO#", "ON Not Valid", "Aborted @ INT: "))):
        return order.NAME
    try:
        path = order.OD+'/'+order.NAME+'/'+order.NAME+'.json'
        if os.path.exists(path):
            with open(path) as json_file:
                order = o.order_initialization(order, json.load(json_file))
        else:
            order = o.order_initialization(
                order, jsonData.json_data(order))
    except:
        log.logger.exception("")
        if(not AUTORUN):
            return "".join(["Aborted @ JS#: ", order.NUMBER, " ", order.NAME])
        else:
            if(EMAILPRINT):
                D110_IP = "156" if PRINTER == 0 else "162"
                EmailPrint.Email_Print(order.OD,
                                       order.NAME, print_que, "toptray", D110_IP)
                return "".join(["Not Supported S:  ", order.NAME])
            return "".join(["Not Supported S:  ", order.NAME])
    # Keeps track of how much each printer has printed for load balancing
    D110_IP = impression_counter(order, PRINTER)
    # This calls the function that creates the banner sheet for the given order number
    BANNER_SHEET_FILE = BannerSheet.banner_sheet(order)
    # Checks if the job specs can be ran
    if (not can_run(order, COLOR, BOOKLETS)):
        print(colored("This Order Currently Does not Support AutoSelection, please double check if the order requires the normal driver.", "red"))
        if(not AUTORUN):
            if(EMAILPRINT):
                EmailPrint.Email_Print(order.OD,
                                       order.NAME, print_que, "toptray", D110_IP)
            return "".join(["Not Supported:  ", order.NAME])
        else:
            if(EMAILPRINT):
                EmailPrint.Email_Print(order.OD,
                                       order.NAME, print_que, "toptray", D110_IP)
            return "".join(["Not Supported AutoS: ", order.NAME])
    print("\n")
    for iter in order.PAGE_COUNTS_LIST:
        print(iter)
    print("Number of (Total) Copies Listed Per File: ",
          colored(order.COPIES, "magenta"))
    if(order.SPECIAL_INSTRUCTIONS):
        print("SPECIAL INSTRUCTIONS: ", order.SPECIAL_INSTRUCTIONS)
    if(order.SLIPSHEETS):
        print("Slip or Shrink Wrap: ", order.SLIPSHEETS)
    SIP = instructions.Special_Instructions(order)
    if(order.SPECIAL_INSTRUCTIONS == False and order.SLIPSHEETS == False or order.BOOKLET == "Yes"):
        SETS = 1
        if(order.BOOKLET == "Yes"):
            COPIES_PER_SET = 1
        else:
            COPIES_PER_SET = order.COPIES
        print("\n!--I WILL TAKE IT FROM HERE--!")
        order.RESULT = "SUCCESS!     : "
    elif(SIP != (0, 0)):
        SETS = SIP[0]
        COPIES_PER_SET = SIP[1]
        print("Sets: ", colored(SETS, "magenta"))
        print("CPS : ", colored(COPIES_PER_SET, "magenta"))
        print(
            "\n!--I WILL TAKE IT FROM HERE & DONE WITH SPECIAL INSTRUCTION PROCESSING --!")
        order.RESULT = "SUCCESS SPI! : "
    else:
        if(not AUTORUN):
            # If their are special instructions prompt the user to manually enter copies and set counts
            print("If more than one set is required, do the appropriate calculation to determine correct amount of Sets and Copies per Set")
            while True:
                try:
                    SETS = int(input("\nHow Many Sets?: "))
                    if(SETS == 0):
                        return "".join(["Aborted @ Set: ", order.NAME])
                    break
                except:
                    log.logger.exception("")
                    pass
            while True:
                try:
                    COPIES_PER_SET = int(input("How Many Copies Per Set?: "))
                    if(COPIES_PER_SET == 0):
                        return "".join(["Aborted @ CPS: ", order.NAME])
                    break
                except:
                    log.logger.exception("")
                    pass
            order.RESULT = "Manual Input : "
        else:
            if(EMAILPRINT):
                EmailPrint.Email_Print(order.OD,
                                       order.NAME, print_que, "toptray", D110_IP)
            return "".join(["Not Supported SPI  : ", order.NAME])
    if os.path.exists(order.OD+'/' + order.NAME + '/PostScript/') == False:
        try:
            # Create PostScript File
            print(colored(
                "This was an Archived Order, PostsScript files are being Regenerated.", 'green'))
            PostScript.postscript_conversion(order)
            if(instructions.merging(order)):
                PostScript.file_merge(order, instructions.duplex_state(order))
        except:
            log.logger.exception("")
            print("PostScript Conversion Failed")
    # This gets the number of pages for every pdf file for the job.
    MERGED = False
    # Sets the correct PJL commands
    MERGED = instructions.pjl_insert(order, COPIES_PER_SET)
   # Merge PostScript Header File to All Postscript Job Files
    instructions.pjl_merge(order, "PSP", MERGED, order.FILE_NAMES)
    try:
        # remove temp file
        os.remove("input.ps")
        os.remove("Blank.ps")
    except:
        log.logger.exception("")
        print("Temp File Remove Failed")
    # Gets list of Files in the Postscript Print Ready Folder
    Print_Files = files.postscript_list(order.OD, order.NAME, "PSP")
    LPR = ["C:/Windows/System32/lpr.exe -S 10.56.54.156 -P PS ",
           "C:/Windows/System32/lpr.exe -S 10.56.54.162 -P PS "]
    print("\n")
    if(EMAILPRINT):
        EmailPrint.Email_Print(order.OD, order.NAME,
                               print_que, "stacker", D110_IP)
    lpr_path = ""

    if(order.BOOKLET == "Yes"):
        booklet.bookletPrint(
            log, order, print_que, Print_Files, SETS, LPR, D110_IP, MERGED)
    else:
        lpr_path = LPR[D110_IP] + '"' + BANNER_SHEET_FILE + '"'
        print_que.append(lpr_path)
        print(BANNER_SHEET_FILE)  # Print and Run Banner Sheet
        i = 0
        while i < SETS:
            i += 1
            for j in range(len(Print_Files)):
                print("File Name: ", Print_Files[j])
        print("\n")
        print(lpr_path)
        # Change Path so only File Name Shows up on Printer per File Banner Sheet
        for i in range(SETS):
            for j in range(len(Print_Files)):
                lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                lpr_path = LPR[D110_IP] + '"' + order.OD+'/' + order.NAME + '/PSP/' + \
                    Print_Files[j] + '" -J "' + Print_Files[j] + '"'
                log.logger.debug((lpr_path.replace(
                    "C:/Windows/System32/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0]))
                print_que.append(lpr_path)
        print("\n")
    Orders.append(order.NAME)
    IP = ["P156", "P162"]
    try:
        jsonData.orderStatusExport(order, str(IP[D110_IP]), False)
    except:
        log.logger.exception("")
        print("Order Status Update Failed")
    # , order.NUMBER,  str(IP[D110_IP])
    return "".join([order.RESULT, LPR[D110_IP][40:43], " : ", order.NAME])


def main(AUTORUN, EMAILPRINT, COLOR, BOOKLETS):
    """
    Sets up the pre run conditions.

    Parameters: 
        AUTORUN             (int)   : The autorun flag, that skips any input requests.
        EMAILPRINT          (bool)  : Email/Ticket Printing Printing Overide.
        COLOR               (bool)  : Color / HeavyWeight Paper Override
        BOOKLETS            (bool)  : Booklet Printing Overide.      

    Returns: 
        bool: Unused Return.
    """
    # Contains the list of final commands for all the orders that were proccessed to be run.
    print_que = []
    Orders = []
    # Check if user wants to processes jobs with colored paper, if disabled this adds protection against accidentally running jobs on colored paper.
    loop = True
    # Lets the user choose with printer they would like to use, or if they want to autoload balance between both printers.
    while(loop):
        while True:
            try:
                D110_IP = int(
                    input(''.join(["Choose a Printer: 156 (", colored("0", "cyan"), "), 162 (", colored("1", "cyan"), "), Auto (", colored("2", "cyan"), "): "])))
                if D110_IP == 1 or D110_IP == 2 or D110_IP == 0:
                    break
                else:
                    pass
            except:
                log.logger.exception("")
                pass
        loop = True
        ORDER_NUMBER = []  # The List of order numbers to validate and run
        # Contains the list of orders that were processed and also displays the state of them. ex, ran automatically, with manual input, invalid, aborted, etc.
        printed = []
        temp = ""
        while(True):
            if(temp != "run"):
                temp = str(input("Type In an Order Number: "))
            if(temp != "run" and BOOKLETS == True):
                ORDER_NUMBER.append(temp)
                temp = "run"
            if(temp != "run"):
                ORDER_NUMBER.append(temp)
            else:
                OUTPUT_DIRECTORY = "SO/"
                print("\nI am Going to Run:")
                print('\n'.join(map(str, ORDER_NUMBER)))
                for orders in ORDER_NUMBER:
                    printOrder = printing(Orders, str(
                        orders), OUTPUT_DIRECTORY, D110_IP, COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS)
                    # Does all the processing for the orders
                    printed.append(printOrder)  # [0])
                print("\n")
                print('\n'.join(map(str, printed)))
                printer.print_processor(print_que)  # Does the printing
                files.file_cleanup(Orders, OUTPUT_DIRECTORY)
                print("\n")
                print('\n'.join(map(str, printed)))
                log.report("print", printed, log)
                while True:
                    try:
                        loop = True if int(
                            input(''.join(["\nSubmit Another Set of Orders?  Yes : (", colored("1", "cyan"), ") | No : (", colored("0", "cyan"), "): "]))) == 1 else False
                        break
                    except:
                        log.logger.exception("")
                        pass
                os.system('clear')  # on linux
                os.system('CLS')    # on windows
                break
    return 1


if __name__ == "__main__":
    if (datetime.datetime.today().date() > datetime.datetime.strptime(log.license, "%Y%m%d").date()):
        exit()
    log.logInit("Print")
    print = log.Print
    input = log.Input
    print("Terminal Auto Printing  REV:", colored(__version__, "magenta"))
    print("Terminal Email Printing REV:",
          colored(EmailPrint.__version__, "magenta"))
    print('Type Your Order Number and Hit Enter,\nType ', colored(
        '"run"', 'green'), ' then hit enter when your all set. \n')
    print("Compatible Jobs will AutoRun, jobs will pause for requested input if needed.")
    print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Input or Invalid Requests.")
    print(colored("Purple Paper", "magenta"),
          " (Or any bright color) should be loaded as gray plain paper.\n")
    integrity.integrity()
    o.integrityCheck("SO/")
    while True:
        try:
            EMAILPRINT = True if int(
                input(''.join(["Print Emails with Jobs?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else False
            if(EMAILPRINT):
                print("Make Sure White and Bright Colored Paper is loaded!")
            break
        except:
            log.logger.exception("")
            pass
    while True:
        try:
            COLOR = 1 if int(
                input(''.join(["Enable Colored Paper / Cardstock?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else 0
            if(COLOR):
                print(
                    "Make sure to load colored paper / cardstock before submitting jobs, otherwise banner sheets will all print first!")
            break
        except:
            log.logger.exception("")
            pass
    while True:
        try:
            BOOKLETS = 1 if int(
                input(''.join(["Enable Booklets?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else 0
            if(BOOKLETS):
                print(
                    "BOOKLETS CAN ONLY BE RAN ONE ORDER AT A TIME! Currently only Pre-Imposed and Letter Sized")
            break
        except:
            log.logger.exception("")
            pass
    main(False, EMAILPRINT, COLOR, BOOKLETS)
