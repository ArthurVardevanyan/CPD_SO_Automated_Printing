# Print.py
__version__ = "v20191231"

# Local Files
import files
import BannerSheet
import instructions
import EmailPrint
import printer
import PostScript

# Built-In Libraries
import os
import glob
import json


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


def impression_counter(PAGE_COUNTS, COPIES, PRINTER):
    if PRINTER == 0:
        return 0
    if PRINTER == 1:
        return 1
    # Counts the number of impressions that are sent to each printer for load balancing
    global D110_156
    global D110_162
    if D110_156 < D110_162:
        D110_156 += PAGE_COUNTS * COPIES
        return 0
    if D110_162 < D110_156:
        D110_162 += PAGE_COUNTS * COPIES
        return 1


def can_run(JOB_INFO, COLOR, BOOKLETS, COVERS):
    # Determines if jobs is able to be ran or not using this script
    if(JOB_INFO.get('Ran', False) == "True"):
        return False
    if(JOB_INFO.get('Stapling', False)):
        if(JOB_INFO.get('Stapling', False) == "Upper Left - portrait" or JOB_INFO.get('Stapling', False) == "Upper Left - landscape" or JOB_INFO.get('Stapling', False) == "Double Left - portrait" or JOB_INFO.get('Stapling', False) == "None"):
            None
        else:
            return False
    if(not COVERS and JOB_INFO.get('Front Cover', False)):
        return False
    if(not COVERS and JOB_INFO.get('Back Cover', False)):
        return False
    if(JOB_INFO.get('Booklets', False) == "Yes" and BOOKLETS == 0):
        return False
    if("11 x 17" in str(JOB_INFO.get('Paper', False))):
        return False
    if(JOB_INFO.get('Paper', False) != "8.5 x 11 Paper White" and COLOR == 0):
        return False
    if("color" in str.lower(JOB_INFO.get('Slip Sheets / Shrink Wrap', "")) and "print" in str.lower(JOB_INFO.get('Slip Sheets / Shrink Wrap', ""))):
        return False
    if("color" in str.lower(JOB_INFO.get('Special Instructions', "")) and "print" in str.lower(JOB_INFO.get('Special Instructions', ""))):
        return False
    if(not COVERS and "cover" in str.lower(JOB_INFO.get('Special Instructions', ""))):
        return False
    return True


def order_selection(ORDER_NUMBER, Folders, AUTORUN):
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


