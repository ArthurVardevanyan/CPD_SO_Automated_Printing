# Email.py
__version__ = "v20200110"

# Source for email fetch https://gist.github.com/robulouski/7442321#file-gmail_imap_dump_eml-py

# Built-In Libraries
import sys
import imaplib
import os
import time
import shutil
import re
import getpass
import datetime

# Downloaded Libraries
import termcolor
from termcolor import colored
import colorama

# Local Files
import GDrive
import SchoolDataJson
import PostScript
import files
import EmailPrint
import Print
import printer
import database
import instructions
import order as o

# use Colorama to make Termcolor work on Windows too
colorama.init()


def link_cleanup(file_links):
 # Removing Unwanted Characters
    if(len(file_links) != 0):
        for i in range(len(file_links)):
            file_links[i] = file_links[i][2:].strip()
            file_links[i] = file_links[i].replace("3D", "", 1).replace(
                "https://drive.google.com/open?id", "").replace("\\r", "").replace("\\n", "")
            file_links[i] = re.sub(r'[\\\:*?\"<>|.;=\]\']', "", file_links[i])
            print(file_links[i])
        return file_links
    else:
        return []


def link_extractor(file_links):
    # This Function extracts the Google Drive FileIDs from the contents of the Email
    # Checks if the email is indeed a School Order and not something else.
    if ("Attach your file(s) in PDF format." in file_links):
        file_links = file_links.split("Number of Copies Needed per File", 1)
        file_links.pop(1)
        file_links = str(file_links)
        file_links = file_links.split("Attach your file(s) in PDF format.", 1)
        file_links.pop(0)
        file_links = str(file_links)
        file_links = file_links.split("File ")
        file_links.pop(0)
        return file_links
    else:
        return []


def Drive_Downloader(email_body, OrderNumber, OUTPUT_DIRECTORY, Subject, Error):
    file_links = link_extractor(email_body)
    file_links = link_cleanup(file_links)
    if(len(file_links) != 0):
        # Calls the Google Drive Downloader Function in GDrive.py
        count = 0
        for ids in file_links:
            count += 1
            GDrive.Google_Drive_Downloader(
                ids, OrderNumber, OUTPUT_DIRECTORY, Subject, count, Error)
        return 1
    else:
        print("This Isn't A School Order")
        return 0


def subject_line(subject):
    # Stripping Unwanted Content
    subject = str(subject[1][0][1]).replace(
        "Subject: ", "").replace("Copy Job - ", "")
    subject = subject[2:-9].strip()
    subject = re.sub(r'[/\r\n\\:*?\"()<>|.;]', " ", subject)
    # Keeps only the First 35 Characters of the subject.
    subject = subject[:35].rstrip()
    return subject


def order_number_random():
    time = datetime.datetime.today().strftime('%M%S')
    return "".join(["-", time])


def order_number_extract(email_body, RANDOM):

    try:  # Checks if Email is Indeed A School Order, Strips Unwanted Information
        email_body = email_body.split("Order Number:", 1)
        ORDER_NUMBER = str(email_body[1])
        ORDER_NUMBER = ORDER_NUMBER[:9].strip()
        ORDER_NUMBER = ORDER_NUMBER.replace('\\r', "").replace(" ", "")
        ORDER_NUMBER = re.sub(r'[\\*]', "", ORDER_NUMBER)
        # Adds some randomness to the order number's using time
        return "".join([ORDER_NUMBER, RANDOM]), ""
    except:
        print("This Email is Not Standard, Will Still Attempt to Download Files.")
        error_state = "Error/"
        return "", error_state


