# SchoolDataJson.py
__version__ = "v20190815"

# Built-In Libraries
import json
import os
import glob

# Downloaded Libraries
from PyPDF2 import PdfFileReader

# Local Files
from files import folder_list
from files import file_list


def school_data_json(ORDER_NUMBER, subject, OUTPUT_DIRECTORY):
    school_data = {'Account ID': 'CHANGE ME'}
    
    ORDER_NAME = ORDER_NUMBER + " " + subject

    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    files = file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    school_data["Order Number"] = ORDER_NUMBER
    school_data["Order Subject"] = ORDER_NAME[5:]
    school_data["Files"] = {}

    # This gets the number of pages for every pdf file for the job.
    for i in range(len(files)):
        pdf = PdfFileReader(
            open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+files[i], "rb"))
        school_data["Files"]["File " +
                             str(i+1)] = {"File Name": files[i],  "Page Count": str(pdf.getNumPages())}

    # Imports the Email contents line by line.
    email = [line.rstrip('\n') for line in open(
        OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+".txt", "r")]

    # Removes the duplicate portion of the email that contains html (form) code.
    for i in range(len(email)):
        if "IF YOU HAVE ANY QUESTIONS" in email[i]:
            email = email[10:-(len(email)-i)]
            break

            # Searchs for required elements from the form for the JSON file.
    for lines in email:
        test_string = "*Timestamp: *"
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Date Ordered"] = line[1]
        test_string = "Email address "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Email"] = line[1]
        test_string = "Your Last Name "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Last Name"] = line[1]
        test_string = "Your First Name "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["First Name"] = line[1]
        test_string = "Your Call Back Number "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Phone Number"] = line[1]
        test_string = "Your building "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Building"] = line[1]
        test_string = "Number of Copies Needed per File "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Copies"] = line[1]
        test_string = "Printing Setup "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Duplex"] = line[1]
        test_string = "Collated or Uncollated "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Collation"] = line[1]
        test_string = "Paper Size, Type, and Color "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Paper"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Stapling "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Stapling"] = line[1]
        test_string = "Drilling - Three Hole Punch "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Drilling"] = line[1]
        test_string = "Folding "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Folding"] = line[1]
        test_string = "Cutting "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Cutting"] = line[1]
        test_string = "Slip Sheets and/or Shrink Wrap "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Slip Sheets / Shrink Wrap"] = line[1]
        test_string = "Special Instructions "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Special Instructions"] = line[1]
        test_string = "Booklet Fold and Staple "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Booklets"] = line[1]
        test_string = "Front Cover "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Front Cover"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Back Cover "
        if test_string in lines:
            line = lines.split(test_string)
            school_data["Back Cover"] = line[1].replace("=E2=80=93 ", "")
        test_string = "Deliver To: "
        if test_string in lines:
            test_string = "Deliver to: (Staff Member's Name) "
            if test_string in lines:
                line = lines.split(test_string)
                school_data["Deliver To Address"] = line[1]
            else:
                test_string = "Deliver To: "
                line = lines.split(test_string)
                school_data["Deliver To Name"] = line[1]
        school_data["Ran"] = "False"

        # Creates the JSON file
    with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json', 'w') as outfile:
        json.dump(school_data, outfile, indent=4, separators=(',', ': '))
    return school_data
