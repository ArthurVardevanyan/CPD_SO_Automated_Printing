# GDrive.py
# Downloaded Libraries
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# Built-In Libraries
import re
import log
__version__ = "v20200721"
# Source https://developers.google.com/drive/api/v3/quickstart/python
# Source https://stackoverflow.com/questions/52211886/downloading-file-from-google-drive-using-api-nameerror-name-service-is-not-d
# If modifying these scopes, delete the file token.json.
# Defines how much access is given to the program.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


def link_cleanup(file_links):
    """
    Removes unwanted characters from Google Drive File Links.
    
    Parameters: 
        file_links (list): The list containing all the unmodified Google Drive Links
                
    Returns: 
        list: The cleaned up Google Drive Links.
    """
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


def link_extractor(email_body):
    """
    This Function extracts the Google Drive FileIDs from the contents of the Email
    Checks if the email is indeed an Order and not something else.
    
    Parameters: 
        email_body (str): The body of the email for the current order.
                
    Returns: 
        list: Extraced Google Drive Links.
    """
    file_links = email_body
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
    """
    The main driver function for downloading files.

    Calls necessary functions to get Google File Links, calls the downloader for each file.

    Parameters: 
        email_body          (str): The body of the email for the current order.
        OUTPUT_DIRECTORY    (str): Location of the order.
        OrderNumber         (str): The Order Number.
        Subject             (str): The Subject Line fo the Email.
        error_state         (str): The flag that determines where to store the order.
                
    Returns: 
        bool: unused return
    """
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
    """
    Downloads the Google Drive file.

    Downloads the file, cleans up the filename, and increments each file.

    Parameters: 
        DRIVE_ID            (str): The Google Drive ID of the file being downloaded.
        ORDER_NUMBER        (str): The Order Number.
        OUTPUT_DIRECTORY    (str): Location of the order.
        Subject             (str): The Subject Line fo the Email.
        count               (int): Knows which file is being downloaded, is added to the file name.
        error_state         (str): The flag that determines where to store the order.
                
    Returns: 
        bool: unused return
    """
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
