# Print.py
__version__ = "v20190807"

# Source for email fetch https://gist.github.com/robulouski/7442321#file-gmail_imap_dump_eml-py

# Built-In Libraries
import sys
import imaplib
import os
import time
import shutil
import re
import getpass

# Downloaded Libraries
from termcolor import colored 
from colorama import init

# use Colorama to make Termcolor work on Windows too
init()

# Local Files
from GDrive import Google_Drive_Downloader
from SchoolDataJson import school_data_json
from PostScript import postscript_conversion
from PostScript import file_merge
from files import page_counts
from EmailPrint import Email_Printer

print("School Order Downloader Revision: ", __version__)

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = "@gmail.com"
EMAIL_FOLDER = "Inbox"
OUTPUT_DIRECTORY = 'School_Orders/'
PASSWORD = getpass.getpass()

# This Function extracts the Google Drive FileIDs from the contents of the Email


def link_extractor(EmailBody, OrderNumber, OUTPUT_DIRECTORY, Subject, Error):
    file_links = EmailBody[0]
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

        # Removing Unwanted Characters
        for i in range(len(file_links)):
            file_links[i] = file_links[i][2:].strip()
            file_links[i] = file_links[i].replace("3D", "", 1).replace(
                "https://drive.google.com/open?id", "").replace("\\r", "").replace("\\n", "")
            file_links[i] = re.sub(r'[\\\:*?\"<>|.;=\]\']', "", file_links[i])
            print(file_links[i])

        # Calls the Google Drive Downloader Function in GDrive.py
        for ids in file_links:
            Google_Drive_Downloader(
                ids, OrderNumber, OUTPUT_DIRECTORY, Subject, Error)
    else:
        print("This Isn't A School Order")


def process_mailbox(M):

    # Gets all the UNSEEN emails from the INBOX
    rv, data = M.search(None, 'UNSEEN')
    if rv != 'OK':
        print("No messages found!")
        return

    emails_proccessed = 0
    for num in data[0].split():
        ORDER_NUMBER = ""
        error_state = ""

        rv, data = M.fetch(num, '(UID BODY[TEXT])')  # Email Body
        # Email Subject
        subject = M.fetch(num, '(UID BODY[HEADER.FIELDS (Subject)])')
        # Stripping Unwanted Content
        subject = str(subject[1][0][1]).replace(
            "Subject: ", "").replace("Copy Job - ", "")
        subject = subject[2:-9].strip()
        subject = re.sub(r'[/\r\n\\:*?\"()<>|.;]', " ", subject)
        # Keeps only the First 35 Characters of the subject.
        subject = subject[:35].rstrip()

        email_body = str(data[0][1])

        try:  # Checks if Email is Indeed A School Order, Strips Unwanted Information
            email_body = email_body.split("Order Number:", 1)
            ORDER_NUMBER = str(email_body[1])
            ORDER_NUMBER = ORDER_NUMBER[:9].strip()
            ORDER_NUMBER = ORDER_NUMBER.replace('\\r', "").replace(" ", "")
            ORDER_NUMBER = re.sub(r'[\\*]', "", ORDER_NUMBER)
            email_body.pop(0)
        except:
            print("This Email is Not Standard, Will Still Attempt to Download Files.")
            error_state = "Error/"

        if rv != 'OK':
            print("ERROR getting message", num)
            return
        print("Order: ", ORDER_NUMBER, " ", subject)

        try:
            os.makedirs(OUTPUT_DIRECTORY +
                        error_state+ORDER_NUMBER+" "+subject)
        except OSError:
            print("Creation of the directory %s failed" %
                  OUTPUT_DIRECTORY+error_state+"/"+subject)
            print("Successfully created the directory %s " %
                  OUTPUT_DIRECTORY+error_state+"/"+subject)
        if("Re:" in subject):  # Ignore Replies from Teachers
            print("This is a reply, skipping")
        else:
            # Calls Google Drive Link Extractor
            link_extractor(email_body, ORDER_NUMBER,
                           OUTPUT_DIRECTORY, subject, error_state)
            # Makes a file and Writes Email Contents to it.
            f = open(OUTPUT_DIRECTORY+error_state+ORDER_NUMBER+" " +
                     subject + "/" + ORDER_NUMBER+" " + subject+'.txt', 'wb')
            f.write(data[0][1])
            f.close()
        try:
            # Create JSON file with Job Requirements
            JOB_INFO = school_data_json(ORDER_NUMBER, "School_Orders")
        except:
            print("JSON File Failed")
        try:
            # Create PostScript File
            postscript_conversion(ORDER_NUMBER, "School_Orders")
        except:
            print("PostScript Conversion Failed")
        try:
            # Merge Uncollated Files
            if(JOB_INFO.get('Duplex', False) == "Two-sided (back to back)"):
                DUPLEX_STATE = True
                print('Double Sided')
            else:
                DUPLEX_STATE = False
                print('Single Sided')
            if JOB_INFO.get('Collation', False) == "Uncollated" and JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and len(JOB_INFO.get('Files', False)) != 1:
                if page_counts(OUTPUT_DIRECTORY, ORDER_NUMBER+" " + subject) / len(JOB_INFO.get('Files', False)) >= 10:
                    print("DUE TO PAGE COUNT, MERGED TURNED OFF")
                else:
                    file_merge(OUTPUT_DIRECTORY, ORDER_NUMBER +
                               " " + subject, DUPLEX_STATE)
            else:
                print("Not Merging")
        except:
            print("File Merge Failure")
        try:
            # Create Email Html Pdf & PS
            Email_Printer(ORDER_NUMBER)
        except:
            print("Email Conversion Failed")
        emails_proccessed += 1
    return emails_proccessed


def main():
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
                EMAILS_PROCCESSED = process_mailbox(M)
                print("\n\n\n\n\n\n\n\n")
                print("Emails Proccessed: ", EMAILS_PROCCESSED)
                print("Im Resting, Check Back Later:")
                print(colored("!--DO NOT CLOSE--!", "red"))
                print("School Order Downloader Revision: ", __version__)
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
    main()
