# Source for email fetch https://gist.github.com/robulouski/7442321#file-gmail_imap_dump_eml-py
import sys
import imaplib
import getpass
from GDrive import GoogleDriveDownload
import os
import time
import shutil
import re
from SchoolDataJson import SchoolDataJson

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = "@gmail.com"
EMAIL_FOLDER = "Inbox"
OUTPUT_DIRECTORY = 'School_Orders/'
NetworkP = "P:/OneTimeJobs/School Orders"
PASSWORD = getpass.getpass()


def LinkExtractor(EmailBody, OrderNumber, OUTPUT_DIRECTORY, Subject, Error):
    FileLinks = EmailBody[0]
    if ("Attach your file(s) in PDF format." in FileLinks):
        FileLinks = FileLinks.split("Number of Copies Needed per File", 1)
        FileLinks.pop(1)
        FileLinks = str(FileLinks)
        FileLinks = FileLinks.split("Attach your file(s) in PDF format.", 1)
        FileLinks.pop(0)
        FileLinks = str(FileLinks)
        FileLinks = FileLinks.split("File ")
        FileLinks.pop(0)

        for i in range(len(FileLinks)):
            FileLinks[i] = FileLinks[i][2:].strip()
            FileLinks[i] = FileLinks[i].replace("3D", "", 1).replace(
                "https://drive.google.com/open?id", "").replace("\\r", "").replace("\\n", "")
            FileLinks[i] = re.sub(r'[\\\:*?\"<>|.;=\]\']', "", FileLinks[i])
            print(FileLinks[i])

        for y in FileLinks:
            GoogleDriveDownload(y, OrderNumber, OUTPUT_DIRECTORY, Subject, Error)
    else:
        print("This Isn't A School Order")


def process_mailbox(M):

    rv, data = M.search(None, 'UNSEEN')
    if rv != 'OK':
        print("No messages found!")
        return

    EmailsProccessed = 0
    for num in data[0].split():
        OrderNumber = ""
        Error = ""

        rv, data = M.fetch(num, '(UID BODY[TEXT])')
        Subject = M.fetch(num, '(UID BODY[HEADER.FIELDS (Subject)])')
        Subject = str(Subject[1][0][1]).replace(
            "Subject: ", "").replace("Copy Job - ", "")
        Subject = Subject[2:-9].strip()
        Subject = re.sub(r'[/\r\n\\:*?\"<>|.;]', " ", Subject)
        # Keeps only the First 75 Characters of the subject.
        Subject = Subject[:75]

        EmailBody = str(data[0][1])

        try:
            EmailBody = EmailBody.split("Order Number:", 1)
            OrderNumber = str(EmailBody[1])
            OrderNumber = OrderNumber[:9].strip()
            OrderNumber = OrderNumber.replace('\\r', "").replace(" ", "")
            OrderNumber = re.sub(r'[\\*]', "", OrderNumber)
            EmailBody.pop(0)
        except:
            print("This Email is Not Standard, Will Still Attempt to Download Files.")
            Error = "Error/"

        if rv != 'OK':
            print("ERROR getting message", num)
            return
        print("Order: ", OrderNumber, " ", Subject)
        path = os.getcwd()
        try:
            os.makedirs(path + "/" + OUTPUT_DIRECTORY +
                        Error+OrderNumber+" "+Subject)
        except OSError:
            print("Creation of the directory %s failed" %
                  path+"/" + OUTPUT_DIRECTORY+Error+"/"+Subject)
            print("Successfully created the directory %s " %
                  path+"/" + OUTPUT_DIRECTORY+Error+"/"+Subject)
        if("Re:" in Subject):
            print("This is a reply, not going to bother")
        else:
            LinkExtractor(EmailBody, OrderNumber,
                          OUTPUT_DIRECTORY, Subject, Error)
            f = open(OUTPUT_DIRECTORY+Error+OrderNumber+" " +
                     Subject + "/" + OrderNumber+" " + Subject+'.txt', 'wb')
            f.write(data[0][1])
            f.close()
        try:
            SchoolDataJson(OrderNumber, "School_Orders")
        except:
            print("JSON File Failed")
        try:
            os.mkdir(NetworkP)
        except:
            print("School Order Main Folder Creation Failed, Probbly Already Exsists")
        try:
            shutil.copytree(OUTPUT_DIRECTORY+OrderNumber+" "+Subject,
                            NetworkP + "/" + OrderNumber+" "+Subject)
        except:
            print("Sub Folder Copy Failed")
        EmailsProccessed += 1
    return EmailsProccessed


def main():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    rv, data = M.select(EMAIL_FOLDER)  # pylint: disable=unused-variable

    if rv == 'OK':
        print("Processing mailbox: ", EMAIL_FOLDER)
        print("Im Resting, Check Back Later:")
        while(1 == 1):
            try:
                time.sleep(420)
                print("Running Loop")
                M = imaplib.IMAP4_SSL(IMAP_SERVER)
                M.login(EMAIL_ACCOUNT, PASSWORD)
                rv, data = M.select(
                    EMAIL_FOLDER)  # pylint: disable=unused-variable
                EmailsP = process_mailbox(M)
                print("\n\n\n\n\n\n\n\n\n\n\n")
                print("Emails Proccessed: ", EmailsP)
                print("Im Resting, Check Back Later:")
                if rv == 'OK':
                    print("Again")
                else:
                    print("ERROR: Unable to open mailbox ", rv)
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
