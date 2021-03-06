# EmailPrint.py
__version__ = "v20201115"
# Built-In Libraries
import os
import json
# Downloaded Libraries
import pdfkit
import termcolor
from termcolor import colored
import colorama
# Local Files
import integrity
from PJL_Commands.BannerSheetPS import bannerSheet
from PJL_Commands.PJL_PS import end
import files
import PostScript
import printer
import log
import jsonData
import order as o
# use Colorama to make Termcolor work on Windows too
colorama.init()
# https://micropyramid.com/blog/how-to-create-pdf-files-in-python-using-pdfkit/


def Email_Html(ORDER_NAME, PATH, NAME, Files):
    """
    Creates an HTML Ticket, and a PDF Ticket

    The HTML portion of the Email is extracted and saved for use as a printable ticket.
    The page count for each file is also added to the HTML table.
    The person who is being billed is also added to the top of the ticket.

    Parameters: 
        ORDER_NAME  (str)   : The name of the order.
        PATH        (str)   : Location of the order.
        NAME        (str)   : The html for the person that is being billed for the order that will be inserted into the html.
        Files       (list)  : The html list of filenames and page counts that will be inserted into the html.

    Returns: 
        bool: unused return
    """
    F = "".join([PATH, "/Tickets"])
    try:
        if not os.path.exists(F):
            os.makedirs(F)
            print("Successfully created the directory ", F)
    except OSError:
        print("Creation of the directory failed ", PATH, "/Tickets")
    email = []
    with open("".join([PATH, '/', ORDER_NAME, ".txt"]), "r") as f:
        for line in f.readlines():
            email.append(line.rstrip('\n'))
    for i in range(len(email)):
        if "<p>Your copy job has been submitted as shown below:</p>" in email[i]:
            start_line = i
            end_line = len(email)-8
    html = ""
    for i in range(start_line, end_line):
        temp = email[i]
        temp = temp[:-1]
        temp = temp.replace("3D", "")
        temp = temp.replace("href", "")
        html = "".join([html, temp])
    if len(Files) != 0:
        for j in range(0, len(Files)):
            temp2 = str(Files[j]).rsplit(',', 1)
            Files[j] = temp2[1]
            Files[j] = str(Files[j]).replace("'", "").replace(",", "")
            temp3 = Files[j].split(": ")
            Files[j] = "".join([temp3[0], ": <b>", temp3[1], "</b>"])
        for j in range(1,  len(Files)+1):
            if "".join(["File ", str(j), "<"]) in html:
                html = html.replace("".join(["File ", str(j), "<"]),
                                    "".join(["File ", str(j), ": ", Files[j-1], "<"])).replace("=E2=80=93 ", "").replace("=E2=80=93 ", "")
    style = "<head><style>html * { font-size: 1em !important; color: #000 !important; font-family: Arial !important; }</style></head>"
    html = "".join([style, NAME, html, temp])
    with open("".join([PATH, "/Tickets/", ORDER_NAME, ".html"]), "w") as text_file:
        text_file.write(html)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.2in',
        'margin-right': '0.2in',
        'margin-bottom': '0.2in',
        'margin-left': '0.2in',
    }
    # Doesn't Output to Log
    if(os.name == "posix"):
        pdfkit.from_string(html, "".join([PATH, "/Tickets/",
                                          ORDER_NAME, '.pdf']), options=options,)
    else:
        path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_string(html, "".join([PATH, "/Tickets/",
                                          ORDER_NAME, '.pdf']), options=options, configuration=config)
    PostScript.ticket_conversion(
        "".join([PATH, "/Tickets/", ORDER_NAME, '.pdf']))
    return 1


def Email_Printer(OUTPUT_DIRECTORY, ORDER_NAME, error_state):
    """
    Loads the requested order, and generates Bill Name and Page Count Html

    Generates the html that gets inserted for the current orders ticket.
    Bill TO: and Page Counts for each file.

    Parameters: 
        OUTPUT_DIRECTORY    (str): Location of the order.
        ORDER_NAME          (str): The name of the order.
        error_state         (str): The flag that determines where to pull the order from.

    Returns: 
        bool: unused return
    """
    files_list = []
    NAME = ""
    try:
        with open("".join([OUTPUT_DIRECTORY, '/', error_state, ORDER_NAME, '/', ORDER_NAME, '.json'])) as json_file:
            JOB_INFO = json.load(json_file)
        JOB_INFO_FILES = JOB_INFO.get('Files', False)
        for items in JOB_INFO_FILES:
            files_list.append("".join([
                items, ": ", str(JOB_INFO_FILES.get(items))[20:][:-1]]))  # Remove clutter from string
        NAME = "".join(["<b>Bill To: ",             JOB_INFO.get('First Name', False), ' ',
                        JOB_INFO.get('Last Name', False), "</b><br>", ORDER_NAME, "<br>"])
    except:
        print("JSON open-failure")
    Email_Html(ORDER_NAME, "".join([OUTPUT_DIRECTORY, '/',
                                    error_state, ORDER_NAME]), NAME, files_list)
    print(ORDER_NAME)
    return 1


print_count = 0
print_count_2 = 0


