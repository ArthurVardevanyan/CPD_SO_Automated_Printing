from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
# https://developers.google.com/drive/api/v3/quickstart/python
# Source https://stackoverflow.com/questions/52211886/downloading-file-from-google-drive-using-api-nameerror-name-service-is-not-d

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly' #Defines how much acess is given to the program.


def GoogleDriveDownload(FileId, OrderNumber, OUTPUT_DIRECTORY, Subject, Error):
    store = file.Storage('Credentials/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'Credentials/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    try:
        file_id = FileId
        request = service.files().get(fileId=file_id)  # pylint: disable=no-member
        result = request.execute()

        # will return metadata of file but I will only get file name
        file_name = result['name']
        print(f"File name is {file_name}")

        # will get actual file
        request = service.files().get_media(fileId=file_id)  # pylint: disable=no-member
        result = request.execute()
        print("Downloading " + file_name)

        # Remove Unwanted Characters from file path
        file_name = re.sub(r'[\\/:;?\"<>*|]', "", file_name)

        # will write file using the file_name
        with open(OUTPUT_DIRECTORY+Error+OrderNumber+" " +Subject+"/" + OrderNumber + " " + file_name, mode="wb") as f:
                f.write(result)
        print("Finished writing " + file_name)

    except:
        print("DRIVE FAILED: LINK (or path) PROBBLY DOES NOT EXIST: ", FileId)
