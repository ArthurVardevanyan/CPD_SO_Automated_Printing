__version__ = "v20200225"

import files
import json
import SchoolDataJson
import os

class Files:

    NAME = ""
    PAGE_COUNT = ""


class Order:

    OD = ""
    UID = ""
    status = ""
    RESULT = ""
    NAME = ""
    NUMBER = ""
    SUBJECT = ""
    COPIES = 0
    DUPLEX = ""
    COLLATION = ""
    STAPLING = ""
    STAPLING_BOOL = False
    DRILLING = ""
    FOLDING = ""
    CUTTING = ""
    BOOKLET = ""
    FRONT_COVER = ""
    BACK_COVER = ""
    SLIPSHEETS = ""
    SPECIAL_INSTRUCTIONS = ""

    PAPER = ""
    PAPER_SIZE = ""
    PAPER_COLOR = ""
    PAPER_WEIGHT = ""

    DATE = ""
    FIRST_NAME = ""
    LAST_NAME = ""
    EMAIL = ""
    PHONE = ""
    BILL_TO = ""
    DELIVER_TO_NAME = ""
    DELIVER_TO_ADDRESS = ""

    PAGE_COUNTS = ""
    PAGE_COUNTS_LIST = ""
    FILE_NAMES = []

    def __init__(self):
        self.FILES = []

    COST = 0


def order_initialization(order, JOB_INFO):
    order.UID = JOB_INFO.get('Email_ID', False)
    order.status = JOB_INFO.get('Status', False)
    order.NUMBER = JOB_INFO.get('Order Number', False)
    order.SUBJECT = JOB_INFO.get('Order Subject', False)
    order.COPIES = int(JOB_INFO.get('Copies', False))
    order.DUPLEX = JOB_INFO.get('Duplex', False)
    order.COLLATION = JOB_INFO.get('Collation', False)
    order.STAPLING = JOB_INFO.get('Stapling', False)
    order.DRILLING = JOB_INFO.get('Drilling', False)
    order.FOLDING = JOB_INFO.get('Folding', False)
    order.CUTTING = JOB_INFO.get('Cutting', False)
    order.BOOKLET = JOB_INFO.get('Booklets', False)
    order.FRONT_COVER = JOB_INFO.get('Front Cover', False)
    order.BACK_COVER = JOB_INFO.get('Back Cover', False)
    order.SLIPSHEETS = JOB_INFO.get('Slip Sheets / Shrink Wrap', False)
    order.SPECIAL_INSTRUCTIONS = JOB_INFO.get('Special Instructions', False)
    order.PAPER = JOB_INFO.get('Paper', False)
    order.DATE = JOB_INFO.get('Date Ordered', False)
    order.FIRST_NAME = JOB_INFO.get('First Name', False)
    order.LAST_NAME = JOB_INFO.get('Last Name', False)
    order.EMAIL = JOB_INFO.get('Email', False)
    order.PHONE = JOB_INFO.get('Phone Number', False)
    order.DELIVER_TO_NAME = JOB_INFO.get('Deliver To Name', False)
    order.DELIVER_TO_ADDRESS = JOB_INFO.get('Deliver To Address', False)

    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    for FILE in JOB_INFO_FILES:
        FILE_INFO = JOB_INFO_FILES.get(str(FILE), 0)
        F = Files()
        F.NAME = str(FILE_INFO.get('File Name', 0))
        F.PAGE_COUNT = int(FILE_INFO.get('Page Count', 0))
        order.FILES.append(F)
    order.FILE_NAMES = [i.NAME for i in order.FILES]
    order.PAGE_COUNTS, order.PAGE_COUNTS_LIST = files.page_counts(order)

    if(any(s in str(order.STAPLING) for s in ("Upper Left - portrait",  "Upper Left - landscape",  "Double Left - portrait",  "None"))):
        order.STAPLING_BOOL = True

    return order


def notStarted():
    import sys
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    OD = "SO/"
    folders = files.folder_list(OD)
    orders = []
    for i in range(len(folders)):
        if ("Error" in folders[i] or "Archive" in folders[i]):
            folders.pop(i)
    for folder in folders:
        order = Order()
        order.OD = OD
        order.NAME = folder
        order.NUMBER = folder.split(" ", 1)[0]
        order.SUBJECT = folder.split(" ", 1)[1]
        # Create JSON file with Job Requirements
        JSON_PATH = "".join(
        [order.OD, '/', order.NAME, '/', order.NAME, '.json'])
        if (os.path.exists(JSON_PATH)):
            with open(JSON_PATH) as json_file:
                JOB_INFO = json.load(json_file)
        else:
            JOB_INFO = SchoolDataJson.school_data_json(order)
        order = order_initialization(order, JOB_INFO)
        if(order.status == "NotStarted"):
            orders.append(order.NAME)

    return orders
