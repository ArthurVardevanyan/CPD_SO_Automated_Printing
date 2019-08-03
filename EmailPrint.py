import os
import json
from files import folder_list
from files import file_list
from PostScript import ticket_conversion
import pdfkit

OUTPUT_DIRECTORY = 'School_Orders/'


def Email_Html(PATH, Files):
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
    for j in range(0, 10):
        temp2 = str(Files[j]).split(".pdf")
        Files[j] = temp2[1]
        Files[j] = str(Files[j]).replace("'", "").replace(",", "")
    for j in range(1, 11):
        if "File " + str(j)+"<" in html:
            html = html.replace("File " + str(j)+"<", "File " + str(j) + ": " + Files[j-1]+"<")
    with open(PATH+ "/Tickets/"+ORDER_NAME+".html", "w") as text_file:
        text_file.write(html)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.2in',
        'margin-right': '0.2in',
        'margin-bottom': '0.2in',
        'margin-left': '0.2in',
    }



    pdfkit.from_string(html, PATH + "/Tickets/"+ORDER_NAME+'.pdf', options=options)
    ticket_conversion(PATH + "/Tickets/"+ORDER_NAME+'.pdf')

Start = str(input("Start #: "))
End = str(input("End #: "))
Job_Specs = {}
Total_Copies = 0
Total_Staples = 0
for ORDER_NUMBER in range(int(Start), int(End)+1):
    ORDER_NUMBER = str(ORDER_NUMBER)
    ORDER_NAME = " "  # This is the Order Name taken from the subject line.=
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            ORDER_NAME = i
    if ORDER_NAME == " ":
        continue
    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
        JOB_INFO = json.load(json_file)

    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    files_list = []
    for items in JOB_INFO_FILES:
        files_list.append(
            items + ": " + str(JOB_INFO_FILES.get(items))[20:][:-1])  # Remove clutter from string
    Email_Html(OUTPUT_DIRECTORY+'/'+ORDER_NAME, files_list)
    print(ORDER_NAME)
