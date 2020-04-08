# Invoicing
__version__ = "20200310"
import files
import json
import math
import instructions
import order as o
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
    "Sheets",
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
invoiceList = []
invoiceList.append(invoice_headers)


def invoice(order, JOB_INFO):
    ORDER_NAME = order.NAME
    total = 0
    with open('Credentials/pricing.json') as json_file:
        PRICING = json.load(json_file)
    try:
        order = o.Order()
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
            job.append(
                str(JOB_INFO.get('Order Subject', "0")).split(" - ")[1])
            job.append((str(FILE_INFO.get('File Name')).split(
                " ", 1)[1]).rsplit(" - ", 1)[0])
            job.append(FILE_INFO.get('Page Count', 0))
            COPIES = int(JOB_INFO.get('Copies', "0"))
            job.append(COPIES)
            IMP = int(FILE_INFO.get('Page Count', 0))*COPIES
            job.append(str(IMP))
            job.append(JOB_INFO.get('Duplex', "0").split(
                " (back to back)")[0])
            SPECIAL = (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()) + \
                " " + \
                "color" in (JOB_INFO.get('Special Instructions', "0").lower())
            if ("color" in SPECIAL):
                if("different" in SPECIAL or "color paper" in SPECIAL or "colored" in SPECIAL
                    or "first page in color" in SPECIAL or "colorful" in SPECIAL
                        or "color slip" in SPECIAL or "color sheet" in SPECIAL and not "print in color" in SPECIAL):
                    job.append("BW")
                    COLOR = False
                else:
                    job.append("C")
                    COLOR = True
            else:
                job.append("BW")
                COLOR = False
            if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)" and int(FILE_INFO.get('Page Count', 0)) >= 2:
                if (COLOR):
                    CU = PRICING.get("Color_Letter_DS", 0)
                else:
                    CU = PRICING.get("BW_Letter_DS", 0)
                job.append(CU)
                IMPS = float(CU) * IMP
                job.append(round(IMPS, 2))
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
            if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)" and int(FILE_INFO.get('Page Count', 0)) % 2 == 0:
                IMPD = IMP / 2
            elif JOB_INFO.get('Duplex', False) == "One-sided":
                IMPD = IMP
            else:
                IMPD = (int(FILE_INFO.get('Page Count', 0)) - 1) * \
                    COPIES/2 + 1*COPIES
            job.append(IMPD)
            job.append(JOB_INFO.get('Collation', "0"))
            PAPER = JOB_INFO.get('Paper', "0")
            job.append(PAPER)
            if PAPER == "8.5 x 11 Paper White":
                PAPER = 0
                CP = 0
                job.append("0")
                job.append("0")
            elif PAPER == "8.5 x 11 Card Stock White":
                CP = PRICING.get("Cardstock", 0)
                job.append(CP)
                PAPER = float(CP)*math.ceil(IMPD)
                job.append(round(PAPER, 2))
            elif "8.5 x 11 Card Stock" in PAPER:
                CP = PRICING.get("Color_Cardstock", 0)
                job.append(CP)
                PAPER = float(CP)*math.ceil(IMPD)
                job.append(round(PAPER, 2))
            else:
                CP = PRICING.get("Color_Paper", 0)
                job.append(CP)
                PAPER = float(CP)*math.ceil(IMPD)
                job.append(round(PAPER, 2))
            STAPLING = JOB_INFO.get('Stapling', "None")
            if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)" and int(FILE_INFO.get('Page Count', 0)) <= 2:
                STAPLE_REVOKE = 0
            elif JOB_INFO.get('Duplex', False) == "One-sided" and int(FILE_INFO.get('Page Count', 0)) == 1:
                STAPLE_REVOKE = 0
            else:
                STAPLE_REVOKE = 1
            job.append(STAPLING)
            if STAPLING == "Upper Left - portrait" or STAPLING == "Upper Left - landscape":
                CS = PRICING.get("Staple", 0)
                job.append(CS)
                STAPLING = float(CS)*COPIES*STAPLE_REVOKE
                job.append(round(STAPLING, 2))
            elif STAPLING == "Double Left - portrait":
                CS = PRICING.get("D-Staple", 0)
                job.append(CS)
                STAPLING = float(CS)*COPIES*STAPLE_REVOKE
                job.append(round(STAPLING, 2))
            else:
                STAPLING = 0
                job.append("0")
                job.append("0")
            DRILLING = JOB_INFO.get('Drilling', "No")
            job.append(DRILLING)
            if DRILLING == "Yes":
                if JOB_INFO.get('Paper', "0") != "8.5 x 11 Paper White":
                    CD = PRICING.get("3-Hole-D", 0)
                    job.append(CD)
                    DRILLING = float(CD)*math.ceil(IMPD/1000)
                else:
                    CD = PRICING.get("3-Hole", 0)
                    job.append(CD)
                    DRILLING = float(CD)*IMPD
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
                FOLDING = float(CP)*IMPD
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
                if FRONTCOVER == "8.5 x 11 Paper White":
                    FC = 0
                    FRONTCOVER = 0
                    # Doesn't Account for Cover Colors Currently
                    job.append("0")
                    job.append("0")
                elif FRONTCOVER == "8.5 x 11 Card Stock White":
                    FC = PRICING.get("Cardstock", 0)
                    job.append(FC)
                    FRONTCOVER = float(FC)*COPIES
                    job.append(round(FRONTCOVER, 2))
                elif "8.5 x 11 Card Stock" in FRONTCOVER:
                    FC = PRICING.get("Color_Cardstock", 0)
                    job.append(FC)
                    FRONTCOVER = float(FC)*COPIES
                    job.append(round(FRONTCOVER, 2))
                else:
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
                if BACKCOVER == "8.5 x 11 Paper White":
                    BC = 0
                    BACKCOVER = 0
                    job.append("0")
                    job.append("0")
                elif BACKCOVER == "8.5 x 11 Card Stock White":
                    BC = PRICING.get("Cardstock", 0)
                    job.append(BC)
                    BACKCOVER = float(FC)*COPIES
                    job.append(round(BACKCOVER, 2))
                elif "8.5 x 11 Card Stock" in BACKCOVER:
                    BC = PRICING.get("Color_Cardstock", 0)
                    job.append(BC)
                    BACKCOVER = float(BC)*COPIES
                    job.append(round(BACKCOVER, 2))
                else:
                    BC = PRICING.get("Color_Paper", 0)
                    job.append(BC)
                    BACKCOVER = float(BC)*COPIES
                    job.append(round(BACKCOVER, 2))
            else:
                BACKCOVER = 0
                job.append("0")
                job.append("0")
            job.append("0")
            job.append("0")
            job.append("0")
            SLIP_SHRINK = JOB_INFO.get(
                'Slip Sheets / Shrink Wrap', "No")
            if "shrink wrap" in (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()):
                SRC = instructions.Special_Instructions(order)
                SR = PRICING.get("ShrinkWrap", 0)
                job.append(SRC[0])
                job.append(SR)
                SLIP_SHRINK = float(SR)*SRC[0]
                job.append(round(SLIP_SHRINK, 2))
            else:
                SLIP_SHRINK = 0
                job.append("0")
                job.append("0")
                job.append("0")
            if "laminate" in (JOB_INFO.get('Slip Sheets / Shrink Wrap', "0").lower()) or "laminate" in (JOB_INFO.get('Special Instructions', "0").lower()):
                job.append("Yes")
                LM = PRICING.get("Lamination", 0)
                job.append(LM)
                LAMINATION = float(LM)*IMPD
                job.append(round(LAMINATION, 2))
            else:
                LAMINATION = 0
                job.append("None")
                job.append("0")
                job.append("0")
            job.append(JOB_INFO.get('Deliver To Address', "0"))
            job.append(round(IMPS+PAPER+STAPLING+DRILLING +
                             FOLDING+CUTTING+BOOKLETS+LAMINATION+SLIP_SHRINK+FRONTCOVER+BACKCOVER, 2))
            invoiceList.append(job)
        pos = len(invoiceList) - 1
        end = len(invoiceList) - len(JOB_INFO_FILES)
        while (pos >= end):
            total += invoiceList[pos][len(invoiceList[pos])-1]
            pos -= 1
        pos = len(invoiceList) - 1
        while (pos >= end):
            order.COST = total
            invoiceList[pos].append(total)
            pos -= 1
    except Exception as e:
        print(e)
        job = []
        job.append(ORDER_NAME.split(" ", 1)[0])
        job.append(ORDER_NAME.split(" ", 1)[1])
        job.append("Error")
        invoiceList.append(job)
    return total


def main():
    order = o.Order()
    order.OD = "SO/"
    Start = str(input("Start #: "))
    End = str(input("End   #: "))
    folders = files.folder_list(order.OD)
    ORDER_NAMES = []
    for ORDER_NUMBER in range(int(Start), int(End)+1):
        ORDER_NUMBER = str(ORDER_NUMBER)  # .zfill(5)
        for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
            if ORDER_NUMBER in i:
                ORDER_NAMES.append(i)
    for ORDER_NAME in ORDER_NAMES:
        with open(order.OD+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file:
            JOB_INFO = json.load(json_file)
        with open(order.OD+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file_1:
            order = o.order_initialization(order, json.load(json_file_1))
        order.NAME = JOB_INFO["Order Number"] + JOB_INFO["Order Subject"]
        invoice(order, JOB_INFO)
    import pandas
    dataframe_array = pandas.DataFrame(invoiceList)
    dataframe_array.to_csv("invoice.csv")


if __name__ == "__main__":
    main()
