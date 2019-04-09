import json
import os
import glob
from PyPDF2 import PdfFileReader
from files import FolderList 
from files import FilesList



def SchoolDataJson(ONumber, folder):
    SchoolData = {'Account ID':'CHANGEME'}
    OName = " "
    Folders = FolderList(folder)
    #print(*Folders,sep = "\n")
    for i in Folders:
        if ONumber in i:
            OName = i
    Files = FilesList(folder, OName)

    SchoolData["Order Number"] = ONumber
    SchoolData["Order Subject"] = OName[5:]
    SchoolData["Files"] = {}
    
    for i in range(len(Files)):
        pdf = PdfFileReader(open(folder+'/'+OName+'/'+Files[i], "rb"))
        SchoolData["Files"]["File "+ str(i+1)] = {"File Name":Files[i],  "Page Count":str(pdf.getNumPages())}
                    
    Email = [line.rstrip('\n') for line in open(folder+'/'+OName+'/'+OName+".txt", "r")]
    
    for i in range(len(Email)):
        if "IF YOU HAVE ANY QUESTIONS" in Email[i]:
            Email = Email[10:-(len(Email)-i)]
            break


    for lines in Email:
        TestString = "*Timestamp: *"
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Date Orded"] = line[1]
        TestString = "Email address "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Email"] = line[1]
        TestString = "Your Last Name "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Last Name"] = line[1]
        TestString = "Your First Name "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["First Name"] = line[1]
        TestString = "Your Call Back Number "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Phone Number"] = line[1]
        TestString = "Your building "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Building"] = line[1]
        TestString = "Number of Copies Needed per File "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Copies"] = line[1]
        TestString = "Printing Setup "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Duplex"] = line[1]
        TestString = "Collated or Uncollated "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Collation"] = line[1]
        TestString = "Paper Size, Type, and Color "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Paper"] = line[1]
        TestString = "Stapling "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Stapling"] = line[1]
        TestString = "Drilling - Three Hole Punch "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Drilling"] = line[1]
        TestString = "Slip Sheets and/or Shrink Wrap "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Slip Sheets / Shrink Wrap"] = line[1]
        TestString = "Special Instructions "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Special Instructions"] = line[1]
        TestString = "Booklet Fold and Staple "
        if  TestString in lines:
            line = lines.split(TestString)
            SchoolData["Booklets"] = line[1]
        TestString = "Deliver To: "
        if  TestString in lines:
            TestString = "Deliver to: (Staff Member's Name) "
            if  TestString in lines:
                line = lines.split(TestString)
                SchoolData["Deliver To Address"] = line[1]
            else:    
                TestString = "Deliver To: "
                line = lines.split(TestString)
                SchoolData["Deliver To Name"] = line[1]
       

    with open(folder+'/'+OName+'/'+OName+'.json', 'w') as outfile:
        json.dump(SchoolData, outfile, indent=4, separators=(',', ': '))
