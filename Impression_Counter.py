# Impression Counter
__version__ = "v20190928"
import json
import files
import pprint


OUTPUT_DIRECTORY = 'SO/'

print("\nTerminal AutoPrinting REV: " + __version__)
Start = str(input("Start #: "))
End = str(input("End   #: "))
Job_Specs = {}
Total_Copies = 0
Total_Staples = 0
for ORDER_NUMBER in range(int(Start), int(End)+1):
    ORDER_NUMBER = str(ORDER_NUMBER)
    ORDER_NAME = " "  # This is the Order Name taken from the subject line.=
    # Calls a function in files.py, which gets a list of all the orders downladed
    folders = files.folder_list(OUTPUT_DIRECTORY)
    for i in folders:  # Searchs for Requested Order Number from list of currently downloaded orders
        if ORDER_NUMBER in i:
            ORDER_NAME = i
    if ORDER_NAME == " ":
        continue
    # Calls a function in files.py, which gets all the pdf files within that order numbers folder.
    FILES = files.file_list(OUTPUT_DIRECTORY, ORDER_NAME)

    try:
        with open(OUTPUT_DIRECTORY+'/'+ORDER_NAME+'/'+ORDER_NAME+'.json') as json_file:
            JOB_INFO = json.load(json_file)
    except:
        print("JSON File Failed")
        continue
    

    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    copy_count = 0
    stapling = 0
    if JOB_INFO.get('Duplex', False) == "Two-sided (back to back)":
        duplex = 2
    else:
        duplex = 1
    for items in JOB_INFO_FILES:
        copy_count += int(str(JOB_INFO_FILES.get(items))
                          [-3:-2])*int(JOB_INFO.get('Copies', False))
        if JOB_INFO.get('Stapling', False):
            stapling += int(JOB_INFO.get('Copies', False))
    Job_Specs[str(JOB_INFO.get('Paper', False))] = int(
        Job_Specs.get(JOB_INFO.get('Paper', False), 0)) + copy_count/duplex
    Total_Copies += copy_count
    if JOB_INFO.get('Stapling', False):
        Job_Specs[str(JOB_INFO.get('Stapling', False))] = int(
            Job_Specs.get(JOB_INFO.get('Stapling', False), 0)) + stapling
    Total_Staples += stapling


print("Impressions: " + str(Total_Copies))
print("Staples: " + str(Total_Staples))
pprint.pprint(Job_Specs)
