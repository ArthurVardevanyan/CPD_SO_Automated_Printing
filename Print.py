import os
import glob
from PyPDF2 import PdfFileReader
from files import FolderList
from files import FilesList
from files import PostList
import json
from BannerSheet import bannerSheet
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


def Printing(OrderNumber, folder):

    # This is the Order Name taken from the subject line.
    OName = "No Order Selected"
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = FolderList(folder)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i

    print(OName)
    if(OName == "No Order Selected"):
        print("Order Number is not Valid")
        return
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
        print("\n!---This Job Is AutoRun Compatible---!")
        print('My Suggestions are as Follows:')
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
            print("Staple - Upper Left - portrait")
        else:
            Stapling = str.encode('')
        if(JobInfo.get('Drilling', False) == "Yes"):
            Punch = str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n')
            print('Hole Punched')
        else:
            Punch = str.encode('')
        if(JobInfo.get('Collation', False) == "Collated"):
            Collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print('Collated')
        else:
            Collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')
            print('UnCollated')
        if(JobInfo.get('Stapling', False) != "Upper Left - portrait" and JobInfo.get('Drilling', False) != "Yes"):
            default = str.encode('@PJL XCPT <value syntax="enum">3</value>\n')
            print('No Finishing')
        else:
            default = str.encode('')

        if(JobInfo.get('Special Instructions', False)):
            print("SPECIAL INSTRUCTIONS: " +
                  JobInfo.get('Special Instructions', False))
    else:
        if(int(input("\nThis Order Currently Does not Support AutoSelection, please double chek if the order requires the normal driver. Continue : 1 | Exit : 0 ") != 1)):
            return

    LP = int(input("Choose a Printer: 156 (0), 162 (1): "))
    print("\nNumber of (Total) Copies Listed Per File: " +
          JobInfo.get('Copies', False))
    if(JobInfo.get('Slip Sheets / Shrink Wrap', False)):
        print("SPECIAL INSTRUCTIONS: " +
              JobInfo.get('Slip Sheets / Shrink Wrap', False))
    print("If more than one set is requried, do the appriate calculation to determine correct amount of Sets and Copies per Set")
    Sets = int(input("\nHow Many Sets?: "))
    CPS = int(input("How Many Copies Per Set?: "))
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

    with open('PJL_Commands/input.ps', 'wb') as f:
        for item in lines:
            f.write(item)

    path = os.getcwd()  # Current Path
    try:
        os.makedirs(path + "/" + folder+"/"+OName + "/PSP")
        print("Successfully created the directory " + path +
              "/" + folder+"/"+OName + "/PSP")
    except OSError:
        print("Creation of the directory failed " + path +
              "/" + folder+"/"+OName + "/PSP")

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


loop = True
while(loop):
    os.chdir(owd)
    print("Terminal AutoPrinting REV: 20190526")
    print("ALWAYS Skim Outputs, Page Counts, etc, for Invalid Teacher Input or Invalid Requests")
    Printing(str(input("Type In an Order Number: ")), "School_Orders")

    if(int(input("Submit Another Order?  Yes : 1 | No : 0 ")) == 1):
        loop = True
    else:
        loop = False
    # os.system('clear') # on linux
    os.system('cls')  # on windows
