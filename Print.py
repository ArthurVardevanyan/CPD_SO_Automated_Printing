import os
import glob
from PyPDF2 import PdfFileReader
from files import FolderList
from files import FilesList
from files import PostList
import json
from BannerSheet import bannerSheet
from PostScript import FileMerge
owd = os.getcwd()
owd = owd.replace("\\", "/")


def CanRun(JobInfo):

    if(JobInfo.get('Ran', False) == "True"):
        return False
    if(JobInfo.get('Paper', False) != "8.5 x 11 Paper White"):
        return False
    if(JobInfo.get('Stapling', False)):
        if(JobInfo.get('Stapling', False) != "Upper Left - portrait"):
            return False
    if(JobInfo.get('Front Cover', False)):
        return False
    if(JobInfo.get('Back Cover', False)):
        return False
    return True


def Printing(OrderNumber, folder, Confirmation, Printer):

    # This is the Order Name taken from the subject line.
    OName = "No Order Selected"
    Manual = ''
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = FolderList(folder)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i

    print(OName)
    if(OName == "No Order Selected"):
        print("Order Number is not Valid")
        return "ON Not Valid :  " + OrderNumber
    if(Confirmation == 1):
        if(int(input("Confirm Order Yes : 1 | No : 0 ")) == 0):
            return

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    Files = FilesList(folder, OName)

    with open(folder+'/'+OName+'/'+OName+'.json') as json_file:
        JobInfo = json.load(json_file)

    BannerFile = bannerSheet(JobInfo, folder+'/'+OName+'/')
    # This gets the number of pages for every pdf file for the job.
    for i in range(len(Files)):
        pdf = PdfFileReader(open(folder+'/'+OName+'/'+Files[i], "rb"))
        print("Page Count: " + str(pdf.getNumPages()) +
              " FileName: " + Files[i])

    if (CanRun(JobInfo)):
        print("\n!---This Job Is Semi-AutoRun Compatible---!")
        print('My Suggestions are as Follows:')
        if(JobInfo.get('Collation', False) == "Collated"):
            Collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print('Collated')
        else:
            Collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')
            print('UnCollated')
        if(JobInfo.get('Duplex', False) == "Two-sided (back to back)"):
            Duplex = str.encode(
                '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n')
            print('Double Sided')
        else:
            Duplex = str.encode(
                '@PJL XCPT <sides syntax="keyword">one-sided</sides>\n')
            print('Single Sided')
        if(JobInfo.get('Stapling', False) == "Upper Left - portrait"):
            Stapling = str.encode(
                '@PJL XCPT <value syntax="enum">20</value>\n')
            if str('<sheet-collate syntax="keyword">uncollated') in str(Collation):
                Collation = str.encode(
                    '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
                print("Collation Overide - Collated")
            print("Staple - Upper Left - portrait")
        else:
            Stapling = str.encode('')
        if(JobInfo.get('Drilling', False) == "Yes"):
            Punch = str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n')
            print('Hole Punched')
        else:
            Punch = str.encode('')
        if(JobInfo.get('Stapling', False) != "Upper Left - portrait" and JobInfo.get('Drilling', False) != "Yes"):
            default = str.encode('@PJL XCPT <value syntax="enum">3</value>\n')
            print('No Finishing')
        else:
            default = str.encode('')

        if(JobInfo.get('Special Instructions', False)):
            print("SPECIAL INSTRUCTIONS: " +
                  JobInfo.get('Special Instructions', False))
    else:
        print("This Order Currently Does not Support AutoSelection, please double chek if the order requires the normal driver.")
        return "Not Supported:  " + OName
    if(Printer == 0):
        LP = int(input("Choose a Printer: 156 (0), 162 (1): "))
    else:
        LP = 1
    print("\nNumber of (Total) Copies Listed Per File: " +
          JobInfo.get('Copies', False))
    if(JobInfo.get('Slip Sheets / Shrink Wrap', False)):
        print("SPECIAL INSTRUCTIONS: " +
              JobInfo.get('Slip Sheets / Shrink Wrap', False))
    if(JobInfo.get('Special Instructions', False) == False and JobInfo.get('Slip Sheets / Shrink Wrap', False) == False):
        Sets = 1
        CPS = int(JobInfo.get('Copies', False))
        print("!--I WILL TAKE IT FROM HERE--!")
        Manual = "SUCCESS!     :  "
    else:
        print("If more than one set is requried, do the appriate calculation to determine correct amount of Sets and Copies per Set")
        Sets = int(input("\nHow Many Sets?: "))
        CPS = int(input("How Many Copies Per Set?: "))
        Manual = "Manual Input :  "
    Copies_Command = str.encode(
        '@PJL XCPT <copies syntax="integer">'+str(CPS)+'</copies>\n')
    with open('PJL_Commands/PJL.ps', 'rb') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = Copies_Command
        if str('<value syntax="enum">3</value>') in str(lines[i]):
            lines[i] = default
            if str('<value syntax="enum">3</value>') not in str(default):
                lines.insert(i, Stapling)
                lines.insert(i+1, Punch)
        if str('<sheet-collate syntax="keyword">') in str(lines[i]):
            lines[i] = Collation
        if str('<sides syntax="keyword">one-sided</sides>') in str(lines[i]):
            lines[i] = Duplex
        if str('<sheet-collate syntax="keyword">uncollated') in str(Collation) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]):
            lines[i] = str.encode(
                '@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            lines.insert(i, str.encode(
                '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n'))

    with open('PJL_Commands/input.ps', 'wb') as f:
        for item in lines:
            f.write(item)
    Merged = False
    if str('<sheet-collate syntax="keyword">uncollated') in str(Collation) and len(JobInfo.get('Files', False)) != 1:
        Merged = True

    path = os.getcwd()  # Current Path
    try:
        os.makedirs(path + "/" + folder+"/"+OName + "/PSP")
        print("Successfully created the directory " + path +
              "/" + folder+"/"+OName + "/PSP")
    except OSError:
        print("Creation of the directory failed " + path +
              "/" + folder+"/"+OName + "/PSP")

    if Merged == True:
        filenames = ['PJL_Commands/input.ps', folder+"/" +
                     OName + "/"+OName+".ps", 'PJL_Commands/End.ps']
        with open(folder+"/"+OName + "/PSP/"+OName+".ps", 'wb') as outfile:
            for fname in filenames:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
    if Merged == False:

        for i in range(len(Files)):
            filenames = ['PJL_Commands/input.ps', folder+"/"+OName +
                         "/PostScript/"+Files[i]+".ps", 'PJL_Commands/End.ps']
            with open(folder+"/"+OName + "/PSP/"+Files[i][:-4]+".ps", 'wb') as outfile:
                for fname in filenames:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)

    Print_Files = PostList(folder, OName, "PSP")

    LPR = ["C:/Windows/SysNative/lpr.exe -S 10.56.54.156 -P PS ",
           "C:/Windows/SysNative/lpr.exe -S 10.56.54.162 -P PS "]

    try:
        os.remove("PJL_Commands/input.ps")
    except:
        print("Temp File Remove Failed")

    print(BannerFile)
    for i in range(Sets):
        for j in range(len(Print_Files)):
            print("File Name: " + Print_Files[j])

    LPRP = LPR[LP] + '"' + BannerFile + '"'
    print(LPRP)
    os.system(LPRP)
    np = owd + '/' + folder+'/' + OName + '/PSP'
    os.chdir(np)
    for i in range(Sets):
        for j in range(len(Print_Files)):
            LPRP = LPR[LP] + '"' + Print_Files[j] + '"'
            print(LPRP)
            os.system(LPRP)
    print("\n\n\n")
    return Manual + OName


