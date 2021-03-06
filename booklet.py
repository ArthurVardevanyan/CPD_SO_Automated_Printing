# booklet.py
__version__ = "v20200801"

from termcolor import colored
import colorama
import printer
import instructions


def bookletPrint(log, order, print_que, Print_Files, SETS, LPR, D110_IP, MERGED):
    """
    Logic & workflow for printing saddle-stitched booklets.

    Saddle-stitched bookelts require a differnet workflow.
    Booklets also require extra validation before running.
    Booklets also only get ran one-set at a time. 
    This can handle that.

    Parameters: 
        log         (object): The object that allows the software to log itself.
        order       (object): The object containing all the information for the current order.
        print_que   (list)  : The list of print ready files waiting to be run. (Used when Bulk Printing)
        Print_Files (list)  : The location of all the postscript files for the current job.
        SETS        (int)   : How many sets to run.
        LPR         (list)  : The front portion of the LPR command for each printer.
        D110_IP     (int)   : Which IP to use form the LPR list.
        MERGED      (bool)  : The flag for knowing if all the files are merged together.
                        

    Returns: 
        N/A
    """
    approved = 0
    COPIES_PER_SET = 0
    print("Enter How Many Sets and Copies Per Set You Would Like to Run.\nEnter 1 + Copy Count if you want to run everything at once.")
    while True:
        try:
            SETS = int(input("\nHow Many Sets?: "))
            break
        except:
            log.logger.exception("")
            pass
    while True:
        try:
            COPIES_PER_SET = int(input("How Many Copies Per Set?: "))
            break
        except:
            log.logger.exception("")
            pass

    for j in range(len(Print_Files)):
        lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
        lpr_path = LPR[D110_IP] + '"' + order.OD+'/' + order.NAME + '/PSP/' + \
            Print_Files[j] + '" -J "' + Print_Files[j] + '"'
        log.logger.debug((lpr_path.replace(
            "C:/Windows/system32/lpr.exe -S 10.56.54.", "").replace(
            '-P PS "C:/S/SO/', "").split("-J")[0]))
        print_que.append(lpr_path)
    printer.print_processor(print_que)  # Does the printing
    print("PLEASE CHECK PROOF, if any files look incorrect, please cancel order")
    loop = True
    flip = []
    while loop:
        try:
            approved = int(input(''.join(["Flip All & Proof?: ", colored("1", "cyan"), " | Flip Individually & Proof?: ", colored(
                "2", "cyan"),  " | Approved?  Yes: ", colored(
                "3", "cyan"), " | No: ", colored("0", "cyan"), " :"])))
        except:
            log.logger.exception("")
            pass
        if(approved == 3):
            if (len(flip) == 0):
                instructions.pjl_insert(
                    order, COPIES_PER_SET)
                instructions.pjl_merge(order,
                                       "PSP", MERGED, order.FILE_NAMES)
            else:
                for j in range(len(Print_Files)):
                    order.DUPLEX = "two-sided-short-edge" if flip[j] else "Two-sided (back to back)"
                    instructions.pjl_insert(
                        order, COPIES_PER_SET)
                    flip_file = [order.FILE_NAMES[j]]
                    instructions.pjl_merge(order, "PSP",
                                           MERGED, flip_file)
            for i in range(SETS):
                print("\n\nRunning Set " + str(i+1) + " of " + str(SETS))
                for j in range(len(Print_Files)):
                    lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                    lpr_path = LPR[D110_IP] + '"' + order.OD+'/' + order.NAME + \
                        '/PSP/' + Print_Files[j] + \
                        '" -J "' + Print_Files[j] + '"'
                    log.logger.debug((lpr_path.replace(
                        "C:/Windows/system32/lpr.exe -S 10.56.54.", "").replace(
                        '-P PS "C:/S/SO/', "").split("-J")[0]))
                    print_que.append(lpr_path)
                printer.print_processor(print_que)  # Does the printing
                print("Ran Set " + str(i+1) + " of " + str(SETS))
                if(SETS != 1):
                    str(input("\nPress Enter to Continue: "))
            loop = False
        elif(approved == 1):
            order.DUPLEX = "two-sided-short-edge"
            instructions.pjl_insert(
                order, 1)
            instructions.pjl_merge(order, "PSP", MERGED, order.FILE_NAMES)
            for j in range(len(Print_Files)):
                lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                lpr_path = LPR[D110_IP] + '"' + order.OD+'/' + order.NAME + '/PSP/' + \
                    Print_Files[j] + '" -J "' + Print_Files[j] + '"'
                log.logger.debug((lpr_path.replace(
                    "C:/Windows/system32/lpr.exe -S 10.56.54.", "").replace(
                    '-P PS "C:/S/SO/', "").split("-J")[0]))
                print_que.append(lpr_path)
            printer.print_processor(print_que)  # Does the printing
        elif(approved == 2):
            for j in range(len(Print_Files)):
                while True:
                    try:
                        flipT = int(input(''.join(["File: ", str(j+1), ": Flip?  Yes: ", colored(
                            "1", "cyan"), " No: ", colored("0", "cyan"), " : "])))
                        if(flipT == 1 or flipT == 0):
                            flip.append(flipT)
                            break
                        else:
                            pass
                    except:
                        log.logger.exception("")
                        pass
                order.DUPLEX = "two-sided-short-edge" if flip[-1] else "Two-sided (back to back)"
                instructions.pjl_insert(
                    order, 1)
                flip_file = [order.FILE_NAMES[j]]
                instructions.pjl_merge(order,
                                       "PSP", MERGED, flip_file)
                lpr_path = LPR[D110_IP] + '"' + Print_Files[j] + '"'
                lpr_path = LPR[D110_IP] + '"' + order.OD+'/' + order.NAME + '/PSP/' + \
                    Print_Files[j] + '" -J "' + Print_Files[j] + '"'
                print_que.append(lpr_path)
            printer.print_processor(print_que)  # Does the printing
        elif(approved == 0):
            loop = False