def pjl_merge(OUTPUT_DIRECTORY, ORDER_NAME, MERGED, FILES):

    try:
        os.makedirs(OUTPUT_DIRECTORY +
                    "/"+ORDER_NAME + "/PSP")
        print("Successfully created the directory ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PSP")
    except OSError:
        print("Creation of the directory failed ",
              "/", OUTPUT_DIRECTORY, "/", ORDER_NAME, "/PSP")

    if MERGED == True:
        # Add the PJL Commands to the merged file in preperation to print.
        file_names = ['PJL_Commands/input.ps', OUTPUT_DIRECTORY+"/" +
                      ORDER_NAME + "/"+ORDER_NAME+".ps", 'PJL_Commands/End.ps']
        with open(OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP/"+ORDER_NAME+".ps", 'wb') as outfile:
            for fname in file_names:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
        return 1
    elif MERGED == False:
        # Add the PJL Commands to the files in preperation to print.
        for i in range(len(FILES)):
            file_names = ['PJL_Commands/input.ps', OUTPUT_DIRECTORY+"/"+ORDER_NAME +
                          "/PostScript/"+FILES[i]+".ps", 'PJL_Commands/End.ps']
            with open(OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP/"+FILES[i][:40][:-4]+".ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)
        return 1
    return 0


def printing(Orders, ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER, COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS, COVERS):
    # Runs the bulk of code
    print_result = ''  # Used for Status Output

    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = files.folder_list(OUTPUT_DIRECTORY)

    ORDER_NAME = order_selection(ORDER_NUMBER, Folders, AUTORUN)
    if("Order DNE" in ORDER_NAME or "Aborted @ CO#" in ORDER_NAME or "ON Not Valid" in ORDER_NAME or "Aborted @ INT: " in ORDER_NAME):
        return ORDER_NAME
    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    try:
        with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
            JOB_INFO = json.load(json_file)
    except:
        if(not AUTORUN):
            return "".join(["Aborted @ JS#: ", ORDER_NUMBER, " ", ORDER_NAME])
        else:
            if(EMAILPRINT):
                D110_IP = "156" if PRINTER == 0 else "162"
                EmailPrint.Email_Print(OUTPUT_DIRECTORY,
                                       ORDER_NAME, print_que, "toptray", D110_IP)
                return "".join(["Not Supported S:  ", ORDER_NAME])
    # Keeps track of how much each printer has printed for load balancing
    page_counts = files.page_counts(OUTPUT_DIRECTORY, ORDER_NAME)
    D110_IP = impression_counter(page_counts, int(
        JOB_INFO.get('Copies', False)), PRINTER)

    # This calls the function that creates the banner sheet for the given order number
    BANNER_SHEET_FILE = BannerSheet.banner_sheet(
        JOB_INFO, "".join([OUTPUT_DIRECTORY, '/', ORDER_NAME, '/']))

    # Checks if the job specs can be ran
    if (not can_run(JOB_INFO, COLOR, BOOKLETS, COVERS)):
        print(colored("This Order Currently Does not Support AutoSelection, please double check if the order requires the normal driver.", "red"))
        if(not AUTORUN):
            if(EMAILPRINT):
                EmailPrint.Email_Print(OUTPUT_DIRECTORY,
                                       ORDER_NAME, print_que, "toptray", D110_IP)
            return "".join(["Not Supported:  ", ORDER_NAME])
        else:
            if(EMAILPRINT):
                EmailPrint.Email_Print(OUTPUT_DIRECTORY,
                                       ORDER_NAME, print_que, "toptray", D110_IP)
            return "".join(["Not Supported AutoS: ", ORDER_NAME])

    print("\nNumber of (Total) Copies Listed Per File: ",
          colored(JOB_INFO.get('Copies', False), "magenta"))
    if(JOB_INFO.get('Special Instructions', False)):
        print("SPECIAL INSTRUCTIONS: ",
              JOB_INFO.get('Special Instructions', False))
    if(JOB_INFO.get('Slip Sheets / Shrink Wrap', False)):
        print("Slip or Shrink Wrap: ",
              JOB_INFO.get('Slip Sheets / Shrink Wrap', False))

    SIP = instructions.Special_Instructions(JOB_INFO)
    if(JOB_INFO.get('Special Instructions', False) == False and JOB_INFO.get('Slip Sheets / Shrink Wrap', False) == False or JOB_INFO.get('Booklets', False) == "Yes"):
        SETS = 1
        if(JOB_INFO.get('Booklets', False) == "Yes"):
            COPIES_PER_SET = 1
        else:
            COPIES_PER_SET = int(JOB_INFO.get('Copies', False))
        print("\n!--I WILL TAKE IT FROM HERE--!")
        print_result = "SUCCESS!     : "
    elif(SIP != (0, 0)):
        SETS = SIP[0]
        COPIES_PER_SET = SIP[1]
        print("Sets: ", colored(SETS, "magenta"))
        print("CPS : ", colored(COPIES_PER_SET, "magenta"))
        print(
            "\n!--I WILL TAKE IT FROM HERE & DONE WITH SPECIAL INSTRUCTION PROCESSING --!")
        print_result = "SUCCESS SPI! : "
    else:
        if(not AUTORUN):
            # If their are special instructions prompt the user to manually enter copies and set counts
            print("If more than one set is required, do the appropriate calculation to determine correct amount of Sets and Copies per Set")

            while True:
                try:
                    SETS = int(input("\nHow Many Sets?: "))
                    if(SETS == 0):
                        return "".join(["Aborted @ Set: ", ORDER_NAME])
                    break
                except:
                    pass
            while True:
                try:
                    COPIES_PER_SET = int(input("How Many Copies Per Set?: "))
                    if(COPIES_PER_SET == 0):
                        return "".join(["Aborted @ CPS: ", ORDER_NAME])
                    break
                except:
                    pass
            print_result = "Manual Input : "
        else:
            if(EMAILPRINT):
                EmailPrint.Email_Print(OUTPUT_DIRECTORY,
                                       ORDER_NAME, print_que, "toptray", D110_IP)

            return "".join(["Not Supported SPI  : ", ORDER_NAME])

    if os.path.exists(OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PostScript/') == False:
        try:
            # Create PostScript File
            print(colored(
                "This was an Archived School Order, PostsScript files are being Regenerated.", 'green'))
            PostScript.postscript_conversion(ORDER_NUMBER, OUTPUT_DIRECTORY)
        except:
            print("PostScript Conversion Failed")

    # This gets the number of pages for every pdf file for the job.
    MERGED = False
    # Sets the correct PJL commands
    MERGED = instructions.pjl_insert(
        JOB_INFO, COPIES_PER_SET, page_counts, COVERS)
    if(COVERS and "cover" in str.lower(JOB_INFO.get('Special Instructions', ""))):
        MERGED = instructions.cover_manual(
            OUTPUT_DIRECTORY, ORDER_NAME, JOB_INFO)

   # Merge PostScript Header File to All Postscript Job Files
    pjl_merge(OUTPUT_DIRECTORY, ORDER_NAME, MERGED, FILES)
    try:
        os.remove("PJL_Commands/input.ps")  # remove temp file
    except:
        print("Temp File Remove Failed")

    # Gets list of Files in the Postscript Print Ready Folder
    Print_Files = files.postscript_list(OUTPUT_DIRECTORY, ORDER_NAME, "PSP")

    LPR = ["C:/Windows/SysNative/lpr.exe -S 10.56.54.156 -P PS ",
           "C:/Windows/SysNative/lpr.exe -S 10.56.54.162 -P PS "]

    print("\n")
    if(EMAILPRINT):
        EmailPrint.Email_Print(OUTPUT_DIRECTORY, ORDER_NAME,
                               print_que, "stacker", D110_IP)
    lpr_path = ""

    if(JOB_INFO.get('Booklets', False) == "Yes"):
        approved = 0
        for i in range(SETS):
            for j in range(len(Print_Files)):
                lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                lpr_path = LPR[D110_IP] + '"' + OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PSP/' + \
                    Print_Files[j] + '" -J "' + Print_Files[j] + '"'
                print(lpr_path.replace(
                    "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0])
                print_que.append(lpr_path)
        printer.print_processor(print_que)  # Does the printing
        print("PLEASE CHECK PROOF, if any files look incorrect, please cancel order")
        while True:
            try:
                approved = int(input(''.join(["Approved?  Yes : ", colored("1", "cyan"), " | Flip & Proof?: ", colored(
                    "2", "cyan"), " | No : ", colored("0", "cyan"), " "])))
                break
            except:
                pass
        if(approved == 1):
            COPIES_PER_SET = int(JOB_INFO.get('Copies', False))
            instructions.pjl_insert(JOB_INFO, COPIES_PER_SET, page_counts)
            pjl_merge(OUTPUT_DIRECTORY, ORDER_NAME, MERGED, FILES)
        elif(approved == 2):
            JOB_INFO["Duplex"] = "two-sided-short-edge"
            instructions.pjl_insert(JOB_INFO, COPIES_PER_SET, page_counts)
            pjl_merge(OUTPUT_DIRECTORY, ORDER_NAME, MERGED, FILES)
            for i in range(SETS):
                for j in range(len(Print_Files)):
                    lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                    lpr_path = LPR[D110_IP] + '"' + OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PSP/' + \
                        Print_Files[j] + '" -J "' + Print_Files[j] + '"'
                    print(lpr_path.replace(
                        "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                        '-P PS "C:/S/SO/', "").split("-J")[0])
                print_que.append(lpr_path)
            printer.print_processor(print_que)  # Does the printing
            while True:
                try:
                    approved = 1 if int(
                        input(''.join(["Approved?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " "]))) == 1 else 0
                    break
                except:
                    pass
            if(approved == 1):
                COPIES_PER_SET = int(JOB_INFO.get('Copies', False))
                instructions.pjl_insert(JOB_INFO, COPIES_PER_SET, page_counts)
                pjl_merge(OUTPUT_DIRECTORY, ORDER_NAME, MERGED, FILES)
            else:
                return "Booklet Not Approved"
        else:
            return "Booklet Not Approved"
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
            lpr_path = LPR[D110_IP] + '"' + OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PSP/' + \
                Print_Files[j] + '" -J "' + Print_Files[j] + '"'
            print(lpr_path.replace(
                "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                '-P PS "C:/S/SO/', "").split("-J")[0])
            print_que.append(lpr_path)

    print("\n")
    Orders.append(ORDER_NAME)
    return "".join([print_result, LPR[D110_IP][41:44], " : ", ORDER_NAME])


def main(AUTORUN, SEQUENTIAL, EMAILPRINT, COLOR, BOOKLETS, COVERS):
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
                pass
        loop = True
        ORDER_NUMBER = []  # The List of order numbers to validate and run
        # Contains the list of orders that were processed and also displays the state of them. ex, ran automatically, with manual input, invalid, aborted, etc.
        printed = []
        temp = ""
        while(True):
            if(temp != "run" and SEQUENTIAL == False):
                temp = str(input("Type In an Order Number: "))
            if(temp != "run" and SEQUENTIAL == False and BOOKLETS == True):
                ORDER_NUMBER.append(temp)
                temp = "run"
            if(temp != "run" and SEQUENTIAL == False):
                ORDER_NUMBER.append(temp)
            elif(temp != "run" and SEQUENTIAL == True):
                Start = str(input("Start #: "))
                End = str(input("End   #: "))
                for ORDER_NUMBERS in range(int(Start), int(End)+1):
                    ORDER_NUMBER.append(ORDER_NUMBERS)
                temp = "run"
            else:
                OUTPUT_DIRECTORY = "SO/"
                print("\nI am Going to Run:")
                print('\n'.join(map(str, ORDER_NUMBER)))
                for orders in ORDER_NUMBER:

                    printed.append(
                        printing(Orders, str(orders), OUTPUT_DIRECTORY, D110_IP, COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS, COVERS))  # Does all the processing for the orders
                print("\n")
                print('\n'.join(map(str, printed)))
                printer.print_processor(print_que)  # Does the printing
                files.file_cleanup(Orders, OUTPUT_DIRECTORY)
                print("\n")
                print('\n'.join(map(str, printed)))
                while True:
                    try:
                        loop = True if int(
                            input(''.join(["\nSubmit Another Set of Orders?  Yes : (", colored("1", "cyan"), ") | No : (", colored("0", "cyan"), "): "]))) == 1 else False
                        break
                    except:
                        pass

                os.system('clear')  # on linux
                os.system('CLS')    # on windows
                break
    return 1


if __name__ == "__main__":
    print("Terminal Auto Printing  REV:", colored(__version__, "magenta"))
    print("Terminal Email Printing REV:",
          colored(EmailPrint.__version__, "magenta"))
    print('Type Your Order Number and Hit Enter,\nType "', colored(
        'run', 'green'), '" then hit enter when your all set. \n')
    print("Compatible Jobs will AutoRun, jobs will pause for requested input if needed.")
    print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests.")
    print(colored("Purple Paper", "magenta"),
          " (Or any bright color) MUST BE loaded in bypass as gray plain paper.\n")
    while True:
        try:
            SEQUENTIAL = True if int(
                input(''.join(["Enable Sequential Printing  Paper?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else False
            break
        except:
            pass
    while True:
        try:
            EMAILPRINT = True if int(
                input(''.join(["Print Emails with Jobs?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else False
            if(EMAILPRINT):
                print("Make Sure White and Bright Colored Paper is loaded!")
            break
        except:
            pass
    while True:
        try:
            COLOR = 1 if int(
                input(''.join(["Enable Colored Paper?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else 0
            if(COLOR):
                print(
                    "Make sure to load colored paper before submitting jobs, otherwise banner sheets will all print first!")
            break
        except:
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
            pass
    while True:
        try:
            COVERS = 1 if int(
                input(''.join(["Enable Covers?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default) "]))) == 1 else 0
            break
        except:
            pass
    main(False, SEQUENTIAL, EMAILPRINT, COLOR, BOOKLETS, COVERS)
