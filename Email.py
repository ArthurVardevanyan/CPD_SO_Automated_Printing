#Source for email fetch https://gist.github.com/robulouski/7442321#file-gmail_imap_dump_eml-py
import sys
import imaplib
import getpass
from GDrive import GDownload
import os
import time
import shutil
import re

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = "@gmail.com"
EMAIL_FOLDER = "Inbox"
OUTPUT_DIRECTORY = 'School_Orders/'

PASSWORD = getpass.getpass()

def FileM(Order, OrderN, OUTPUT_DIRECTORY,Subjects, Error):
    Files = Order[0]
    if ("Attach your file(s) in PDF format." in Files):
        Files = str((Files.split("Number of Copies Needed per File", 1)).pop(1))
        #Files = str(Files.pop(1))
        Files = str((Files.split("Attach your file(s) in PDF format.", 1)).pop(0))
        #Files = str(Files.pop(0))
        Files = str((Files.split("File ")).pop(0))
        #Files.pop(0)

        for i in range(len(Files)):
            Files[i] = Files[i][2:].strip()
            Files[i] = Files[i].replace("3D", "", 1).replace("https://drive.google.com/open?id", "")
            Files[i] = re.sub(r'[\r\n\\:*?\"<>|.;=\]]', "", Files[i])
            print(Files[i])

        for y in Files:
            GDownload(y, OrderN, OUTPUT_DIRECTORY,Subjects,Error)
    else:
        print("This Isn't A School Order")


def process_mailbox(M):

    rv, data = M.search(None, 'UNSEEN')
    if rv != 'OK':
        print("No messages found!")
        return

    EmailsProccessed = 0
    for num in data[0].split():
        rv, data = M.fetch(num, '(UID BODY[TEXT])')
        SubjectF = M.fetch(num, '(UID BODY[HEADER.FIELDS (Subject)])')
        Subject = str(SubjectF[1][0][1])
        Subjects = Subject.replace("Subject: ", "").replace("Copy Job - ", "")
        Subjects = Subjects[:-9].strip()
        Subjects = Subjects[2:].strip()
        Subjects = re.sub(r'[/\r\n\\:*?\"<>|.;]', " ", Subjects)
        Subjects = Subjects.strip()
        Subjects = Subjects[:75] #Keeps only the First 75 Characters of the subject.
        OrderN = ""
        Order = str(data[0][1])
        Error = ""
        try:
            Order = Order.split("Order Number:", 1)
            OrderN = str(Order[1])
            OrderN = OrderN[:9].strip()
            OrderN = OrderN.replace("*", "")
            OrderN = OrderN.replace('\\r', "")
            OrderN = OrderN.replace("\\", "")
            OrderN = OrderN.replace(" ", "")
            Order.pop(0)
        except:
            print("This Email is Not Standard, Will Still Attempt to Download Files.")
            Error = "Error"


        if rv != 'OK':
            print ("ERROR getting message", num)
            return
        print ("Order: ", OrderN)
        path  = os.getcwd()
        if (Error == ""):
            try:
                os.makedirs(path+ "/" +OUTPUT_DIRECTORY+OrderN+" "+Subjects)
            except OSError:
                print ("Creation of the directory %s failed" % path+"/" +OUTPUT_DIRECTORY+OrderN+" "+Subjects)
                print ("Successfully created the directory %s " % path+"/" +OUTPUT_DIRECTORY+OrderN+" "+Subjects)

            if("Re:" in Subject):
                print("This is a reply, not going to bother")
            else:
                FileM(Order, OrderN,OUTPUT_DIRECTORY, Subjects, Error)
            f = open(OUTPUT_DIRECTORY+OrderN+" "+Subjects+"/" +OrderN+" "+Subjects+'.txt', 'wb')
            f.write(data[0][1])
            f.close()
        else:
            path  = os.getcwd()
            try:
                os.makedirs(path+ "/" +OUTPUT_DIRECTORY+Error+"/"+Subjects)
            except OSError:
                print ("Creation of the directory %s failed" % path+"/" +OUTPUT_DIRECTORY+Error+"/"+Subjects)
                print ("Successfully created the directory %s " % path+"/" +OUTPUT_DIRECTORY+Error+"/"+Subjects)
            if("Re:" in Subject):
                print("This is a reply, not going to bother")
            else:
                FileM(Order, OrderN,OUTPUT_DIRECTORY, Subjects, Error)
            f = open(OUTPUT_DIRECTORY+"/"+Error+"/"+Subjects+"/" +Subjects+'.txt', 'wb')
            f.write(data[0][1])
            f.close()
        EmailsProccessed +=1
        NetworkP = "P:/OneTimeJobs/School Orders"
        try:
            os.mkdir(NetworkP)
        except:
            print("School Order Main Folder Creation Failed, Probbly Already Exsists")
        try:
            shutil.copytree(OUTPUT_DIRECTORY+OrderN+" "+Subjects, NetworkP + "/" + OrderN+" "+Subjects)
        except:
            print("Sub Folder Copy Failed")


    return EmailsProccessed

def main():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    rv = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print ("Processing mailbox: ", EMAIL_FOLDER)
        while(1 == 1):
            try:
               print("Running Loop")
               M = imaplib.IMAP4_SSL(IMAP_SERVER)
               M.login(EMAIL_ACCOUNT, PASSWORD)
               rv = M.select(EMAIL_FOLDER)
               EmailsP = process_mailbox(M)
               print("\n\n\n\n\n\n\n\n\n\n\n")
               print("Emails Proccessed: ", EmailsP)
               print("Im Resting, Check Back Later:")
               time.sleep(420)

               if rv == 'OK':
                    print("Again")
               else:
                    print ("ERROR: Unable to open mailbox ", rv)
            except:
                print("SOMETHING WENT HORRIBLY WRONG, Check Internet Connection")
                continue
        M.logout()
        M.close()
    else:
        print ("ERROR: Unable to open mailbox ", rv)
    M.logout()

if __name__ == "__main__":
    main()
