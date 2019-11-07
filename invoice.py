# Invoicing
__version__ = "v20191106"

import files
import json
import math
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
    "image",
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
    "Drill Unit Cost",
    "Drilling Cost",
    "Folding",
    "FLD Unit Cost",
    "Folding Cost",
    "Cutting",
    "C Unit Cost",
    "C Cost",
    "Booklet",
    "BK Unit Cost",
    "Booklet Cost",
    "Front Cover",
    "FC Unit Cost",
    "FC Cost",
    "Back Cover",
    "BC Unit Cost",
    "BC Cost",
    "SlipSheets",
    "SP Unit Cost",
    "SP Cost",
    "ShrinkWrap",
    "SW Unit Cost",
    "SW Cost",
    "Lam",
    "Lam Unit Cost",
    "Lam Cost",
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
    try:
        with open(OUTPUT_DIRECTORY+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file:
            JOB_INFO = json.load(json_file)
        JOB_INFO_FILES = JOB_INFO.get('Files', False)

        TOTAL_PAGES = 0
        for FILES in JOB_INFO_FILES:
            FILE_INFO = JOB_INFO_FILES.get(str(FILES), 0)
            TOTAL_PAGES += int(FILE_INFO.get('Page Count', 0))

        for FILES in JOB_INFO_FILES:
            FILE_INFO = JOB_INFO_FILES.get(str(FILES), 0)
            job = []
            job.append(JOB_INFO.get('Order Number', "0"))
            job.append(JOB_INFO.get('First Name', "0") +
                    " " + JOB_INFO.get('Last Name', "0"))
            job.append(JOB_INFO.get('Email', "0"))
            job.append(str(JOB_INFO.get('Order Subject', "0")).split(" - ")[1])
            job.append((str(FILE_INFO.get('File Name')).split(
                " ", 1)[1]).rsplit(" - ", 1)[0])
            job.append(FILE_INFO.get('Page Count', 0))
            COPIES = int(JOB_INFO.get('Copies', "0"))
            job.append(COPIES)
            IMP = int(FILE_INFO.get('Page Count', 0))*COPIES
            job.append(str(IMP))
            job.append(JOB_INFO.get('Duplex', "0").split(" (back to back)")[0])
            if "color" in (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()) or "color" in (JOB_INFO.get('Special Instructions', "0").lower()):
                if "different" in (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()) or "different" in (JOB_INFO.get('Special Instructions', "0").lower()):
                    job.append("BW")
                    COLOR = False
                else:
                    job.append("C")
                    COLOR = True
            else:
                job.append("BW")
                COLOR = False
            if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)":
                if (COLOR):
                    CU = PRICING.get("Color_Letter_DS", 0)
                else:
                    CU = PRICING.get("BW_Letter_DS", 0)
                job.append(CU)
                IMPS = float(CU) * IMP
                job.append(round(IMPS))
                duplex = .5
            else:
                if (COLOR):
                    CU = PRICING.get("Color_Letter_SS", 0)
                else:
                    CU = PRICING.get("BW_Letter_SS", 0)
                job.append(CU)
                IMPS = float(CU) * IMP
                job.append(round(IMPS, 2))
                duplex = 1
            job.append(JOB_INFO.get('Collation', "0"))
            PAPER = JOB_INFO.get('Paper', "0")
            job.append(PAPER)
            if PAPER == "8.5 x 11 Paper White":
                PAPER = 0
                job.append("0")
                job.append("0")
            elif PAPER == "8.5 x 11 Card Stock White":
                CP = PRICING.get("Cardstock", 0)
                job.append(CP)
                PAPER = float(CP)*COPIES * duplex
                job.append(round(PAPER, 2))
            elif "8.5 x 11 Card Stock" in PAPER:
                CP = PRICING.get("Color_Cardstock", 0)
                job.append(CP)
                PAPER = float(CP)*COPIES * duplex
                job.append(round(PAPER, 2))
            else:
                CP = PRICING.get("Color_Paper", 0)
                job.append(CP)
                PAPER = float(CP)*COPIES * duplex
                job.append(round(PAPER, 2))
            STAPLING = JOB_INFO.get('Stapling', "None")
            job.append(STAPLING)
            if STAPLING == "Upper Left - portrait":
                CS = PRICING.get("Staple", 0)
                job.append(CS)
                STAPLING = float(CS)*COPIES
                job.append(round(STAPLING, 2))
            elif STAPLING == "Double Left - portrait":
                CS = PRICING.get("D-Staple", 0)
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
                CD = PRICING.get("3-Hole", 0)
                job.append(CD)
                DRILLING = float(CD)*COPIES
                job.append(round(DRILLING, 2))
            else:
                DRILLING = 0
                job.append("0")
                job.append("0")
            FOLDING = JOB_INFO.get('Folding', "None")
            job.append(FOLDING)
            if FOLDING != "None":
                CF = PRICING.get("Folding", 0)
                job.append(CF)
                FOLDING = float(CP)*COPIES * duplex
                job.append(round(FOLDING, 2))
            else:
                FOLDING = 0
                job.append("0")
                job.append("0")
            CUTTING = JOB_INFO.get('Cutting', "None")
            job.append(CUTTING)
            if CUTTING != "None":
                CC = PRICING.get("Cutting", 0)
                job.append(CC)
                CUTTING = math.ceil(TOTAL_PAGES * COPIES *
                                    duplex / 400) * float(CC) / len(JOB_INFO_FILES)
                job.append(round(CUTTING, 2))
            else:
                CUTTING = 0
                job.append("0")
                job.append("0")
            BOOKLETS = JOB_INFO.get('Booklets', "No")
            job.append(BOOKLETS)
            if BOOKLETS == "Yes":
                CB = PRICING.get("Booklet", 0)
                job.append(CB)
                BOOKLETS = float(CB)*COPIES
                job.append(round(BOOKLETS, 2))
            else:
                BOOKLETS = 0
                job.append("0")
                job.append("0")
            FRONTCOVER = JOB_INFO.get('Front Cover', "No")
            job.append(FRONTCOVER)
            if FRONTCOVER != "No":
                FC = PRICING.get("Color_Paper", 0)
                job.append(FC)
                FRONTCOVER = float(FC)*COPIES
                job.append(round(FRONTCOVER, 2))
            else:
                FRONTCOVER = 0
                job.append("0")
                job.append("0")
            BACKCOVER = JOB_INFO.get('Back Cover', "No")
            job.append(BACKCOVER)
            if BACKCOVER != "No":
                BC = PRICING.get("Color_Paper", 0)
                job.append(BC)
                BACKCOVER = float(BC)*COPIES
                job.append(round(BACKCOVER, 2))
            else:
                BACKCOVER = 0
                job.append("0")
                job.append("0")
            SPECIAL_INSTRUCTIONS = JOB_INFO.get('Slip Sheets / Shrink Wrap', "No")
            job.append("0")
            job.append("0")
            job.append("0")
            job.append("0")
            job.append("0")
            job.append("0")
            if "laminate" in (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()) or "laminate" in (JOB_INFO.get('Special Instructions', "0").lower()):
                job.append("Yes")
                LM = PRICING.get("Lamination", 0)
                job.append(LM)
                LAMINATION = float(LM)*IMP * duplex
                job.append(round(LAMINATION, 2))
            else:
                LAMINATION = 0
                job.append("None")
                job.append("0")
                job.append("0")
            job.append(JOB_INFO.get('Deliver To Name', "0"))
            job.append(round(IMPS+PAPER+STAPLING+DRILLING +
                            FOLDING+CUTTING+BOOKLETS+LAMINATION, 2))
            invoice.append(job)

        pos = len(invoice) - 1
        end = len(invoice) - len(JOB_INFO_FILES)
        total = 0
        while (pos >= end):
            total += invoice[pos][len(invoice[pos])-1]
            pos -= 1
        pos = len(invoice) - 1
        while (pos >= end):
            invoice[pos].append(total)
            pos -= 1
    except:
        job = []
        job.append(ORDER_NAME.split(" ", 1)[0])
        job.append(ORDER_NAME.split(" ", 1)[1])
        job.append("Error")
        invoice.append(job)



dataframe_array = pandas.DataFrame(invoice)
dataframe_array.to_csv("invoice.csv")
