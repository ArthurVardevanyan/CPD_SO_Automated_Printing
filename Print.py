import os
import glob
from PyPDF2 import PdfFileReader
from files import FolderList
from files import FilesList
from files import PostList
import json
def CanRun(JobInfo):
    
    JobInfo.get('ront Cover', False)
    if(JobInfo.get('Ran', False) == "True"):
        return False
    if(JobInfo.get('Collation', False) == "UnCollated"):
        return False
    if(JobInfo.get('Special Instructions', False)):
        return False
    if(JobInfo.get('Stapling', False) == "Double Left - portrait"):
        return False
    if(JobInfo.get('Front Cover', False)):
        return False
    if(JobInfo.get('Back Cover', False)):
        return False
    return True

    


def Printing(OrderNumber, folder):

    OName = " "  # This is the Order Name taken from the subject line.
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = FolderList(folder)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    Files = FilesList(folder, OName)


    with open(folder+'/'+OName+'/'+OName+'.json') as json_file:  
        JobInfo = json.load(json_file)



    # This gets the number of pages for every pdf file for the job.
    for i in range(len(Files)):
        pdf = PdfFileReader(open(folder+'/'+OName+'/'+Files[i], "rb"))
        print("File Name:" + Files[i] +
              " Page Count: " + str(pdf.getNumPages()))

    PO = ['00 Normal.ps',
          '01 Duplex.ps',
          '02 SS Staple.ps',
          '03 DS Staple.ps',
          '04 SS Punch.ps',
          '05 DS Punch.ps',
          '06 SS Staple Punch.ps',
          '07 DS Staple Punch.ps',
          '08 SS Slipt Collated.ps',
          '09 DS Slipt Collated.ps',
          '10 SS Slipt Uncollated.ps',
          '11 DS Slipt Uncollated.ps',
          '12 SS Slipt Punch Collated.ps',
          '13 DS Slipt Punch Collated.ps',
          '14 SS Slipt Punch Uncollated.ps',
          '15 DS Slipt Punch Uncollated.ps',
          ]

    if (CanRun(JobInfo)):
        print("We are a go for AutoRun in The Future....!...")

    print("\nPrinting Options:\n")
    for i in PO:
        print(i)
    PC = int(input("\nChoose a Printing Option: "))
    LP = int(input("\nChoose a Printer: 156 (0), 162 (1): "))
    Sets = int(input("\nHow Many Sets?: "))
    CPS = int(input("\nHow Many Copies Per Set?: "))
    Copies_Command = str(
        '@PJL XCPT 		<copies syntax="integer">'+str(CPS)+'</copies>')
    with open('PJL_Commands/' + PO[PC]) as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = Copies_Command

    with open('PJL_Commands/input.ps', 'w') as f:
        for item in lines:
            f.write("%s\n" % item)

    path = os.getcwd()  # Current Path
    try:
        os.makedirs(path + "/" + folder+"/"+OName + "/PostScript_Print")
        print("Successfully created the directory " + path +
              "/" + folder+"/"+OName + "/PostScript_Print")
    except OSError:
        print("Creation of the directory failed " + path +
              "/" + folder+"/"+OName + "/PostScript_Print")

    for i in range(len(Files)):
        filenames = ['PJL_Commands/input.ps', folder+"/"+OName +
                     "/PostScript/"+Files[i]+".ps", 'PJL_Commands/End.ps']
        with open(folder+"/"+OName + "/PostScript_Print/"+Files[i]+".ps", 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    Print_Files = PostList(folder, OName, "PostScript_Print")

    LPR = ["lpr -S 10.56.54.156 -P PS ", "lpr -S 10.56.54.162 -P PS "]


    for i in range(Sets):
        for j in range(len(Print_Files)):
            print("File Name:" + Print_Files[j])
    for i in range(Sets):
        for j in range(len(Print_Files)):
            print(LPR[LP] + Print_Files[j])
            
            

print("REV: 20190517")
Printing(str(input("Type In an Order Number: ")), "School_Orders")

