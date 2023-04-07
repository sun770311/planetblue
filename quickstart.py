from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

from pprint import pprint
from googleapiclient import discovery

import numpy as np
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Nubu0jvhPI1nNYZt8XuZnuTZjhmIT4flz3QR0AZwrU8'
SAMPLE_RANGE_NAME = '!A1:B'


# Importing required libraries


# If you want to know in more detail, read below. If you don't understand what's written below, don't worry about it.


# The requests library (https://requests.readthedocs.io/en/latest/) is used for making HTTP requests to the API endpoint.
# The os library is used for accessing environment variables
# The dotenv library (https://pypi.org/project/python-dotenv/) is used for loading variables from a .env file into the environment.
import requests
import os
import json
from dotenv import load_dotenv



# The load_dotenv() function is called to load environment variables from a .env file.


# If you want to know in more detail, read below. If you don't understand what's written below, don't worry about it.


# This file should contain the CLIENT_ID and CLIENT_SECRET variables which are used for authentication when making requests to the API.
# These variables are loaded into the environment using the os.getenv() function.
load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")



# The requests.post() function is used to make a POST request to the API endpoint to obtain an access token.


# If you want to know in more detail, read below. If you don't understand what's written below, don't worry about it.


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
def get_members(id1):
    #members_url = f"https://gw.api.it.umich.edu/um/MCommunityGroups/Members/{group}"
    #members_url = f"https://gw.api.it.umich.edu/um/mcomm-person/find/{id1}"
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

    #print(response.text)
    #print(response.json())

    #prints entire API response
    #print(json.dumps(response.json(), separators=(",",":"), indent=2))

    #we only want the information inside of rows- QUESTION: do we want to rewrite for every
    #single piece of personal information (first name, last name, etc.)?
    json_str = json.dumps(response.json()["data"])
    resp = json.loads(json_str)
    resp_2 = resp["query"]
    resp_3 = resp_2["rows"]
    return (json.dumps(resp_3[0]["FIRST_NAME"]))

my_list2 = ["hysun", "yangjust", "jmfree"]


def main():
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
        spreadsheet_id = '1Nubu0jvhPI1nNYZt8XuZnuTZjhmIT4flz3QR0AZwrU8'  # TODO: Update placeholder value.

        # The A1 notation of the values to update.
        range_ = 'A1:A3'  # TODO: Update placeholder value.

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.


        value_range_body = {
            "values": 
                hi
            
        }

        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, 
                                                         range=range_, 
                                                         valueInputOption=value_input_option, 
                                                         body=value_range_body)
    
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        pprint(json.dumps(response))


    except HttpError as err:
        print(err)

    
hi = []



if __name__ == '__main__':
    for i in my_list2:
        hi.append(str(get_members(i)))
        
    hi = np.reshape(hi, (3,1)).tolist()
    print(hi)
    main()





