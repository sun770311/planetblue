from __future__ import print_function

import os.path
import json
import numpy as np

import requests
import os
import json
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pprint import pprint
from googleapiclient import discovery

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Nubu0jvhPI1nNYZt8XuZnuTZjhmIT4flz3QR0AZwrU8'
SAMPLE_RANGE_NAME = '!A1:B'

load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# This token is necessary for making requests to protected endpoints.
# The grant_type parameter is set to "client_credentials" to indicate that we are using our own credentials.
# The scope parameter is set to "mcommunitygroups" to specify which resource we want to access.
# The auth parameter is set to a tuple containing the CLIENT_ID and CLIENT_SECRET variables to provide authentication credentials.
print(CLIENT_ID)
print(CLIENT_SECRET)

response = requests.post(
    "https://gw.api.it.umich.edu/um/oauth2/token",
    data={"grant_type": "client_credentials", "scope": "studentaffiliation"},
    auth=(CLIENT_ID, CLIENT_SECRET)
)


# The response.json() method is called on the response object to convert the response to a JSON format.
# The access token is extracted from the JSON object using the key "access_token", and stored in the token variable.
token = response.json()["access_token"]


# The get_members(group) function gets the name of all the members
# The get_members() function takes a single parameter group, which specifies the name of the group whose members are to be retrieved.


# If you want to know in more detail, read below. If you don't understand what's written below, don't worry about it.
# The URL for the group members API endpoint is constructed using an f-string.
# The Authorization header is set to include the access token in a Bearer token format.
# The Accept header is set to "application/json" to indicate that the client expects a JSON response.
def get_members(id1, target):
    members_url = f"https://gw.api.it.umich.edu/um/studentrecords/Affiliation"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    parameters = {
        "prompt_fieldvalue": {id1}
    }
# Finally, the requests.get() method is used to make a GET request to the group members API endpoint.
# The headers dictionary is passed as an argument to provide the authorization and accept headers.
# The response text is returned by the function.
    response = requests.get(members_url, headers = headers, params=parameters)

    #prints entire API response
    #print(json.dumps(response.json(), separators=(",",":"), indent=2))

    #accesses the relevant section of the API response (data in "rows")
    json_str = json.dumps(response.json()["data"])
    resp = json.loads(json_str)
    resp_2 = resp["query"]
    resp_3 = resp_2["rows"]

    #1. First Name
    #2. Last Name
    #3. Campus ID (uniqname)
    #4. EMPLID (UMID)
    #5. Typename (Active/Inactive/Never)
    #6. Description (School Name)
    #7. Program (Undergrad/Grad/PhD)

    match target:
        case '1':
            return (json.dumps(resp_3[0]["FIRST_NAME"]))
        case '2':
            return (json.dumps(resp_3[0]["LAST_NAME"]))
        case '3':
            return (json.dumps(resp_3[0]["CAMPUS_ID"]))
        case '4':
            return (json.dumps(resp_3[0]["EMPLID"]))
        case '5':
            return (json.dumps(resp_3[0]["TYPENAME"]))
        case '6':
            return (json.dumps(resp_3[0]["DESCR"]))
        case '7':
            return (json.dumps(resp_3[0]["PROGRAM"]))

member_list = ["hysun", 
            "yangjust", 
            "jmfree"]


def main(target):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = discovery.build('sheets', 'v4', credentials=creds)

        # The ID of the spreadsheet to update.
        spreadsheet_id = '1Nubu0jvhPI1nNYZt8XuZnuTZjhmIT4flz3QR0AZwrU8'  

        #Switch statement to determine which column to update
        # The A1 notation of the values to update.
        match target:
            case '1':
                range_ = 'A2:A4'
            case '2':
                range_ = 'B2:B4'
            case '3':
                range_ = 'C2:C4'
            case '4':
                range_ = 'D2:D4'
            case '5':
                range_ = 'E2:E4'
            case '6':
                range_ = 'F2:F4'
            case '7':
                range_ = 'G2:G4'
          

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'  


        value_range_body = {
            "values": 
                input_list
            
        }

        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, 
                                                         range=range_, 
                                                         valueInputOption=value_input_option, 
                                                         body=value_range_body)
    
        response = request.execute()

        pprint(json.dumps(response))

    except HttpError as err:
        print(err)

    
input_list = [] 

string1 = "Choose a number option:\n"
string2 = "1. First Name\n"
string3 = "2. Last Name\n"
string4 = "3. Uniqname\n"
string5 = "4. UMID\n"
string6 = "5. Active Status\n"
string7 = "6. School\n"
string8 = "7. Program\n"
temp = ''.join((string1, string2, string3, string4,
                string5, string6, string7, string8))

usr_input = input(temp)

if __name__ == '__main__':
    for i in member_list:
        input_list.append(str(get_members(i, usr_input)))

    #converts 1d array to 2d array to display result in different rows instead of columns
    input_list = np.reshape((input_list), (3,1)).tolist()
    #print(input_list)
    main(usr_input)