def Email_Print(OUTPUT_DIRECTORY, ORDER_NAME, print_que, STACKER, D110_IP):
    """
    Facialites the process of generating and printing order tickets.

    Parameters: 
        OUTPUT_DIRECTORY   (str)   : Location of the order.
        ORDER_NAME         (str)   : The name of the order.
        print_que          (list)  : The list of print ready files waiting to be run. (Used when Bulk Printing)
        STACKER            (str)   : Which Tray of the Printer to print the ticket out of.
        D110_IP            (int)   : Which IP to use form the LPR list.

    Returns: 
        bool: unused return
    """
    if D110_IP == 1 or D110_IP == 0:
        D110_IP = "156" if D110_IP == 0 else "162"
    LPR = "".join(
        ["C:/Windows/System32/lpr.exe -S 10.56.54.", str(D110_IP), " -P PS "])
    PATH = "".join([OUTPUT_DIRECTORY, "/", ORDER_NAME,
                    "/Tickets/", ORDER_NAME, ".pdf.ps"])
    if os.path.exists(PATH) == False:
        Email_Printer(OUTPUT_DIRECTORY, ORDER_NAME, "")
    if os.path.exists(PATH) == False:
        return 0
    else:
        # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
        pjl_lines = bannerSheet.splitlines()
        if(STACKER == "toptray"):
            for i in range(len(pjl_lines)):
                if str('<output-bin syntax="keyword">') in str(pjl_lines[i]):
                    pjl_lines[i] = str.encode(
                        '@PJL XCPT 		<output-bin syntax="keyword">top</output-bin>')
            for i in range(len(pjl_lines)):
                if str('<value syntax="keyword">') in str(pjl_lines[i]):
                    pjl_lines[i] = str.encode(
                        '@PJL XCPT 	<value syntax="keyword">none</value>')
        with open('input.ps', 'wb') as f:
            for item in pjl_lines:
                f.write(item + b"\n")
        file_names = ['input.ps',
                      PATH]
        with open("".join([PATH[:-6], "pjl.ps"]), 'wb') as outfile:
            for fname in file_names:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
            for line in end.splitlines():
                outfile.write(line)

        print(ORDER_NAME)
        print_que.append(
            "".join([LPR, '"', PATH[:-6], "pjl.ps", '" -J "', ORDER_NAME, '"']))
        # TEMPORARY TILL WHOLE FILE GETS CONVERTED TO OOP
        JSON_PATH = "".join(
            [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.json'])
        order = o.Order()
        order.OD = OUTPUT_DIRECTORY
        order.NAME = ORDER_NAME
        with open(JSON_PATH) as json_file:
            order = o.order_initialization(order, json.load(json_file))
        order.OD = OUTPUT_DIRECTORY
        # Update Json File to Show the Email Ticket was Printing
        try:
            jsonData.orderStatusExport(order, "Ticket", True)
        except:
            log.logger.exception("")
            print("Order Status Update Failed")
        try:
            os.remove("input.ps")  # remove temp file
        except:
            print("Temp File Remove Failed")
        return 1


def main():
    """
    Facialites the process of handeling which orders need thier tickets printed.

    Asks the operator to select printer and enter order number range.
    Can also print all unprinted orders.

    Parameters: 
        N/A

    Returns: 
        void: unused return
    """
    OUTPUT_DIRECTORY = 'SO'
    print_que = []
    count = 0
    while(True):
        try:
            D110_IP = int(
                input(''.join(["Choose a Printer: 156 (", colored("0", "cyan"), "), 162 (", colored("1", "cyan"), "): "])))
            if D110_IP == 1 or D110_IP == 0:
                D110_IP = "156" if D110_IP == 0 else "162"
                break
            else:
                pass
        except:
            pass
    try:
        unread = o.notStarted()
        print("".join(["\nTheir are ", str(len(unread)),
                       " unprinted orders, Enter 0, 0 to run "]))
    except:
        unread = None
        log.logger.exception("")
    Start = str(input("Start #: "))
    End = str(input("End   #: "))
    folders = files.folder_list(OUTPUT_DIRECTORY)
    ORDER_NAMES = []
    if(Start == '0' and End == '0'):
        ORDER_NAMES = unread
    else:
        for ORDER_NUMBER in range(int(Start), int(End)+1):
            ORDER_NUMBER = str(ORDER_NUMBER).zfill(5)
            for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
                if ORDER_NUMBER in i:
                    ORDER_NAMES.append(i)
    try:
        for ORDER_NAME in ORDER_NAMES:
            count += Email_Print(OUTPUT_DIRECTORY, ORDER_NAME,
                                 print_que, "toptray", D110_IP)
        printer.print_processor(print_que)
    except:
        print("I have Failed due to some Error")
        print("Try Deleting the Last Order Displayed")
        log.logger.exception("")
    #log.report("emailPrint", ORDER_NAMES, log)
    print(str(count), " Order(s) Ran")
    quit = str(input("Press Any Key To Exit"))
    print(quit)


if __name__ == "__main__":
    if(os.name != "posix"):
        os.chdir('..')
    log.logInit("EmailPrint")
    print = log.Print
    input = log.Input
    print("\n\nTerminal Email Printing REV: ",
          colored(__version__, "magenta"))
    print('\nMake Sure White and Bright Colored Paper are loaded!\nSet Colored Paper as ',
          colored('"Other"', "magenta"))
    integrity.integrity()
    o.integrityCheck("SO/")
    main()
