# printer_processing
__version__ = "v20190928"

# Built-In Libraries
import os
import time
import subprocess

# Downloaded Libraries
import termcolor
import colorama 

# use Colorama to make Termcolor work on Windows too
colorama.init()


def print_status(ip):
    status = subprocess.Popen(["C:/Windows/SysNative/lpq.exe", "-S",
                               ip, "-P", "PS", "-l"], stdout=subprocess.PIPE, shell=True)
    (out, err) = status.communicate()  # pylint: disable=unused-variable
    out = out.splitlines()
    count = 0
    for line in out:
        if ":" in str(line):
            count += 1
    return count


def print_processor(print_que):
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
            print("Printed so Far: " + str(jobs_ran))
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
                    "C:/Windows/SysNative/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0]))
                print_que.pop(0)
                jobs_ran += 1
        else:
            print(termcolor.colored("\n!--PROCESSING CAUGHT UP--!:   ", "green"))
            run = False
            jobs_ran += 1
