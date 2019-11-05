# Invoicing
__version__ = "v20191104"

import files
import json
import pandas

invoice_headers = [
    "Order Number",
    "Teacher",
    "Teacher Email",
    "Order Subject",
    "File",
    "Page Count",
    "Copies",
    "Total Impressions",
    "Duplex",
    "Copy Unit Cost",
    "Copy Cost",
    "Collation",
    "Paper",
    "Paper Unit Cost",
    "Paper Cost",
    "Stapling",
    "Staple Unit Cost",
    "Staple Cost",
    "Drilling",
    "Drilling Unit Cost",
    "Drilling Cost",
    "Folding",
    "Folding Unit Cost",
    "Folding Cost",
    "Cutting",
    "Cutting Unit Cost",
    "Cutting Cost",
    "Booklet",
    "Booklet Unit Cost",
    "Booklet Cost",
    "SlipSheets",
    "SlipSheet Unit Cost",
    "SlipSheet Cost",
    "ShrinkWrap",
    "ShrinkWrap Unit Cost",
    "ShrinkWrap Cost",
    "Building",
    "File Cost",
    "Order Cost"

]
invoice = []
invoice.append(invoice_headers)

OUTPUT_DIRECTORY = "SO/"
with open('Credentials/pricing.json') as json_file:
    PRICING = json.load(json_file)

Start = str(input("Start #: "))
End = str(input("End   #: "))
folders = files.folder_list(OUTPUT_DIRECTORY)
ORDER_NAMES = []
for ORDER_NUMBER in range(int(Start), int(End)+1):

    ORDER_NUMBER = str(ORDER_NUMBER)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            ORDER_NAMES.append(i)
for ORDER_NAME in ORDER_NAMES:
    with open(OUTPUT_DIRECTORY+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file:
        JOB_INFO = json.load(json_file)
    JOB_INFO_FILES = JOB_INFO.get('Files', False)


    for files in JOB_INFO_FILES:
        FILE_INFO = JOB_INFO_FILES.get(str(files), 0)
        job = []
        job.append(JOB_INFO.get('Order Number', "0"))
        job.append(JOB_INFO.get('First Name', "0")+" "+ JOB_INFO.get('Last Name', "0"))
        job.append(JOB_INFO.get('Email', "0"))
        job.append(str(JOB_INFO.get('Order Subject', "0")).split(" - ")[1])
        job.append((str(FILE_INFO.get('File Name')).split(" ", 1)[1]).rsplit(" - ", 1)[0])
        job.append(FILE_INFO.get('Page Count', 0))
        COPIES = int(JOB_INFO.get('Copies', "0"))
        job.append(COPIES)
        IMP = int(FILE_INFO.get('Page Count', 0))*COPIES
        job.append(str(IMP))
        job.append(JOB_INFO.get('Duplex', "0"))
        if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)":
            CU = PRICING.get( "BW_Letter_DS", 0)
            job.append(CU)
            IMPS = float(CU) *IMP
            job.append(round(IMPS))
            duplex = .5
        else:
            CU = PRICING.get( "BW_Letter_SS", 0)
            job.append(CU)
            IMPS = float(CU) *IMP
            job.append(round(IMPS, 2))
            duplex = 1
        job.append(JOB_INFO.get('Collation', "0"))
        PAPER = JOB_INFO.get('Paper', "0")
        job.append(PAPER)
        if PAPER == "8.5 x 11 Paper White":
            PAPER = 0
            job.append("0")
            job.append("0")
        else:
            CP = PRICING.get( "Color_Paper", 0)
            job.append(CP)
            PAPER = float(CP)*COPIES * duplex
            job.append(round(PAPER, 2))
        STAPLING = JOB_INFO.get('Stapling', "None")
        job.append(STAPLING)
        if STAPLING == "Upper Left - portrait":
            CS = PRICING.get( "Staple", 0)
            job.append(CS)
            STAPLING = float(CS)*COPIES
            job.append(round(STAPLING, 2))
        else:
            STAPLING = 0
            job.append("0")
            job.append("0")
        DRILLING = JOB_INFO.get('Drilling', "No")
        job.append(DRILLING)
        if DRILLING == "Yes":
            CD = PRICING.get( "3-Hole", 0)
            job.append(CD)
            DRILLING = float(CD)*COPIES
            job.append(round(DRILLING, 2))
        else:
            DRILLING = 0
            job.append("0")
            job.append("0")
        FOLDING = JOB_INFO.get('Folding', "No")
        job.append(FOLDING)
        if FOLDING == "Yes":
            CF = PRICING.get( "Folding", 0)
            job.append(CF)
            FOLDING = float(CF)*COPIES
            job.append(round(FOLDING, 2))
        else:
            FOLDING = 0
            job.append("0")
            job.append("0")
        CUTTING = JOB_INFO.get('Cutting', "No")
        job.append(CUTTING)
        if CUTTING == "Yes":
            CC = PRICING.get( "M_Cut", 0)
            job.append(CC)
            CUTTING = float(CC)*COPIES
            job.append(round(CUTTING, 2))
        else:
            CUTTING = 0
            job.append("0")
            job.append("0")
        BOOKLETS = JOB_INFO.get('Booklets', "No")
        job.append(BOOKLETS)
        if BOOKLETS == "Yes":
            CB = PRICING.get( "Booklet", 0)
            job.append(CB)
            BOOKLETS = float(CB)*COPIES
            job.append(round(BOOKLETS, 2))
        else:
            BOOKLETS = 0
            job.append("0")
            job.append("0")
        job.append("0")
        job.append("0")
        job.append("0")
        job.append("0")
        job.append("0")
        job.append("0")
        job.append(JOB_INFO.get('Deliver To Name', "0"))
        job.append(round(IMPS+PAPER+STAPLING+DRILLING+FOLDING+CUTTING+BOOKLETS,2))
        invoice.append(job)

    pos = len(invoice) -1
    end = len(invoice) - len(JOB_INFO_FILES)
    total = 0
    while (pos >= end):
        total += invoice[pos][len(invoice[pos])-1]
        pos -=1
    pos = len(invoice) -1
    while (pos >= end):
        invoice[pos].append(total)
        pos -=1


dataframe_array= pandas.DataFrame(invoice)
dataframe_array.to_csv("invoice.csv")



    







