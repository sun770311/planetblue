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

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Obtain CLIENT_ID and CLIENT_SECRET from .env file
CLIENT_ID = os.getenv("CLIENT_ID") 
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

response = requests.post(
    "https://gw.api.it.umich.edu/um/oauth2/token",
    data={"grant_type": "client_credentials", "scope": "studentaffiliation"},
    auth=(CLIENT_ID, CLIENT_SECRET)
)

token = response.json()["access_token"]

# get_list() returns a list of uniqnames from the PBA Google Spreadsheet
def get_list(starting_point, end_point):
    creds = None

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
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API (Google Sheet to read from)
        NEW_ID = '1Slbbj_JEttGTACe9tpHorcMWopRT5QvBTnt_guduNoc'
        start_point = str(starting_point)
        num_names = str(end_point)
        NEW_RANGE = 'A' + start_point + ':A' + num_names
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=NEW_ID,
                                    range=NEW_RANGE).execute()
        values = result.get('values')

        if not values:
            print('No data found.')
            return

        updated_list = []
        for row in values:
            updated_list.append('%s' % (row[0]))

        # returns the list with number of uniqnames specified
        return updated_list
    
    except HttpError as err:
        print(err)


# get_affiliation() returns 1 of 7 details for a uniqname
def get_affiliation(id1, target):
    members_url = f"https://gw.api.it.umich.edu/um/studentrecords/Affiliation"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    parameters = {
        "prompt_fieldvalue": {id1}
    }

    response = requests.get(members_url, headers = headers, params=parameters)

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

    # Replaces invalid uniqname results with 'DOESNOTEXIST'
    if (resp_3 == []):
       return "DOESNOTEXIST"    
    
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


# main() writes the values returned from get_affiliation() to a spreadsheet 
def main(target, start_row, end_row):
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = discovery.build('sheets', 'v4', credentials=creds)

        # The ID of the spreadsheet to update.
        spreadsheet_id = '1Nubu0jvhPI1nNYZt8XuZnuTZjhmIT4flz3QR0AZwrU8'  

        # First row to be updated (all rows shifted down by 1 due to headers)
        names_start = str(start_row + 1)

        # Last row to be updated
        names_end = str(start_row + end_row)

        # Switch statement to determine which column to update
        match target:
            case '1':
                range_ = 'A' + names_start + ':A' + names_end
            case '2':
                range_ = 'B' + names_start + ':B' + names_end
            case '3':
                range_ = 'C' + names_start + ':C' + names_end
            case '4':
                range_ = 'D' + names_start + ':D' + names_end
            case '5':
                range_ = 'E' + names_start + ':E' + names_end
            case '6':
                range_ = 'F' + names_start + ':F' + names_end
            case '7':
                range_ = 'G' + names_start + ':G' + names_end
          
        value_input_option = 'USER_ENTERED'  

        value_range_body = {
            "values": 
                # List we have modified using get_affiliation()
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


# Prompts the user to select 1 of the 7 possible personal data
    #1. First Name
    #2. Last Name
    #3. Campus ID (uniqname)
    #4. EMPLID (UMID)
    #5. Typename (Active/Inactive/Never)
    #6. Description (School Name)
    #7. Program (Undergrad/Grad/PhD)

usr_input = input(temp)

# Prompts the user to specify which row on the sheet of uniqnames to start at
starting_point = input("\nEnter Index of Starting Row: ")
starting_point = int(starting_point)

# Prompts the user to specify ending row
print("IMPORTANT: Student Affiliations API makes MAXIMUM 200 requests per MINUTE")
end_point = input("\nEnter Index of Last Row: ")
end_point = int(end_point)

difference = end_point - starting_point + 1

member_list = get_list(starting_point, end_point)
print(member_list)

input_list = []

# List that we use to write to the Google Sheet
if __name__ == '__main__':
    for i in member_list:
        input_list.append(str(get_affiliation(i, usr_input)))

    # converts 1d array to 2d array to display result in different rows instead of columns
    input_list = np.reshape((input_list), (difference, 1)).tolist()
    print(input_list)

    # writes to google sheet
    main(usr_input, starting_point, end_point)