def process_mailbox(M, AUTORUN, D110_IP):

    # Gets all the UNSEEN emails from the INBOX
    rv, data = M.search(None, 'UNSEEN')
    if rv != 'OK':
        print("No messages found!")
        return

    emails_proccessed = 0
    for num in data[0].split():

        order = o.Order()
        order.OD = 'SO/'

        rv, data = M.fetch(num, '(UID BODY[TEXT])')  # Email Body
        # Email Subject
        subject = subject_line(
            M.fetch(num, '(UID BODY[HEADER.FIELDS (Subject)])'))

        email_body = data[0][1]
        ORDER_NUMBER, error_state, = order_number_extract(
            str(email_body), order_number_random())
        print("Order: ", ORDER_NUMBER, " ", subject)
        ORDER_NAME = "".join([ORDER_NUMBER, " ", subject])

        order.NUMBER = ORDER_NUMBER
        order.NAME = ORDER_NAME
        order.SUBJECT = subject

        if rv != 'OK':
            print("ERROR getting message", num)
            return

        try:
            os.makedirs("".join([order.OD,
                                 error_state, ORDER_NAME]))
        except OSError:
            print("Creation of the directory %s failed" %
                  order.OD, error_state, "/", subject)
        print("Successfully created the directory %s " %
              order.OD, error_state, "/", subject)
        if("Re:" in subject):  # Ignore Replies
            print("This is a reply, skipping")
        else:
            # Calls Google Drive Link Extractor
            Drive_Downloader(str(email_body), ORDER_NUMBER,
                             order.OD, subject, error_state)
            # Makes a file and Writes Email Contents to it.
            f = open("".join([order.OD, error_state,
                              ORDER_NAME, "/", ORDER_NAME, '.txt']), 'wb')
            f.write(email_body)
            f.close()
        try:

            # Create JSON file with Job Requirements
            JOB_INFO = SchoolDataJson.school_data_json(order)
            order = o.order_initialization(order, JOB_INFO)
        except:
            print("JSON File Failed")
        try:
            # Database Input
            database.database_input(order.OD, JOB_INFO)
        except:
            print("Database Input Failed")
        try:
            # Create PostScript File
            PostScript.postscript_conversion(order)
        except:
            print("PostScript Conversion Failed")
        try:
            # Merge Uncollated Files
            if(instructions.merging(order)):
                PostScript.file_merge(order, instructions.duplex_state(order))
        except:
            print("File Merge Failure")
        try:
            if(Print.can_nup(order, False, 0)):
                PostScript.pdf_conversion(order)
                PostScript.nup(order)
                if(instructions.merging(order)):
                    PostScript.file_merge_n(
                        order, instructions.duplex_state(order))
        except:
            print("Multi-Up Failure")
        try:
            # Create Email Html Pdf & PS
            EmailPrint.Email_Printer(order.OD, ORDER_NAME, error_state)
        except:
            print("Email Conversion Failed")
        emails_proccessed += 1

        if(AUTORUN):
            COLOR = 0
            BOOKLETS = 0
            EMAILPRINT = True
            print_que = []
            Orders = []
            Print.printing(Orders, ORDER_NUMBER, "SO", D110_IP, COLOR,
                           print_que, AUTORUN, EMAILPRINT, BOOKLETS, 0, False)
            printer.print_processor(print_que)
            files.file_cleanup(Orders, order.OD)

    return emails_proccessed


def main(AUTORUN, D110_IP):
    IMAP_SERVER = 'imap.gmail.com'
    EMAIL_FOLDER = "Inbox"
    PASSWORD = getpass.getpass()
    EMAIL_ACCOUNT = "@gmail.com"
    try:
        with open("Credentials/creds.txt") as f:
            cred = f.readlines()
        cred = [x.strip() for x in cred]
        EMAIL_ACCOUNT = "".join([str(cred[0]), EMAIL_ACCOUNT])
    except:
        print("Credential Failure")
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)  # Credentials Info
    rv, data = M.select(EMAIL_FOLDER)  # pylint: disable=unused-variable

    if rv == 'OK':
        print("Processing mailbox: ", EMAIL_FOLDER)
        print("Im Resting, Check Back Later:")
        while(True):  # Infinite Loop for checking emails
            try:
                time.sleep(25)
                print("Running Loop")
                M = imaplib.IMAP4_SSL(IMAP_SERVER)
                M.login(EMAIL_ACCOUNT, PASSWORD)
                rv, data = M.select(
                    EMAIL_FOLDER)  # pylint: disable=unused-variable
                # Starts Executing the Bulk of the program
                EMAILS_PROCCESSED = process_mailbox(M, AUTORUN, D110_IP)
                print("\n\n\n\n\n\n\n\n")
                print("Emails Proccessed: ", EMAILS_PROCCESSED)
                print("Im Resting, Check Back Later:")
                print(colored("!--DO NOT CLOSE--!", "red"))
                print("School Order Downloader Revision: ",
                      colored(__version__, "magenta"))
                print("Running Again") if rv == 'OK' else print(
                    "ERROR: Unable to open mailbox ", rv)
                time.sleep(250)
            except:
                print("SOMETHING WENT HORRIBLY WRONG, Check Internet Connection")
                time.sleep(30)
                continue
        M.logout()
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)
    M.logout()


if __name__ == "__main__":
    print("\nSchool Order Downloader REV:",
          colored(__version__, "magenta"))
    print("Terminal Auto Printing  REV:",
          colored(Print.__version__, "magenta"))
    print("Terminal Email Printing REV:",
          colored(EmailPrint.__version__, "magenta"))
    print("\n")
    D110_IP = 1
    while True:
        try:
            AUTORUN = True if int(
                input("".join(["Enable Print While Download?  Yes : ", colored("1", "cyan"), " | No : ", colored("0", "cyan"), " (default/recommended) "]))) == 1 else False
            if(AUTORUN):
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
            break
        except:
            pass
    main(AUTORUN, D110_IP)
