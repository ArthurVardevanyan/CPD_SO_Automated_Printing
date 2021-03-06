# jsonData.py
__version__ = "v20200801"
# Built-In Libraries
import json
import os
import glob
from datetime import datetime
# Downloaded Libraries
import PyPDF2
# Local Files
import files
import PostScript
import order as o
import log


def json_data(order):
    """
    Generates the JSON/DICT for the current order.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        json/dict: The JSON/DICT for the order.
    """
    json_Data = {'Account ID': 'CHANGE ME'}
    json_Data["Order Number"] = order.NUMBER
    json_Data["Order Subject"] = order.SUBJECT
    FILES = files.file_list(order)
    # Imports the Email contents line by line.
    email = []
    with open("".join([order.OD, '/', order.NAME, '/', order.NAME, ".txt"]), "r") as f:
        for line in f.readlines():
            email.append(line.rstrip('\n'))
    json_Data["Email ID"] = email[0][2:]
    json_Data["Files"] = {}
    # This gets the number of pages for every pdf file for the job.
    for i in range(len(FILES)):
        try:
            f = open('/'.join([order.OD, order.NAME, FILES[i]]), "rb")
            pdf = PyPDF2.PdfFileReader(f)
            json_Data["Files"]["".join(["File ", str(
                i+1)])] = {"File Name": FILES[i],  "Page Count": str(pdf.getNumPages())}
            f.close()
        except:
            log.logger.exception("Using Alternative Page Count Source")
            pdf = files.page_count(
                '/'.join([order.OD, order.NAME, FILES[i]]))
            json_Data["Files"]["".join(["File ", str(
                i+1)])] = {"File Name": FILES[i],  "Page Count": str(pdf)}
    # Removes the duplicate portion of the email that contains html (form) code.
    for i in range(len(email)):
        if "IF YOU HAVE ANY QUESTIONS" in email[i]:
            email = email[8:-(len(email)-i)]
            break
    # Searchs for required elements from the form for the JSON file.
    for i in range(len(email)):
        test_string = "Timestamp"
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Date Ordered"] = line[1]
        test_string = "*Timestamp: *"
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Date Ordered"] = line[1]
        test_string = "Email address "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Email"] = line[1]
        test_string = "Your Last Name "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Last Name"] = line[1]
        test_string = "Your First Name "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["First Name"] = line[1]
        test_string = "Your Call Back Number "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Phone Number"] = line[1]
        test_string = "Your building "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Building"] = line[1]
        test_string = "Number of Copies Needed per File "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Copies"] = line[1]
        test_string = "Printing Setup "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Duplex"] = line[1]
        test_string = "Collated or Uncollated "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Collation"] = line[1]
        test_string = "Paper Size, Type, and Color "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Paper"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Stapling "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Stapling"] = line[1]
        test_string = "Drilling - Three Hole Punch "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Drilling"] = line[1]
        test_string = "Folding "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Folding"] = line[1]
        test_string = "Cutting "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Cutting"] = line[1]
        test_string = "Slip Sheets and/or Shrink Wrap "
        if test_string in email[i]:
            line = email[i].split(test_string)
            extra = ""
            j = 1
            while(not ("Special Instructions " in email[i+j] or "Deliver to: " in email[i+j])):
                extra = "".join([" ", extra, " ", email[i+j]])
                j += 1
            json_Data["Slip Sheets / Shrink Wrap"] = "".join(
                [line[1], extra])
        test_string = "Special Instructions "
        if test_string in email[i]:
            line = email[i].split(test_string)
            extra = ""
            j = 1
            while(not("Deliver to: " in email[i+j])):
                extra = "".join([" ", extra, " ", email[i+j]])
                j += 1
            json_Data["Special Instructions"] = "".join([line[1], extra])
        test_string = "Booklet Fold and Staple "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Booklets"] = line[1]
        test_string = "Front Cover "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Front Cover"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Back Cover "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Back Cover"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Deliver to: (Staff Member's Name) "
        if test_string in email[i]:
            line = email[i].split(test_string)
            json_Data["Deliver To Name"] = line[1]
        test_string = "Deliver To:"
        if test_string in email[i]:
            line = email[i].split(test_string)
            line2 = ""
            if ("@" not in email[i+1]):
                if len(email[i+1]) == 5:
                    line2 = " " + email[i+1]
                else:
                    line2 = email[i+1]
            json_Data["Deliver To Address"] = (line[1].replace(
                "=", "").strip() + line2).strip()
        json_Data["Status"] = order.status = "NotStarted"
        json_Data["Cost"] = order.COST = 0
    # Creates the JSON file
    with open("".join([order.OD, '/', order.NAME, '/', order.NAME, '.json']), 'w') as outfile:
        json.dump(json_Data, outfile, indent=4, separators=(',', ': '))
    return json_Data


def orderStatusExport(order, STATUS, DATE):
    """
    Exports the Status of the order with the date time.

    Puts in the JSON file wether the Ticker or the Order has been printed.

    Parameters: 
        order   (object): The object containing all the information for the current order.
        STATUS  (str)   : The status of the order.
        DATE    (str)   : The Date which it was modified.

    Returns: 
        void: Unused Return
    """
    JSON_PATH = "".join(
        [order.OD, '/', order.NAME, '/', order.NAME, '.json'])
    with open(JSON_PATH) as json_file:
        JOB_INFO = json.load(json_file)
    now = datetime.now()
    current_time = ""
    if(DATE):
        current_time = "_" + now.strftime("%Y%m%d:%H%M")
    order.status = STATUS + current_time
    JOB_INFO["Status"] = order.status
    with open(JSON_PATH, 'w') as outfile:
        json.dump(JOB_INFO, outfile, indent=4, separators=(',', ': '))


def main(OUTPUT_DIRECTORY):
    log.logInit("JSON")
    print = log.Print
    input = log.Input
    Start = str(input("Start #: "))
    End = str(input("End   #: "))
    folders = files.folder_list(OUTPUT_DIRECTORY)
    ORDER_NAMES = []
    for ORDER_NUMBER in range(int(Start), int(End)+1):
        ORDER_NUMBER = str(ORDER_NUMBER).zfill(5)
        for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
            if ORDER_NUMBER in i:
                ORDER_NAMES.append(i)
    for ORDER_NAME in ORDER_NAMES:
        print(ORDER_NAME)
        order = o.Order()
        order.NAME = ORDER_NAME
        order.NUMBER = ORDER_NAME[:10]
        order.SUBJECT = ORDER_NAME[11:]
        order.OD = OUTPUT_DIRECTORY
        json_data(order)


if __name__ == "__main__":
    main("SO/")
