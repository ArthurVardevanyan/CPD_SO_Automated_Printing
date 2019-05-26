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


def Digit(numList):
    return int(''.join(str(i) for i in numList))
    # https://stackoverflow.com/questions/489999/convert-list-of-ints-to-one-number


def SuggestedPrinting(Collation, Duplex, Stapling, Punch):
    Code = Digit([Collation, Duplex, Stapling, Punch])

    InToOut = {
        2111: 0,
        2211: 1,
        2121: 2,
        2221: 3,
        2112: 4,
        2212: 5,
        2122: 6,
        2222: 7,
        0000: 8,
        1000: 9,
        1111: 10,
        1211: 11,
        2000: 12,
        3000: 13,
        1112: 14,
        1212: 15,

    }
    return InToOut.get(Code, None)


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
    print("\nPrinting Options:\n")
    for i in PO:
        print(i)

    if (CanRun(JobInfo)):
        print("\n!---This Job Is AutoRun Compatible---!")
        if(JobInfo.get('Duplex', False) == "Two-sided (back to back)"):
            Duplex = 2
        else:
            Duplex = 1
        if(JobInfo.get('Stapling', False) == "Upper Left - portrait"):
            Stapling = 2
        else:
            Stapling = 1
        if(JobInfo.get('Drilling', False) == "Yes"):
            Punch = 2
        else:
            Punch = 1
        if(JobInfo.get('Collation', False) == "Collated"):
            Collation = 2
        else:
            Collation = 1
        if(JobInfo.get('Collation', False) == "UnCollated"):
            return False
        try:
            print("I Suggest: " +
                  PO[SuggestedPrinting(Collation, Duplex, Stapling, Punch)])
        except:
            print(
                "ERROR: Something Doesn't add up with job specs, please check instruction sheet.")
        if(JobInfo.get('Special Instructions', False)):
            print("SPECIAL INSTRUCTIONS: " +
                  JobInfo.get('Special Instructions', False))
  
    PC = SuggestedPrinting(Collation, Duplex, Stapling, Punch) #int(input("\nChoose a Printing Option: "))
    LP = 1 # int(input("Choose a Printer: 156 (0), 162 (1): "))
    print("\nNumber of (Total) Copies Listed Per File: " +
          JobInfo.get('Copies', False))
    if(JobInfo.get('Slip Sheets / Shrink Wrap', False)):
        print("SPECIAL INSTRUCTIONS: " +
              JobInfo.get('Slip Sheets / Shrink Wrap', False))
    print("If more than one set is requried, do the appriate calculation to determine correct amount of Sets and Copies per Set")
    Sets = 1 #int(input("\nHow Many Sets?: "))
    CPS = int(JobInfo.get('Copies', False)) #int(input("How Many Copies Per Set?: "))
    Copies_Command = str.encode(
        '@PJL XCPT <copies syntax="integer">'+str(CPS)+'</copies>')
    with open('PJL_Commands/' + PO[PC], 'rb') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        #lines[i] = lines[i].rstrip()
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = Copies_Command

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
        with open(folder+"/"+OName + "/PSP/"+Files[i][:37]+".ps", 'wb') as outfile:
            for fname in filenames:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)

    Print_Files = PostList(folder, OName, "PSP")

    LPR = ["C:/Windows/SysNative/lpr.exe -S 10.56.54.156 -P PS ",
           "C:/Windows/SysNative/lpr.exe -S 10.56.54.162 -P PS "]

     
    print(BannerFile)
    for i in range(Sets):
        for j in range(len(Print_Files)):
            print("File Name: " + Print_Files[j])
    LPRP = LPR[LP] + '"' + BannerFile + '"'
    print(LPRP)
    np = owd+ '/'  + folder+'/' + OName + '/PSP'
    os.chdir(np)
    for i in range(Sets):
        for j in range(len(Print_Files)):
            LPRP = LPR[LP] + '"'+ Print_Files[j] + '"'
            print(LPRP)
            os.system(LPRP)

    os.chdir(owd)
