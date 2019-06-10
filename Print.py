import os
import glob
from PyPDF2 import PdfFileReader
from files import folder_list
from files import file_list
from files import postscript_list
import json
from BannerSheet import banner_sheet
from PostScript import file_merge
ORIGINAL_PATH = os.getcwd()
ORIGINAL_PATH = ORIGINAL_PATH.replace("\\", "/")
D110_162 = 0
D110_156 = 1
print_que = []
print_count = 0
print_count_2 = 0


def print_processor():
    printed = 0
    run = True
    global print_count_2
    while run:
        os.chdir(ORIGINAL_PATH)  # Change path back to relative path
        if print_count_2 >= 40:
            print("Printed so Far: " + str(print_count_2))
            input(
                "Please Confirm Printers Will Support 40 More Job IDS before pressing enter: ")
            print_count_2 = 0
        if len(print_que) > 0:
            if("banner" not in print_que[0]):
                os.system(print_que[0])
                print((str(print_que[0]).replace(
                    "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/School_Orders/', "").split("-J")[0]))
                print_que.pop(0)
                printed = 0
                print_count_2 += 1
        else:
            if printed == 0:
                print("\n!--PROCESSING CAUGHT UP--!:   ")
                printed = 1
                run = False
                print_count_2 += 1


def impression_counter(PAGE_COUNTS, COPIES):
    global D110_156
    global D110_162
    if D110_156 < D110_162:
        D110_156 += PAGE_COUNTS * COPIES
        return 0
    if D110_162 < D110_156:
        D110_162 += PAGE_COUNTS * COPIES
        return 1


def color_extract(JOB_INFO):
    color_list = (str(JOB_INFO.get('Paper', False))).split()
    color = color_list[-1].lower()
    if color == 'canary':
        return 'yellow'
    else:
        return color


def can_run(JOB_INFO, COLOR):
    # Determines if jobs is able to be ran or not.
    if(JOB_INFO.get('Ran', False) == "True"):
        return False
    if("Card Stock" in JOB_INFO.get('Paper', False)):
        return False
    if(JOB_INFO.get('Stapling', False)):
        if(JOB_INFO.get('Stapling', False) != "Upper Left - portrait"):
            return False
    if(JOB_INFO.get('Front Cover', False)):
        return False
    if(JOB_INFO.get('Back Cover', False)):
        return False
    if(JOB_INFO.get('Paper', False) != "8.5 x 11 Paper White" and COLOR == 0):
        return False
    return True


def printing(ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER, COLOR):

    # This is the Order Name taken from the subject line.
    ORDER_NAME = "No Order Selected"
    print_result = ''
    page_counts = 0
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = folder_list(OUTPUT_DIRECTORY)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            ORDER_NAME = i

    print(ORDER_NAME)
    if(ORDER_NAME == "No Order Selected"):
        print("Order Number is not Valid")
        return "ON Not Valid : " + ORDER_NUMBER
    while True:
        try:
            if(int(input("Confirm Order Yes : 1 | No : 0 ")) == 0):
                return
            break
        except:
            pass

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
        JOB_INFO = json.load(json_file)

    # This calls the function that creates the banner sheet for the given order number
    BANNER_SHEET_FILE = banner_sheet(
        JOB_INFO, OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/')
    # This gets the number of pages for every pdf file for the job.
    for i in range(len(files)):
        pdf = PdfFileReader(
            open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+files[i], "rb"))
        print("Page Count: " + str(pdf.getNumPages()) +
              " FileName: " + files[i])
        page_counts = page_counts + pdf.getNumPages()
    # Checks if the job specs can be ran, and then sets the correct PJL commands
    JOB_COLOR = color_extract(JOB_INFO)
    if (can_run(JOB_INFO, COLOR)):
        print('\nChoosen Options:')
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
            print('Double Sided')
        else:
            duplex = str.encode(
                '@PJL XCPT <sides syntax="keyword">one-sided</sides>\n')
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
            default = str.encode('@PJL XCPT <value syntax="enum">3</value>\n')
            print('No Finishing')
        else:
            default = str.encode('')
        media_color = str.encode(
            '@PJL XCPT <media-color syntax="keyword">'+JOB_COLOR+'</media-color>\n')
        print(JOB_COLOR)
        if(JOB_INFO.get('Special Instructions', False)):
            print("SPECIAL INSTRUCTIONS: " +
                  JOB_INFO.get('Special Instructions', False))
    else:
        print("This Order Currently Does not Support AutoSelection, please double chek if the order requires the normal driver.")
        return "Not Supported:  " + ORDER_NAME
    print("Number of (Total) Copies Listed Per File: " +
          JOB_INFO.get('Copies', False))

    if(JOB_INFO.get('Slip Sheets / Shrink Wrap', False)):
        print("SPECIAL INSTRUCTIONS: " +
              JOB_INFO.get('Slip Sheets / Shrink Wrap', False))
    if(JOB_INFO.get('Special Instructions', False) == False and JOB_INFO.get('Slip Sheets / Shrink Wrap', False) == False):
        SETS = 1
        COPIES_PER_SET = int(JOB_INFO.get('Copies', False))
        print("\n!--I WILL TAKE IT FROM HERE--!")
        print_result = "SUCCESS!     : "
    else:
        # If thier are special instructions prompt the user to manually enter copies and set counts
        print("If more than one set is requried, do the appropriate calculation to determine correct amount of Sets and Copies per Set")
        SETS = int(input("\nHow Many Sets?: "))
        COPIES_PER_SET = int(input("How Many Copies Per Set?: "))
        print_result = "Manual Input : "
    COPIES_COMMAND = str.encode(
        '@PJL XCPT <copies syntax="integer">'+str(COPIES_PER_SET)+'</copies>\n')
    with open('PJL_Commands/PJL.ps', 'rb') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if str('<media-color syntax="keyword">') in str(lines[i]):
            lines[i] = media_color
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

    with open('PJL_Commands/input.ps', 'wb') as f:
        for item in lines:
            f.write(item)
    MERGED = False
    # If it makes sense to use merged files, it uses them.
    if str('<sheet-collate syntax="keyword">uncollated') in str(collation) and len(JOB_INFO.get('Files', False)) != 1:
        MERGED = True
        print("THESE FILES WERE MERGED!")

    current_path = os.getcwd()  # Current Path
    try:
        os.makedirs(current_path + "/" + OUTPUT_DIRECTORY +
                    "/"+ORDER_NAME + "/PSP")
        print("Successfully created the directory " + current_path +
              "/" + OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP")
    except OSError:
        print("Creation of the directory failed " + current_path +
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
            with open(OUTPUT_DIRECTORY+"/"+ORDER_NAME + "/PSP/"+files[i][:35][:-4]+".ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)

    Print_Files = postscript_list(OUTPUT_DIRECTORY, ORDER_NAME, "PSP")
    if PRINTER == 0:
        D110_IP = 0
        D110 = "156 : "
    if PRINTER == 1:
        D110_IP = 1
        D110 = "162 : "
    if PRINTER == 2:
        D110_IP = impression_counter(page_counts, int(
            JOB_INFO.get('Copies', False)))
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

    print(BANNER_SHEET_FILE)  # Print and Run Banner Sheet
    for i in range(SETS):
        for j in range(len(Print_Files)):
            print("File Name: " + Print_Files[j])

    lpr_path = LPR[D110_IP] + '"' + BANNER_SHEET_FILE + '"'
    print(lpr_path)
    # Change Path so only File Name Shows up on Printer per File Banner Sheet
    print_que.append(lpr_path)
    temp_path = ORIGINAL_PATH + '/' + OUTPUT_DIRECTORY+'/' + ORDER_NAME + '/PSP'
    os.chdir(temp_path)
    global print_count
    for i in range(SETS):
        for j in range(len(Print_Files)):
            print_count += 1
            lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
            lpr_path = LPR[D110_IP] + '"' + temp_path + '/' + \
                Print_Files[j] + '" -J "' + Print_Files[j] + '"'
            print(lpr_path.replace(
                "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                '-P PS "C:/S/School_Orders/', "").split("-J")[0])
            print_que.append(lpr_path)

    print("\n")
    return print_result + D110 + ORDER_NAME


os.chdir(ORIGINAL_PATH)  # Change path back to relative path
print("\nTerminal AutoPrinting REV: 20190610")
print('Type Your Order Number and Hit Enter, \nType "run" then hit enter when your all set. \n')
print("Comaptible Jobs will AutoRun, jobs will pause for requested input if needed.")
print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests.")
print("Purple Paper (Or any bright color) MUST BE loaded in bypass as gray plain paper.\n")
while True:
    try:
        COLOR = int(
            input("Enable Colored Paper?  Yes : 1 | No : 0 (default) "))
        break
    except:
        pass
if(COLOR != 1):
    COLOR = 0
bigger_loop = True
while(bigger_loop):
    while True:
        try:
            D110_IP = int(
                input("Choose a Printer: 156 (0), 162 (1), Auto (2): "))
            break
        except:
            pass
    loop = True
    ORDER_NUMBER = []
    printed = []
    while(loop):
        temp = str(input("Type In an Order Number: "))
        if(temp != "run"):
            ORDER_NUMBER.append(temp)
        else:
            loop = False
            print("\nI am Going to Run:")
            print('\n'.join(map(str, ORDER_NUMBER)))
            for orders in ORDER_NUMBER:
                os.chdir(ORIGINAL_PATH)
                printed.append(
                    printing(str(orders), "School_Orders", D110_IP, COLOR))
            print("\n")
            print('\n'.join(map(str, printed)))
            print(print_count)
            print_processor()
            print("\n")
            print('\n'.join(map(str, printed)))
            print(print_count)
            while True:
                try:
                    if(int(input("\nSubmit Another Set of Orders?  Yes : 1 | No : 0 ")) == 1):
                        bigger_loop = True
                    else:
                        bigger_loop = False
                    break
                except:
                    pass
            os.system('clear')  # on linux
            os.system('cls')  # on windows
