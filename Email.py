# Email.py
__version__ = "v20200718"
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
import integrity
import Print
import EmailPrint
import order as o
import log
# use Colorama to make Termcolor work on Windows too
colorama.init()


def subject_line(subject):
    """
    Cleans up the subject line from the current email.

    The subject line contains unnecessary information that is removed.
    In addition, charcaters that may pose a problem for windows are also removed.

    Parameters: 
        subject (string): The subject line to be cleaned up.

    Returns: 
        string: The cleaned up subject line.
    """
    subject = str(subject[1][0][1]).replace(
        "Subject: ", "").replace("Copy Job - ", "")
    subject = subject[2:-9].strip()
    subject = re.sub(r'[/\r\n\\:*?\"()<>|.;]', " ", subject)
    subject = subject.replace("&", "and")
    # Keeps only the First 35 Characters of the subject.
    subject = subject[:35].rstrip()
    return subject


def order_number_random():
    """
    Generators a "random" order number.

    Customer occasionally supplies duplicate order numbers.
    This appends the minutes & seconds to the end of the order number.
    This sufficiently resolves the duplicate order number issue.

    Parameters: 
        N/A

    Returns: 
        string: A String containing a hyphen and the current time in -MMSS.
    """
    time = datetime.datetime.today().strftime('%M%S')
    return "".join(["-", time])


def order_number_extract(email_body, RANDOM):
    """
    Extract the order number from the body of the email.

    If the order number cannot be determined, or does not exist, 
    a non fatal error flag is thrown and the contents of the email 
    will still be saved but moved to another folder.
    This occurs usually when a email is received that isn't actually an order.

    Parameters: 
        email_body  (str): The body of the email.
        random      (str): "Random" number to append to the end of the order number.

    Returns: 
        string: The order number
        string: The error state
    """
    try:  # Checks if Email is Indeed A School Order, Strips Unwanted Information
        email_body = email_body.split("Order Number:", 1)
        ORDER_NUMBER = str(email_body[1])
        ORDER_NUMBER = ORDER_NUMBER[:9].strip()
        ORDER_NUMBER = ORDER_NUMBER.replace('\\r', "").replace(" ", "")
        ORDER_NUMBER = re.sub(r'[\\*]', "", ORDER_NUMBER)
        # Adds some randomness to the order number's using time
        return "".join([ORDER_NUMBER, RANDOM]), ""
    except:
        logger.exception("")
        print("This Email is Not Standard, Will Still Attempt to Download Files.")
        error_state = "Error/"
        return "", error_state


def autorun(AUTORUN, order):
    """
    Automatically attempts to run an order.

    Used mostly for show, however this does work in production.
    High order loads will be to tougher for human operators to keep up with the printers.
    Orders that can be automatically run get ran.
    Orders that can not be automatically ran, get only the ticket printed, 
    to a separate tray on the printer.

    Parameters: 
        AUTORUN (bool)  : The flag for wether to autorun or not.
        order   (object): The object containing all the information for the current order.

    Returns: 
        bool: Unused return.
    """
    if(AUTORUN):
        import files
        import printer
        COLOR = 0
        BOOKLETS = 0
        EMAILPRINT = True
        print_que = []
        Orders = []
        Print.printing(Orders, order.NUMBER, "SO", D110_IP, COLOR,
                       print_que, AUTORUN, EMAILPRINT, BOOKLETS)
        printer.print_processor(print_que)
        files.file_cleanup(Orders, order.OD)
    return 1


def process_mailbox(M, AUTORUN, D110_IP):
    """
    Checks the Gmail account for new emails and proceeds to operate on all unread emails.

    All the operations that prep an order to be run later are here or called from here.
    This function is main the sequel.

    Parameters: 
        M       (object): The Gmail connection object.
        AUTORUN (bool)  : The flag for wether to autorun or not.
        D110_IP (int)   : Which IP to use form the LPR list.

    Returns: 
        int: The number of emails the are processed. 
    """
    # Gets all the UNSEEN emails from the INBOX
    rv, data = M.search(None, 'UNSEEN')
    # '(SINCE "01-Jan-2012" BEFORE "02-Jan-2012")',  'UNSEEN'
    # https://stackoverflow.com/questions/5621341/search-before-after-with-pythons-imaplib
    if rv != 'OK':
        print("No messages found!")
        return
    emails_proccessed = 0
    for num in data[0].split():
        order = o.Order()
        order.OD = 'SO/'
        rv, data = M.fetch(num, '(UID BODY[TEXT])')  # Email Body
        # Email Subject

        order.SUBJECT = subject_line(
            M.fetch(num, '(UID BODY[HEADER.FIELDS (Subject)])'))
        email_body = data[0][1]
        order.NUMBER, error_state, = order_number_extract(
            str(email_body), order_number_random())
        print("Order: ", order.NUMBER + " ", order.SUBJECT)
        order.NAME = "".join([order.NUMBER, " ", order.SUBJECT])
        if rv != 'OK':
            print("ERROR getting message", num)
            return
        F = "".join([order.OD,
                     error_state, order.NAME])
        try:
            if not os.path.exists(F):
                os.makedirs(F)
        except OSError:
            print("".join(["Creation of the directory failed" %
                           order.OD, error_state, "/", order.SUBJECT]))
        print("".join(["Successfully created the directory %s " %
                       order.OD, error_state, "/", order.SUBJECT]))
        if("Re:" in order.SUBJECT):  # Ignore Replies
            print("This is a reply, skipping")
        else:
            # Makes a file and Writes Email Contents to it.
            f = open("".join([order.OD, error_state,
                              order.NAME, "/", order.NAME, '.txt']), 'wb')
            f.write(email_body)
            f.close()
            # Calls Google Drive Link Extractor
        order = o.process_Email(order, email_body, error_state)
        emails_proccessed += 1
        autorun(AUTORUN, order)
    return emails_proccessed


def main(AUTORUN, D110_IP):
    """
    Preps the connection to the Gmail account, as well as runs the loop to check for new orders.

    Parameters: 
        AUTORUN (bool)  : The flag for wether to autorun or not.
        D110_IP (int)   : Which IP to use form the LPR list.

    Returns: 
        N/A
    """
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
        logger.exception("")
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
                logger.exception("")
                print("SOMETHING WENT HORRIBLY WRONG, Check Internet Connection")
                time.sleep(30)
                continue
        M.logout()
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)
    M.logout()


if __name__ == "__main__":
    if (datetime.datetime.today().date() > datetime.datetime.strptime(log.license, "%Y%m%d").date()):
        exit()
    log.logInit("Email")
    from log import logger
    print = log.Print
    input = log.Input
    print("\nSchool Order Downloader REV:",
          colored(__version__, "magenta"))
    print("Terminal Auto Printing  REV:",
          colored(Print.__version__, "magenta"))
    print("Terminal Email Printing REV:",
          colored(EmailPrint.__version__, "magenta"))
    print("\n")
    integrity.integrity()
    try:
        # Creates the Directory for Output
        if not os.path.exists("SO/"):
            os.makedirs("SO/")
    except OSError:
        print("Creation of the Order directory failed")
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
                        logger.exception("")
                        pass
            break
        except:
            logger.exception("")
            pass
    main(AUTORUN, D110_IP)
