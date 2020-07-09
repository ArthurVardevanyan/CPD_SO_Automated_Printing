# GDrive.py
# Downloaded Libraries
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# Built-In Libraries
import re
import log
__version__ = "v20200709"
# Source https://developers.google.com/drive/api/v3/quickstart/python
# Source https://stackoverflow.com/questions/52211886/downloading-file-from-google-drive-using-api-nameerror-name-service-is-not-d
# If modifying these scopes, delete the file token.json.
# Defines how much access is given to the program.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


def link_cleanup(file_links):
 # Removing Unwanted Characters
    if(len(file_links) != 0):
        for i in range(len(file_links)):
            file_links[i] = file_links[i][2:].strip()
            file_links[i] = file_links[i].replace("3D", "", 1).replace(
                "https://drive.google.com/open?id", "").replace("\\r", "").replace("\\n", "")
            file_links[i] = re.sub(r'[\\\:*?\"<>|.;=\]\']', "", file_links[i])
            log.logger.debug(file_links[i])
        return file_links
    else:
        return []


def link_extractor(file_links):
    # This Function extracts the Google Drive FileIDs from the contents of the Email
    # Checks if the email is indeed a School Order and not something else.
    if ("Attach your file(s) in PDF format." in file_links):
        file_links = file_links.split("Number of Copies Needed per File", 1)
        file_links.pop(1)
        file_links = str(file_links)
        file_links = file_links.split("Attach your file(s) in PDF format.", 1)
        file_links.pop(0)
        file_links = str(file_links)
        file_links = file_links.split("File ")
        file_links.pop(0)
        return file_links
    else:
        return []


def Drive_Downloader(email_body, OrderNumber, OUTPUT_DIRECTORY, Subject, Error):
    file_links = link_extractor(email_body)
    file_links = link_cleanup(file_links)
    if(len(file_links)):
        # Calls the Downloader for each file.
        count = 0
        for ids in file_links:
            count += 1
            Google_Drive_Downloader(
                ids, OrderNumber, OUTPUT_DIRECTORY, Subject, count, Error)
        return 1
    else:
        print("This Isn't A Compatible Order")
        return 0


def Google_Drive_Downloader(DRIVE_ID, ORDER_NUMBER, OUTPUT_DIRECTORY, SUBJECT, count, ERROR_STATE):
    # Get the AUTH Token, or request a new token.
    store = file.Storage('Credentials/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'Credentials/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(
        Http()), cache_discovery=False)
    # Call the Drive v3 API
    try:
        file_id = DRIVE_ID
        request = service.files().get(fileId=file_id)  # pylint: disable=no-member
        result = request.execute()
        # will return metadata of file but I will only get file name
        file_name = result['name']
        print(f"File name is {file_name}")
        # will get actual file
        request = service.files().get_media(fileId=file_id)  # pylint: disable=no-member
        result = request.execute()
        print("Downloading ", file_name)
        # Remove Unwanted Characters from file path
        file_name = re.sub(r'[\\/:;?\"<>*|]', "", file_name)
        file_name = file_name.replace(
            "Multifunction Printer", "").replace("&", "and").replace("ñ", "n").replace("ó", "")
        # Adds file extension if missing.
        ext = "" if("pdf" in file_name) else ".pdf"
        # will write file using the file_name
        if count < 10:
            count = "".join([str("0"), str(count)])
        elif count > 10:
            return 2
        with open("".join([OUTPUT_DIRECTORY, "/", ERROR_STATE, "/", ORDER_NUMBER, " ", SUBJECT, "/", ORDER_NUMBER, ".", str(count), " ", file_name, ext]), mode="wb") as f:
            f.write(result)
        print("Finished writing ", file_name)
        return 1
    except:
        log.logger.exception("")
        print("DRIVE FAILED: LINK (or path) PROBABLY DOES NOT EXIST: ", DRIVE_ID)
        return 0