os.chdir(owd)
print("Terminal AutoPrinting REV: 20190527")
print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests")
if(int(input("Bulk Order Printing?  Yes : 1 | No : 0 ")) != 1):
    loop = True
    while(loop):
        os.chdir(owd)
        print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests")
        Printing(str(input("Type In an Order Number: ")),
                 "School_Orders", 1, 0)
        if(int(input("Submit Another Order?  Yes : 1 | No : 0 ")) == 1):
            loop = True
        else:
            loop = False
            os.system('clear')  # on linux
            os.system('cls')  # on windows
else:
    print("Bulk Print Mode, Type Your Order Number and Hit Enter, \ntype run then enter when your all set.")
    print("Comaptible Jobs with no Special Instructions will AutoRun, if their are, jobs will pause for requested input if any")
    print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests")
    biggerloop = True
    while(biggerloop):
        loop = True
        OrderN = []
        Printed = []
        while(loop):
            temp = str(input("Type In an Order Number: "))
            if(temp != "run"):
                OrderN.append(temp)
            else:
                loop = False
                print("\nI am Going to Run:")
                print('\n'.join(map(str, OrderN)))
                for orders in OrderN:
                    os.chdir(owd)
                    Printed.append(
                        Printing(str(orders), "School_Orders", 0, 162))
                print("\n\n\n")
                print('\n'.join(map(str, Printed)))
                if(int(input("\n\n\nSubmit Another Set of Orders?  Yes : 1 | No : 0 ")) == 1):
                    biggerloop = True
                else:
                    biggerloop = False
                os.system('clear')  # on linux
                os.system('cls')  # on windows
