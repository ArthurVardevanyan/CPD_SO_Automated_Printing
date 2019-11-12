import mysql.connector
import files
import json

db = mysql.connector.connect(
    host="localhost",
    user="",
    passwd="",
    database='',
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()

OUTPUT_DIRECTORY = "SO/"

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
        print(ORDER_NAME)
        with open(OUTPUT_DIRECTORY+ORDER_NAME+"/"+ORDER_NAME+".json") as json_file:
            JOB_INFO = json.load(json_file)
            add_order = ("INSERT INTO order_list "
                         "(email_id, order_number) "
                           "VALUES (%s, %s)")
            data_order = (JOB_INFO.get('Email ID', "0"), JOB_INFO.get('Order Number', "0"))
            cursor.execute(add_order, data_order)
            db.commit()


db.close
