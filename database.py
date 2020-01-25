__version__ = "v20200124"

import mysql.connector
import files
import json
from datetime import datetime


def database_input(OUTPUT_DIRECTORY, JOB_INFO):

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
                        drilling,folding,cutting,booklets,front_cover,back_cover,special_instructions,slip_shrink) "
                 "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
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


def status_change(order):

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

    cursor = db.cursor()
    status = "UPDATE order_data SET status = '"+order.status + \
        "' WHERE order_number = '"+order.NUMBER+"'"

    cursor.execute(status)

    db.commit()

    db.close
    return 1


def main(OUTPUT_DIRECTORY):
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


if __name__ == "__main__":
    main("SO/")
