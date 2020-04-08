# printer_processing
__version__ = "v20200302"
# Built-In Libraries
import os
import time
import subprocess
# Downloaded Libraries
import termcolor
import colorama
import database
from datetime import datetime
import log
print = log.Print
input = log.Input
# use Colorama to make Termcolor work on Windows too
colorama.init()


def print_status(ip):
    status = subprocess.Popen(["C:/Windows/system32/lpq.exe", "-S",
                               ip, "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
    (out, err) = status.communicate()  # pylint: disable=unused-variable
    out = out.splitlines()
    count = 0
    for line in out:
        if ":" in str(line):
            count += 1
    return count


def order_status():
    finishedOrders = []
    try:
        P162 = False
        P156 = False
        orders = database.printingOrders()
        for order in orders:
            if order[1] == "162":
                P162 = True
            if order[1] == "156":
                P156 = True
        orderStatus = ""
        if(P162 and P156):
            status = subprocess.Popen(["C:/Windows/system32/lpq.exe", "-S",
                                       "10.56.54.162", "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
            (orderStatus1, err) = status.communicate(
            )  # pylint: disable=unused-variable
            status1 = subprocess.Popen(["C:/Windows/system32/lpq.exe", "-S",
                                        "10.56.54.156", "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
            (orderStatus2, err) = status1.communicate(
            )  # pylint: disable=unused-variable
            orderStatus = str(orderStatus1) + str(orderStatus2)
        elif(P162):
            status = subprocess.Popen(["C:/Windows/system32/lpq.exe", "-S",
                                       "10.56.54.162", "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
            (orderStatus, err) = status.communicate(
            )  # pylint: disable=unused-variable
        elif(P156):
            status = subprocess.Popen(["C:/Windows/system32/lpq.exe", "-S",
                                       "10.56.54.156", "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
            (orderStatus, err) = status.communicate(
            )  # pylint: disable=unused-variable
        for order in orders:
            if(str(order[0]) not in str(orderStatus)):
                finishedOrders.append(order)
    except:
        print("Printer Order Status Failed")
    try:
        for order in finishedOrders:
            change = "Printed_" + str(datetime.now().strftime("%Y%m%d:%H%M"))
            database.print_status(order[0], change)
    except:
        log.logger.exception("")
        print("Database Update Failed")


def print_processor(print_que, orders=[]):
    # Runs through the list of files to send to the printers, pausing for input as needed.
    print(termcolor.colored("!--DO NOT CLOSE--!", "red"))
    print(len(print_que))
    ID_LIMIT = 40
    run = True
    jobs_ran = 0
    while run:
        Q_Jobs = 0
        if len(print_que) > 0:
            if "10.56.54.162" in print_que[0]:
                Q_Jobs = print_status("10.56.54.162")
            else:
                Q_Jobs = print_status("10.56.54.156")
        if Q_Jobs >= ID_LIMIT:
            print("Printed so Far: ", str(jobs_ran))
            print("Waiting For Jobs to Clear Up")
            # input(
            #    "Please Confirm Printers Will Support 40 More Job IDS before pressing enter: ")
            jobs_ran = 0
            time.sleep(100)
            continue
        if len(print_que) > 0:
            if("banner" not in print_que[0]):
                os.system(print_que[0])
                print((str(print_que[0]).replace(
                    "C:/Windows/system32/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0]))
                for q in print_que:
                    for order in orders:
                        if order[0] in q:
                            database.print_status(order[0], str(order[1]))
                print_que.pop(0)
                jobs_ran += 1
        else:
            print(termcolor.colored("\n!--PROCESSING CAUGHT UP--!:   ", "green"))
            run = False
            jobs_ran += 1


def main():
    log.logInit("Status")
    from log import logger
    print = log.Print
    input = log.Input
    order_status()


if __name__ == "__main__":
    main()
