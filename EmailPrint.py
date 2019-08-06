# EmailPrint.py
__version__ = "v20190805"

# Built-In Libraries
import os
import json

# Downloaded Libraries
import pdfkit

# Local Files
from files import folder_list
from files import file_list
from PostScript import ticket_conversion
from Print import print_processor
# https://micropyramid.com/blog/how-to-create-pdf-files-in-python-using-pdfkit/
OUTPUT_DIRECTORY = 'School_Orders/'


def Email_Html(ORDER_NAME, PATH, NAME, Files):
    try:
        os.makedirs(PATH + "/Tickets")
        print("Successfully created the directory " + PATH + "/Tickets")
    except OSError:
        print("Creation of the directory failed " + PATH + "/Tickets")

    email = [line.rstrip('\n') for line in open(
        PATH+'/'+ORDER_NAME+".txt", "r")]
    for i in range(len(email)):
        if "<p>Your copy job has been submitted as shown below:</p>" in email[i]:
            start_line = i
            end_line = len(email)-7
    html = ""
    for i in range(start_line, end_line):
        temp = email[i]
        temp = temp[:-1]
        temp = temp.replace("3D", "")
        temp = temp.replace("href", "")
        html = html + temp
    if len(Files) != 0:
        for j in range(0, len(Files)):
            temp2 = str(Files[j]).split(".pdf")
            Files[j] = temp2[1]
            Files[j] = str(Files[j]).replace("'", "").replace(",", "")
        for j in range(1,  len(Files)+1):
            if "File " + str(j)+"<" in html:
                html = html.replace("File " + str(j)+"<",
                                    "File " + str(j) + ": " + Files[j-1]+"<").replace("=E2=80=93 ", "").replace("=E2=80=93 ", "")
    style = "<head><style>html * { font-size: 1em !important; color: #000 !important; font-family: Arial !important; }</style></head>"

    html = style + NAME + html + temp

    with open(PATH + "/Tickets/"+ORDER_NAME+".html", "w") as text_file:
        text_file.write(html)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.2in',
        'margin-right': '0.2in',
        'margin-bottom': '0.2in',
        'margin-left': '0.2in',
    }
    path_wkthmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_string(html, PATH + "/Tickets/" +
                       ORDER_NAME+'.pdf', options=options, configuration=config)
    ticket_conversion(PATH + "/Tickets/"+ORDER_NAME+'.pdf')

# Start = str(input("Start #: "))
# End = str(input("End #: "))

# for ORDER_NUMBER in range(int(Start), int(End)+1):


def Email_Printer(ORDER_NUMBER):
    ORDER_NUMBER = str(ORDER_NUMBER)
    ORDER_NAME = " "  # This is the Order Name taken from the subject line.=
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            ORDER_NAME = i
    if ORDER_NAME == " ":
        return
    files_list = []
    NAME = ""
    try:
        with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
            JOB_INFO = json.load(json_file)
        JOB_INFO_FILES = JOB_INFO.get('Files', False)

        for items in JOB_INFO_FILES:
            files_list.append(
                items + ": " + str(JOB_INFO_FILES.get(items))[20:][:-1])  # Remove clutter from string
        NAME = "Bill To: " + \
            JOB_INFO.get('First Name', False) + ' ' + \
            JOB_INFO.get('Last Name', False) + " "
    except:
        print("JSON open-failure")
    Email_Html(ORDER_NAME, OUTPUT_DIRECTORY+'/'+ORDER_NAME, NAME, files_list)
    print(ORDER_NAME)


print_que = []
print_count = 0
print_count_2 = 0


def main():
    count = 0
    Start = str(input("Start #: "))
    End = str(input("End   #: "))
    LPR = "C:/Windows/SysNative/lpr.exe -S 10.56.54.162 -P PS "
    folders = folder_list(OUTPUT_DIRECTORY)
    for ORDER_NUMBER in range(int(Start), int(End)+1):
        # Email_Printer(ORDER_NUMBER)

        ORDER_NAME = " "
        ORDER_NUMBER = str(ORDER_NUMBER)
        for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
            if ORDER_NUMBER in i:
                ORDER_NAME = i
        if ORDER_NAME == " ":
            continue
        PATH = OUTPUT_DIRECTORY+ORDER_NAME+"/Tickets/"+ORDER_NAME+".pdf.ps"
        if os.path.exists(PATH) == False:
            continue
        else:
            MEDIA_COLOR = ("white", "blue", "yellow", "green", "pink",
                           "ivory", "gray", "buff", "goldenrod,", "red", "orange")
            # Allows differnet color banner sheets. Common Pastel/Astrobrights Colors
            banner_sheet_color = MEDIA_COLOR[0]
            # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
            with open('PJL_Commands/BannerSheet.ps', 'rb') as f:
                pjl_lines = f.readlines()

            # Swap template color for color of choice
            for i in range(len(pjl_lines)):
                if str('<media-color syntax="keyword">') in str(pjl_lines[i]):
                    pjl_lines[i] = str.encode(
                        '@PJL XCPT <media-color syntax="keyword">' + banner_sheet_color + '</media-color>\n')
            banner_sheet_color = MEDIA_COLOR[1]
            # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
            with open('PJL_Commands/BannerSheet.ps', 'rb') as f:
                pjl_lines_2 = f.readlines()

            # Swap template color for color of choice
            for i in range(len(pjl_lines_2)):
                if str('<media-color syntax="keyword">') in str(pjl_lines_2[i]):
                    pjl_lines_2[i] = str.encode(
                        '@PJL XCPT <media-color syntax="keyword">' + banner_sheet_color + '</media-color>\n')

            with open('PJL_Commands/input.ps', 'wb') as f:
                for item in pjl_lines:
                    f.write(item)

            file_names = ['PJL_Commands/input.ps',
                          PATH, 'PJL_Commands/End.ps']
            with open(PATH+"1.ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)
            with open('PJL_Commands/input.ps', 'wb') as f:
                for item in pjl_lines_2:
                    f.write(item)

            file_names = ['PJL_Commands/input.ps',
                          PATH, 'PJL_Commands/End.ps']
            with open(PATH+"2.ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)

            print_que.append(LPR + '"' + PATH+"1.ps" +
                             '" -J "' + ORDER_NUMBER + '"')
            print_que.append(LPR + '"' + PATH+"2.ps" +
                             '" -J "' + ORDER_NUMBER + '"')
            count += 1

    print_processor(print_que)
    try:
        os.remove("PJL_Commands/input.ps")  # remove temp file
    except:
        print("Temp File Remove Failed")
    print(str(count) + " Order Ran")
    quit = str(input("Press Any Key To Exit"))
    print(quit)


if __name__ == "__main__":
    print("\nTerminal Email Printing REV: " + __version__)
    main()