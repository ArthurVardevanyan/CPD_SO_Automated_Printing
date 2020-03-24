__version__ = "v20200324"
import mysql.connector
import files
import json
from datetime import datetime
import order as o
import instructions


def credentials():
    try:
        with open("Credentials/db.txt") as f:
            cred = f.readlines()
        cred = [x.strip() for x in cred]
    except:
        print("Credential Failure")
    db = mysql.connector.connect(
        host="localhost",
        user=cred[0],
        passwd=cred[1],
        database='school_orders',
        auth_plugin='mysql_native_password'
    )
    return db


def database_input(OUTPUT_DIRECTORY, JOB_INFO):
    order = o.Order()
    try:
        order.OD = OUTPUT_DIRECTORY
        order.NAME = JOB_INFO.get('Order Number', "0") + \
            " " + JOB_INFO.get('Order Subject', "0")
        order = o.order_initialization(order, JOB_INFO)
    except:
        print("Order Initialization Failure")
    db = credentials()
    cursor = db.cursor()
    add_teacher = ("INSERT IGNORE INTO teachers "
                   "(email,first_name,last_name,phone) "
                   "VALUES (%s, %s, %s, %s)")
    data_teacher = (
        JOB_INFO.get('Email', "0"),
        JOB_INFO.get('First Name', "0"),
        JOB_INFO.get('Last Name', "0"),
        JOB_INFO.get('Phone Number', "0"),
    )
    add_order = ("INSERT IGNORE INTO order_data"
                 "( email_id,order_number,order_subject,date_ordered,status,cost,email,copies,duplex,collation,paper,stapling,\
                        drilling,folding,cutting,booklets,front_cover,back_cover,special_instructions,slip_shrink,sheets) "
                 "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_order = (
        JOB_INFO.get('Email ID', "0"),
        JOB_INFO.get('Order Number', "0"),
        JOB_INFO.get('Order Subject', "0"),
        datetime.strptime(JOB_INFO.get('Date Ordered', "0"),
                          '%b %d, %Y').strftime('%Y-%m-%d'),
        JOB_INFO.get('Status', "0"),
        JOB_INFO.get('Cost', "0"),
        JOB_INFO.get('Email', "0"),
        JOB_INFO.get('Copies', "0"),
        JOB_INFO.get('Duplex', "0"),
        JOB_INFO.get('Collation', "0"),
        JOB_INFO.get('Paper', "0"),
        JOB_INFO.get('Stapling', "None"),
        JOB_INFO.get('Drilling', "No"),
        JOB_INFO.get('Folding', "None"),
        JOB_INFO.get('Cutting', "None"),
        JOB_INFO.get('Booklets', "No"),
        JOB_INFO.get('Front Cover', "None"),
        JOB_INFO.get('Back Cover', "None"),
        JOB_INFO.get('Special Instructions', "None"),
        JOB_INFO.get('Slip Sheets / Shrink Wrap', "None"),
        order.PAGE_COUNTS * order.COPIES / instructions.duplex_state(order),
    )
    add_deliver = ("INSERT IGNORE INTO deliver "
                   "(order_number,name,address) "
                   "VALUES (%s, %s, %s)")
    data_deliver = (
        JOB_INFO.get('Order Number', "0"),
        JOB_INFO.get('Deliver To Name', "None"),
        JOB_INFO.get('Deliver To Address', "None"),
    )
    cursor.execute(add_teacher, data_teacher)
    cursor.execute(add_order, data_order)
    cursor.execute(add_deliver, data_deliver)
    add_files = ("INSERT IGNORE INTO files "
                 "(file_number, order_number,name,pages) "
                 "VALUES (%s, %s, %s, %s)")
    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    for FILES in JOB_INFO_FILES:
        FILE_INFO = JOB_INFO_FILES.get(str(FILES), 0)
        data_files = (
            (str(FILE_INFO.get('File Name')).split(
                " ", 1)[0]),
            JOB_INFO.get('Order Number', "0"),
            (str(FILE_INFO.get('File Name')).split(
                " ", 1)[1]).rsplit(" - ", 1)[0],
            FILE_INFO.get('Page Count', 0)
        )
        cursor.execute(add_files, data_files)
    db.commit()
    db.close
    return 1


def print_status(order, status):
    db = credentials()
    cursor = db.cursor()
    status = "UPDATE order_data SET status = '"+status + \
        "' WHERE order_number = '"+order+"'"
    cursor.execute(status)
    db.commit()
    db.close
    return 1


def manual_status_change(orders="NotStarted"):
    db = credentials()
    cursor = db.cursor()
    if orders == "NotStarted":
        status = "UPDATE order_data SET status = 'Printed' WHERE status  = 'NotStarted'"
        cursor.execute(status)
        db.commit()
    else:
        for order in orders:
            status = "UPDATE order_data SET status = 'Printed' WHERE `order_number`  like '%" + order + "%'"
            cursor.execute(status)
            db.commit()
    db.close
    return 1


def printingOrders():
    db = credentials()
    cursor = db.cursor()
    query = (
        "SELECT `order_number`, `status` FROM `order_data` WHERE `status` LIKE '%%P1%%'")
    cursor.execute(query)
    orders = []
    for (order_number, status) in cursor:
        order = (str(order_number).replace("(", "").replace(
            ")", "").replace(",", "").replace("'", ""), str(status).replace("(", "").replace(
            ")", "").replace(",", "").replace("'", "").replace("P", ""))
        orders.append(order)
    db.close
    return orders


def main(OUTPUT_DIRECTORY):
    printingOrders()
    option = str(
        input("1 To Add Orders, 2 to Mark Some Printed, 3 to Mark All Orders Printed: "))
    if (int(option) == 1):
        Start = str(input("Start #: "))
        End = str(input("End   #: "))
        folders = files.folder_list(OUTPUT_DIRECTORY)
        ORDER_NAMES = []
        for ORDER_NUMBER in range(int(Start), int(End)+1):
            ORDER_NUMBER = str(ORDER_NUMBER).zfill(5)
            for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
                if ORDER_NUMBER in i:
                    ORDER_NAMES.append(i)
        for ORDER_NAME in ORDER_NAMES:
            with open(OUTPUT_DIRECTORY+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file:
                JOB_INFO = json.load(json_file)
                database_input(OUTPUT_DIRECTORY, JOB_INFO)
                # print(ORDER_NAME)
    elif(int(option) == 2):
        ORDER_NUMBER = []  # The List of order numbers to validate and run
        # Contains the list of orders that were processed and also displays the state of them. ex, ran automatically, with manual input, invalid, aborted, etc.
        temp = ""
        while(temp != "run"):
            temp = str(input("Type In an Order Number: "))
            ORDER_NUMBER.append(temp)
        manual_status_change(ORDER_NUMBER)
    elif(int(option) == 3):
        manual_status_change()


if __name__ == "__main__":
    main("SO/")
