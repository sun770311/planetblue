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
    data={"grant_type": "client_credentials", "scope": "mcommunitygroups"},
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
def get_members(group):
    members_url = f"https://gw.api.it.umich.edu/um/MCommunityGroups/Members/{group}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
# Finally, the requests.get() method is used to make a GET request to the group members API endpoint.
# The headers dictionary is passed as an argument to provide the authorization and accept headers.
# The response text is returned by the function.


    response = requests.get(members_url, 
        headers = headers)


    #print(response.json())

    #cleaner format compared to one big list
    print(json.dumps(response.json(), separators=(",",":"), indent=4))


get_members("Michigan Badminton Club")