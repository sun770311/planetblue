# Planet Blue Ambassador Data Analysis 
Hannah Sun   
hysun@umich.edu  
  
## Goals
* Extract data from University of Michigan's MCommunity to update the U-M Planet Blue Ambassador (PBA) database.   
    * Read from a Google Sheet to retrieve uniqnames by row number
    * Request affiliation data for each uniqname
    * Write extracted credentials to output spreadsheet
* Analyze data for campus distribution of PBAs to determine target audiences for future Planet Blue campaigns    
<br />
     
## Restrictions  
For student and faculty privacy reasons, the .env file containing Client ID and Secret is empty.   
Links to the Google Sheets to read from and write to are also not included.   
To authorize Google API credentials for a desktop application, follow [these instructions](https://developers.google.com/sheets/api/quickstart/python) to generate credentials.json.

__Please contact the API Directory Team to request access to restricted University of Michigan APIs.__   
<br />
   
## APIs 
* [Student Affiliation API](https://dir.api.it.umich.edu/docs/studentrecords/1/overview): University of Michigan API that takes in a uniqname/UMID number and returns
    a student's:
    1. First Name
    2. Last Name 
    3. Uniqname
    4. UMID
    5. Activity Status (Active, Inactive, Never a Student)
    6. School (LSA, COE, etc.)
    7. Program (Undergraduate/Graduate)  
* [Google Sheets API](https://developers.google.com/sheets/api/guides/values#python): Read & write to a range of cell values     
<br />

## Instructions
1. Select personal data to retrieve by indicating a number from 1 to 7 (corresponding to the 7 credential types listed above)   
2. Specify first row number in the Google Sheet with PBA uniqnames to read (Student Affiliation API input)  
3. Specify last row number to read (Student Affiliation API input)  
    
(**Warning: Student Affiliations API makes maximum 200 requests per minute**) 
<br />
<br />

## Adaptability
This project serves as a template for combining Google Sheets APIs with other types of University of Michigan APIs (MCommunityGroups, EmpJobDesc, etc.) to update database records based on uniqname and UMID.
      
<br />
<br />
A University of Michigan Portlab Project  