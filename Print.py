# Print.py
__version__ = "v20190920"

# Local Files
from PostScript import file_merge
from files import file_list, folder_list, postscript_list
from BannerSheet import banner_sheet
from spi import Special_Instructions

# Built-In Libraries
import os
import glob
import json

# Downloaded Libraries
from PyPDF2 import PdfFileReader
from termcolor import colored
from colorama import init

# use Colorama to make Termcolor work on Windows too
init()


# Global Variables

# Load Balancing
D110_162 = 0  # Impressions ran on this machine
D110_156 = 1  # Impressions ran on this machine

# Variables for Safety check to not send more jobs than the printer can hold.
jobs_since_reset = 0
jobs_ran = 0


def print_processor(print_que):
    # Runs through the list of files to send to the printers, pausing for input as needed.
    print(colored("!--DO NOT CLOSE--!", "red"))
    ID_LIMIT = 40
    run = True
    global jobs_ran
    global jobs_since_reset
    while run:
        if jobs_ran >= ID_LIMIT:
            print("Printed so Far: " + str(jobs_ran))
            input(
                "Please Confirm Printers Will Support 40 More Job IDS before pressing enter: ")
            jobs_ran = 0
            jobs_since_reset -= ID_LIMIT
        if len(print_que) > 0:
            if("banner" not in print_que[0]):
                os.system(print_que[0])
                print((str(print_que[0]).replace(
                    "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0]))
                print_que.pop(0)
                jobs_ran += 1
        else:
            print(colored("\n!--PROCESSING CAUGHT UP--!:   ", "green"))
            run = False
            jobs_ran += 1


def impression_counter(PAGE_COUNTS, COPIES):
    # Counts the number of impressions that are sent to each printer for load balancing
    global D110_156
    global D110_162
    if D110_156 < D110_162:
        D110_156 += PAGE_COUNTS * COPIES
        return 0
    if D110_162 < D110_156:
        D110_162 += PAGE_COUNTS * COPIES
        return 1


def weight_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    paper = (str(JOB_INFO.get('Paper', False))).lower()
    return "stationery-heavyweight" if "card stock" in paper else "use-ready"


def color_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    color = (str(JOB_INFO.get('Paper', False))).split()[-1].lower()
    return 'yellow' if color == 'canary' else color


def can_run(JOB_INFO, COLOR, page_counts):
    # Determines if jobs is able to be ran or not using this script
    if(JOB_INFO.get('Ran', False) == "True"):
        return False
    if(JOB_INFO.get('Stapling', False)):
        if(JOB_INFO.get('Stapling', False) == "Upper Left - portrait" or JOB_INFO.get('Stapling', False) == "None"):
            None
        else:
            return False
    if(JOB_INFO.get('Front Cover', False)):
        return False
    if(JOB_INFO.get('Back Cover', False)):
        return False
    if(JOB_INFO.get('Paper', False) != "8.5 x 11 Paper White" and COLOR == 0):
        return False
    return True


def printing(ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER, COLOR, print_que):
    # Runs the bulk of code

    ORDER_NAME = "No Order Selected"  # Default Value
    print_result = ''  # Used for Status Output
    page_counts = 0  # Used for counting impressions for current order and adding to total for load balancing between printers
    # Calls a function in files.py, which gets a list of all the orders downladed
    ORDER_NAMES = []
    Folders = folder_list(OUTPUT_DIRECTORY)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if(i == "Archive" or i == "Error"):
            continue
        try:
            if int(ORDER_NUMBER[:5]) == int(i[:5]):
                if str(ORDER_NUMBER) in i:
                    ORDER_NAMES.append(i)
        except:
            return "Aborted @ INT: " + ORDER_NUMBER

    if(len(ORDER_NAMES) == 0):
        print(ORDER_NUMBER + " Order Number is not Valid")
        return "ON Not Valid : " + ORDER_NUMBER
    if(len(ORDER_NAMES) == 1):
        ORDER_NAME = ORDER_NAMES[0]
        print(ORDER_NAME)
        while True:
            try:
                if(int(input("Confirm Order Yes : (" + colored("1", "cyan") + ") | No : (" + colored("0", "cyan") + ") ")) == 0):
                    return "Aborted @ CO#: " + ORDER_NAME
                break
            except:
                pass
    if(len(ORDER_NAMES) > 1):
        print(colored(
            "!--WARNING--! - DUPLICATE ORDER NUMBERS - PROCEED WITH CAUTION", "red"))
        for order_name in ORDER_NAMES:
            while True:
                try:
                    print(order_name)
                    if(int(input("Confirm Order Yes : (" + colored("1", "cyan") + ") | No : (" + colored("0", "cyan") + ") ")) == 0):
                        break
                    else:
                        ORDER_NAME = order_name
                        break
                except:
                    pass
            if(ORDER_NAME != "No Order Selected"):
                break
        if(ORDER_NAME == "No Order Selected"):
            return "Aborted @ CO#: " + ORDER_NUMBER + " " + ORDER_NAME

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    try:
        with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
            JOB_INFO = json.load(json_file)
    except:
        return "Aborted @ JS#: " + ORDER_NUMBER + " " + ORDER_NAME

    # This calls the function that creates the banner sheet for the given order number
    BANNER_SHEET_FILE = banner_sheet(
        JOB_INFO, OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/')

    # This gets the number of pages for every pdf file for the job.
    for i in range(len(files)):
        pdf = PdfFileReader(
            open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+files[i], "rb"))
        print("Page Count: " + colored(str(pdf.getNumPages()), "magenta") +
              " FileName: " + files[i])
        page_counts = page_counts + pdf.getNumPages()

    # Checks if the job specs can be ran, and then sets the correct PJL commands
    JOB_COLOR = color_extract(JOB_INFO)
    JOB_WEIGHT = weight_extract(JOB_INFO)
    if (can_run(JOB_INFO, COLOR, page_counts)):
        print('\nChosen Options:')
        if(JOB_INFO.get('Collation', False) == "Collated"):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print('Collated')
        else:
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')
            print('UnCollated')
        if(JOB_INFO.get('Duplex', False) == "Two-sided (back to back)"):
            duplex = str.encode(
                '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n')
            duplex_state = 2
            print('Double Sided')
        else:
            duplex = str.encode(
                '@PJL XCPT <sides syntax="keyword">one-sided</sides>\n')
            duplex_state = 1
            print('Single Sided')
        if(JOB_INFO.get('Stapling', False) == "Upper Left - portrait"):
            stapling = str.encode(
                '@PJL XCPT <value syntax="enum">20</value>\n')
            if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
                collation = str.encode(
                    '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
                print("Collation Overide - Collated")
            print("Staple - Upper Left - portrait")
        else:
            stapling = str.encode('')
        if(JOB_INFO.get('Drilling', False) == "Yes"):
            hole_punch = str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n')
            print('Hole Punched')
        else:
            hole_punch = str.encode('')
        if(JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and JOB_INFO.get('Drilling', False) != "Yes"):
            default = str.encode(
                '@PJL XCPT <value syntax="enum">3</value>\n')
            print('No Finishing')
        else:
            default = str.encode('')
        media_color = str.encode(
            '@PJL XCPT <media-color syntax="keyword">'+JOB_COLOR+'</media-color>\n')
        media_type = str.encode(
            '@PJL XCPT <media-type syntax="keyword">'+JOB_WEIGHT+'</media-type>\n')
        print(JOB_COLOR)
        print(JOB_WEIGHT)
        if(JOB_INFO.get('Special Instructions', False)):
            print("SPECIAL INSTRUCTIONS: " +
                  JOB_INFO.get('Special Instructions', False))
    else:
        print(colored("This Order Currently Does not Support AutoSelection, please double check if the order requires the normal driver.", "red"))
        return "Not Supported:  " + ORDER_NAME
    print("Number of (Total) Copies Listed Per File: " +
          colored(JOB_INFO.get('Copies', False), "magenta"))

    if(JOB_INFO.get('Slip Sheets / Shrink Wrap', False)):
        print("SPECIAL INSTRUCTIONS: " +
              JOB_INFO.get('Slip Sheets / Shrink Wrap', False))
    SPI = Special_Instructions(JOB_INFO)
    if(JOB_INFO.get('Special Instructions', False) == False and JOB_INFO.get('Slip Sheets / Shrink Wrap', False) == False):
        SETS = 1
        COPIES_PER_SET = int(JOB_INFO.get('Copies', False))
        print("\n!--I WILL TAKE IT FROM HERE--!")
        print_result = "SUCCESS!     : "
    elif(SPI != (0, 0)):
        SETS = SPI[0]
        COPIES_PER_SET = SPI[1]
        print("Sets: ", colored(SETS, "magenta"))
        print("CPS : ", colored(COPIES_PER_SET, "magenta"))
        print(
            "\n!--I WILL TAKE IT FROM HERE & DONE WITH SPECIAL INSTRUCTION PROCESSING --!")
        print_result = "SUCCESS SPI!  : "
    else:
        # If their are special instructions prompt the user to manually enter copies and set counts
        print("If more than one set is required, do the appropriate calculation to determine correct amount of Sets and Copies per Set")

        while True:
            try:
                SETS = int(input("\nHow Many Sets?: "))
                if(SETS == 0):
                    return "Aborted @ Set: " + ORDER_NAME
                break
            except:
                pass
        while True:
            try:
                COPIES_PER_SET = int(input("How Many Copies Per Set?: "))
                if(COPIES_PER_SET == 0):
                    return "Aborted @ CPS: " + ORDER_NAME
                break
            except:
                pass

        print_result = "Manual Input : "
    COPIES_COMMAND = str.encode(
        '@PJL XCPT <copies syntax="integer">'+str(COPIES_PER_SET)+'</copies>\n')
    with open('PJL_Commands/PJL.ps', 'rb') as f:
        lines = f.readlines()
    # Modifies the PJL file before adding it to the postscript files
    for i in range(len(lines)):
        if str('<media-color syntax="keyword">') in str(lines[i]):
            lines[i] = media_color
        if str('<media-type syntax="keyword">') in str(lines[i]):
            lines[i] = media_type
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = COPIES_COMMAND
        if str('<value syntax="enum">3</value>') in str(lines[i]):
            lines[i] = default
            if str('<value syntax="enum">3</value>') not in str(default):
                lines.insert(i, stapling)
                lines.insert(i+1, hole_punch)
        if str('<sheet-collate syntax="keyword">') in str(lines[i]):
            lines[i] = collation
        if str('<sides syntax="keyword">one-sided</sides>') in str(lines[i]):
            lines[i] = duplex
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]):
            lines[i] = str.encode(
                '@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            lines.insert(i, str.encode(
                '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n'))
            print("\nSplit-Sheeting!")
        # Add SlipSheets to Large Collated Sets
        if page_counts / len(JOB_INFO.get('Files', False)) / duplex_state >= 10 and str('<sheet-collate syntax="keyword">collated') in str(collation) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]) and (JOB_INFO.get('Stapling', False) != "Upper Left - portrait"):
            lines[i] = str.encode(
                '@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            lines.insert(i, str.encode(
                '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n'))
            print("\nSplit-Sheeting!")

    # The Postscript/PJL commands file that gets inserted before the file.
    with open('PJL_Commands/input.ps', 'wb') as f:
        for item in lines:
            f.write(item)
    MERGED = False
    # If it makes sense to use merged files, it uses them.
    if str('<sheet-collate syntax="keyword">uncollated') in str(collation) and len(JOB_INFO.get('Files', False)) != 1:
        if page_counts / len(JOB_INFO.get('Files', False)) / duplex_state >= 10:
            MERGED = False
            print("DUE TO PAGE COUNT, MERGED TURNED OFF")
        else:
            MERGED = True
            print("THESE FILES WERE MERGED!")

    # Create Directory for Print Ready Files
    try:
        os.makedirs(OUTPUT_DIRECTORY +
                    "/"+ORDER_NAME + "/PSP")
        print("Successfully created the directory " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP")
    except OSError:
        print("Creation of the directory failed " +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP")

    if MERGED == True:
        # Add the PJL Commands to the merged file in preperation to print.
        file_names = ['PJL_Commands/input.ps', OUTPUT_DIRECTORY+"/" +
                      ORDER_NAME + "/"+ORDER_NAME+".ps", 'PJL_Commands/End.ps']
        with open(OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP/"+ORDER_NAME+".ps", 'wb') as outfile:
            for fname in file_names:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
    if MERGED == False:
        # Add the PJL Commands to the files in preperation to print.
        for i in range(len(files)):
            file_names = ['PJL_Commands/input.ps', OUTPUT_DIRECTORY+"/"+ORDER_NAME +
                          "/PostScript/"+files[i]+".ps", 'PJL_Commands/End.ps']
            with open(OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP/"+files[i][:40][:-4]+".ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)

    # Gets list of Files in the Postscript Print Ready Folder
    Print_Files = postscript_list(OUTPUT_DIRECTORY, ORDER_NAME, "PSP")

    if PRINTER == 0:
        D110_IP = 0
        D110 = "156 : "
    if PRINTER == 1:
        D110_IP = 1
        D110 = "162 : "
    if PRINTER == 2:
        D110_IP = impression_counter(page_counts, int(
            JOB_INFO.get('Copies', False)))  # Keeps track of how much each printer has printed for load balancing
        if D110_IP == 0:
            D110 = "156 : "
        if D110_IP == 1:
            D110 = "162 : "
    LPR = ["C:/Windows/SysNative/lpr.exe -S 10.56.54.156 -P PS ",
           "C:/Windows/SysNative/lpr.exe -S 10.56.54.162 -P PS "]

    try:
        os.remove("PJL_Commands/input.ps")  # remove temp file
    except:
        print("Temp File Remove Failed")

    global jobs_since_reset
    print(BANNER_SHEET_FILE)  # Print and Run Banner Sheet
    jobs_since_reset += 1
    for i in range(SETS):
        for j in range(len(Print_Files)):
            print("File Name: " + Print_Files[j])

    lpr_path = LPR[D110_IP] + '"' + BANNER_SHEET_FILE + '"'
    print(lpr_path)
    # Change Path so only File Name Shows up on Printer per File Banner Sheet
    print_que.append(lpr_path)
    for i in range(SETS):
        for j in range(len(Print_Files)):
            jobs_since_reset += 1
            lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
            lpr_path = LPR[D110_IP] + '"' + OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PSP/' + \
                Print_Files[j] + '" -J "' + Print_Files[j] + '"'
            print(lpr_path.replace(
                "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                '-P PS "C:/S/SO/', "").split("-J")[0])
            print_que.append(lpr_path)

    print("\n")
    return print_result + D110 + ORDER_NAME


def main():
    # Contains the list of final commands for all the orders that were proccessed to be run.
    print_que = []
    print("\nTerminal AutoPrinting REV: " + colored(__version__, "magenta"))
    print("Supported are :\n• Simplex & Duplex Printing (Long Edge)\n• 3-Hole Punch\n• Top Left Portrait Staple")
    print("• White Paper, Colored Paper & Cardstock\n• SlipSheeting\n• Splitting Jobs Into Sets\n• Balancing Load Between Two Printers\n")
    print('Type Your Order Number and Hit Enter,\nType "' +
          colored('run', 'green') + '" then hit enter when your all set. \n')
    print("Compatible Jobs will AutoRun, jobs will pause for requested input if needed.")
    print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests.")
    print(colored("Purple Paper", "magenta") +
          " (Or any bright color) MUST BE loaded in bypass as gray plain paper.\n")
    # Check if user wants to processes jobs with colored paper, if disabled this adds protection against accidentally running jobs on colored paper.
    while True:
        try:
            COLOR = 1 if int(
                input("Enable Colored Paper?  Yes : " + colored("1", "cyan") + " | No : " + colored("0", "cyan") + " (default) ")) == 1 else 0
            break
        except:
            pass
    else:
        print("Make sure to load colored paper before submitting jobs, otherwise banner sheets will all print first!")
    loop = True
    # Lets the user choose with printer they would like to use, or if they want to autoload balance between both printers.
    while(loop):
        while True:
            try:
                D110_IP = int(
                    input("Choose a Printer: 156 (" + colored("0", "cyan") + "), 162 (" + colored("1", "cyan") + "), Auto (" + colored("2", "cyan") + "): "))
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
        while(True):
            temp = str(input("Type In an Order Number: "))
            if(temp != "run"):
                ORDER_NUMBER.append(temp)
            else:
                print("\nI am Going to Run:")
                print('\n'.join(map(str, ORDER_NUMBER)))
                for orders in ORDER_NUMBER:
                    printed.append(
                        printing(str(orders), "SO", D110_IP, COLOR, print_que))  # Does all the processing for the orders
                print("\n")
                print('\n'.join(map(str, printed)))
                print(jobs_since_reset)
                print_processor(print_que)  # Does the printing
                print("\n")
                print('\n'.join(map(str, printed)))
                print(jobs_since_reset)
                while True:
                    try:
                        loop = True if int(
                            input("\nSubmit Another Set of Orders?  Yes : (" + colored("1", "cyan") + ") | No : (" + colored("0", "cyan") + "): ")) == 1 else False
                        break
                    except:
                        pass

                os.system('clear')  # on linux
                os.system('CLS')    # on windows
                break


if __name__ == "__main__":
    main()
