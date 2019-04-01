import os
import glob
from PyPDF2 import PdfFileReader



folder = "School Orders"

def FolderList(folder):
    # Grabs the Files (Contains the Date Modifer metedata as well)

    fileList = glob.glob(folder+"/*")  # Gathers all the Files
    # fileList.sort(key=os.path.getmtime)  # Sorts Oldset to Newest
    # Strips the file path data to leave just the filename
    # Strip filepath to filename.
    Stripped_List = [os.path.basename(x) for x in fileList]

    return Stripped_List  # Returns the Stripped List to Main Function



def FilesList(folder, OName):
    # Grabs the Files (Contains the Date Modifer metedata as well)

    fileList = glob.glob(folder+"/"+OName+"/*.pdf")  # Gathers all the Files
    # fileList.sort(key=os.path.getmtime)  # Sorts Oldset to Newest
    # Strips the file path data to leave just the filename
    # Strip filepath to filename.
    Stripped_List = [os.path.basename(x) for x in fileList]

    return Stripped_List  # Returns the Stripped List to Main Function

def main():
while(True):
    ONumber = str(input("Type In an Order Number: "))
    # Some Input Validation Goes Here.
    OName = " "
    Folders = FolderList(folder)
    #print(*Folders,sep = "\n")
    for i in Folders:
        if ONumber in i:
            OName = i
    print(OName)
    Files = FilesList(folder, OName)
    for files in Files:
        pdf = PdfFileReader(open(folder+'/'+OName+'/'+files, "rb"))
        print("Page Count: " + str(pdf.getNumPages()) + " File Name: " + files)

    Duplex = int(input("Duplex Yes (1) No (0): "))
    HP = int(input("Hole Punch Yes (1) No (0): "))
    S = int(input("Staple Yes (1) No (0): "))
    TotalQTY = int(input("Type In The Total Number of Copies: "))
    QTY = int(input("Type In The Number of Copies Per Set: "))
    SETS = int(input("Type In The Number of Sets: "))


    sides = ["", "-o sides=two-sided-long-edge"]
    punch = ["", "-o XRPunchOption=3Punch"]
    staple = ["", "-o XRStapleOption=SinglePortrait"]
    QTYA = []

    if(TotalQTY == QTY*SETS):
        for i in range(SETS):
            QTYA.append(QTY)
    else:
        QTYA.append(QTY)
        for i in range(SETS-1):
            if(TotalQTY-QTY > 0):
                TotalQTY = TotalQTY-QTY
                QTYA.append(TotalQTY)
            else:
                QTYA.append(TotalQTY)

    for i in range(SETS):
        for files in Files:
            print('lpr -#'+str(QTYA[i])+' '+staple[S]+ ' ' +punch[HP]+ ' '+sides[Duplex]+ ' "'+folder+'/'+OName+'/'+files+'"')

    Proof = int(input("\nSetup Look Good? (1): "))
    if Proof ==1 :
        for i in range(SETS):
            for files in Files:
                os.system('lpr -#'+str(QTYA[i])+' '+staple[S]+ ' ' +punch[HP]+ ' '+sides[Duplex]+ ' "'+folder+'/'+OName+'/'+files+'"')


    else:
        continue

    Run = int(input("\nRun Another Order? (1) or Exit (0): "))
    if Proof ==1:
        continue
    else:
        exit()

if __name__ == "__main__":
    main()
