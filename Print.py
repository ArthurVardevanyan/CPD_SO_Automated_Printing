import os
import glob
from PyPDF2 import PdfFileReader
from files import FolderList
from files import FilesList


def Printing(OrderNumber, folder):

    OName = " "  # This is the Order Name taken from the subject line.
    # Calls a function in files.py, which gets a list of all the orders downladed
    Folders = FolderList(folder)
    for i in Folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if OrderNumber in i:
            OName = i

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    Files = FilesList(folder, OName)

    # This gets the number of pages for every pdf file for the job.
    for i in range(len(Files)):
        pdf = PdfFileReader(open(folder+'/'+OName+'/'+Files[i], "rb"))
        print("File Name:" + Files[i] +
              "Page Count: " + str(pdf.getNumPages()))

    PO = ['00 Normal.ps',
          '01 Duplex.ps',
          '02 SS Staple.ps',
          '03 DS Staple.ps',
          '04 SS Punch.ps',
          '05 DS Punch.ps',
          '06 SS Staple Punch.ps',
          '07 DS Staple Punch.ps',
          '08 SS Slipt.ps',
          '09 DS Slipt.ps',
          '10 SS Slipt Punch Uncollated.ps',
          '11 DS Slipt Punch Uncollated.ps',
          '13 SS Slipt Punch Collated.ps',
          '14 DS Slipt Punch Collated.ps',
          ]

    print("\nPrinting Options:\n")
    for i in PO:
        print(i)
    PC = int(input("\nChoose a Printing Option: "))
    Sets = int(input("\nHow Many Sets?: "))
    CPS = int(input("\nHow Many Copies Per Set?: "))
    Copies_Command = str('@PJL XCPT 		<copies syntax="integer">'+str(CPS)+'</copies>'  )
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
        os.makedirs(path + "/" +folder+"/"+OName+ "/PostScript_Print")
        print("Successfully created the directory " +path + "/" +folder+"/"+OName+ "/PostScript_Print")
    except OSError:
        print("Creation of the directory failed " + path + "/" +folder+"/"+OName+ "/PostScript_Print")

    for i in range(len(Files)):
        filenames = ['PJL_Commands/input.ps', folder+"/"+OName+ "/PostScript/"+Files[i]+".ps", 'PJL_Commands/End.ps']
        with open(folder+"/"+OName+ "/PostScript_Print/"+Files[i]+".ps", 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                 for line in infile:
                        outfile.write(line)






Printing(str(input("Type In an Order Number: ")), "School_Orders")
