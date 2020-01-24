# EmailPrint.py
__version__ = "v20191224"

# Built-In Libraries
import os
import json

# Downloaded Libraries
import pdfkit
import termcolor
from termcolor import colored
import colorama

# Local Files
import files
import PostScript
import printer
import log
import SchoolDataJson
import order as o

# use Colorama to make Termcolor work on Windows too
colorama.init()

# https://micropyramid.com/blog/how-to-create-pdf-files-in-python-using-pdfkit/


def Email_Html(ORDER_NAME, PATH, NAME, Files):
    F = "".join([PATH, "/Tickets"])
    try:
        if not os.path.exists(F):
            os.makedirs(F)
            print("Successfully created the directory ", F)
    except OSError:
        print("Creation of the directory failed ", PATH, "/Tickets")

    email = [line.rstrip('\n') for line in open("".join([
        PATH, '/', ORDER_NAME, ".txt"]), "r")]
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
        path_wkthmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_string(html, "".join([PATH, "/Tickets/",
                                          ORDER_NAME, '.pdf']), options=options, configuration=config)
    PostScript.ticket_conversion(
        "".join([PATH, "/Tickets/", ORDER_NAME, '.pdf']))
    return 1


def Email_Printer(OUTPUT_DIRECTORY, ORDER_NAME, error_state):

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
    if D110_IP == 1 or D110_IP == 0:
        D110_IP = "156" if D110_IP == 0 else "162"
    LPR = "".join(
        ["C:/Windows/SysNative/lpr.exe -S 10.56.54.", str(D110_IP), " -P PS "])
    PATH = "".join([OUTPUT_DIRECTORY, "/", ORDER_NAME,
                    "/Tickets/", ORDER_NAME, ".pdf.ps"])
    if os.path.exists(PATH) == False:
        Email_Printer(OUTPUT_DIRECTORY, ORDER_NAME, "")
    if os.path.exists(PATH) == False:
        return 0
    else:

        # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
        with open('PJL_Commands/BannerSheet.ps', 'rb') as f:
            pjl_lines = f.readlines()

        if(STACKER == "toptray"):
            for i in range(len(pjl_lines)):
                if str('<output-bin syntax="keyword">') in str(pjl_lines[i]):
                    pjl_lines[i] = str.encode(
                        '@PJL XCPT 		<output-bin syntax="keyword">top</output-bin>\n')
            for i in range(len(pjl_lines)):
                if str('<value syntax="keyword">') in str(pjl_lines[i]):
                    pjl_lines[i] = str.encode(
                        '@PJL XCPT 	<value syntax="keyword">none</value>\n')

        with open('PJL_Commands/input.ps', 'wb') as f:
            for item in pjl_lines:
                f.write(item)

        file_names = ['PJL_Commands/input.ps',
                      PATH, 'PJL_Commands/End.ps']
        with open("".join([PATH[:-6], "pjl.ps"]), 'wb') as outfile:
            for fname in file_names:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
        print(ORDER_NAME)
        print_que.append(
            "".join([LPR, '"', PATH[:-6], "pjl.ps", '" -J "', ORDER_NAME, '"']))

        #TEMPORARY TILL WHOLE FILE GETS CONVERTED TO OOP
        JSON_PATH = "".join(
            [OUTPUT_DIRECTORY, '/', ORDER_NAME, '/', ORDER_NAME, '.json'])
        order = o.Order()
        order.OD = OUTPUT_DIRECTORY
        order.NAME = ORDER_NAME
        with open(JSON_PATH) as json_file:
            order = o.order_initialization(order, json.load(json_file))
        order.OD = OUTPUT_DIRECTORY
        # Update Json File to Show the Email Ticket was Printing
        SchoolDataJson.orderStatusExport(order, "TicketPrinted")

        try:
            os.remove("PJL_Commands/input.ps")  # remove temp file
        except:
            print("Temp File Remove Failed")
        return 1


def main():
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
    Start = str(input("Start #: "))
    End = str(input("End   #: "))
    folders = files.folder_list(OUTPUT_DIRECTORY)
    ORDER_NAMES = []
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
        "I have Failed due to some Error"

    print(str(count), " Order(s) Ran")
    quit = str(input("Press Any Key To Exit"))
    print(quit)


if __name__ == "__main__":
    log.logInit("EmailPrint")
    print = log.Print
    input = log.Input
    print("\nTerminal Email Printing REV: ",
          colored(__version__, "magenta"))
    print('Make Sure White and Bright Colored Paper is loaded!\nSet Colored Paper as ',
          colored('"Other"', "magenta"))
    main()
