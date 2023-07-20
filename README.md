# Planet Blue Ambassador Data Analysis 
Hannah Sun   
hysun@umich.edu  
  
## Goals
* Extract data from University of Michigan's MCommunity to update the existing Planet Blue Ambassador  
(PBA) database in Google Sheets.   
* Analyze data for campus distribution of PBAs to determine target audiences for future Planet Blue campaigns    
    
     
## Restrictions  
For student and faculty privacy reasons, the .env file containing Client ID and Secret is not attached.   
Links to the Google Sheets to read from and write to are also not included.   
__Please contact the API Directory Team to request access to restricted University of Michigan APIs.__
     

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
* [Google Sheets API](https://developers.google.com/sheets/api/guides/values#python): Reads & writes to a range of cell values     
      
## Instructions
1. Select personal data to retrieve by indicating a number from 1 to 7 (corresponding to the 7 student credentials listed above)   
2. Specify first row number   
3. Specify last row number   
    
(**Warning: Student Affiliations API makes maximum 200 requests per minute**)     
      
<br />
<br />
A University of Michigan Portlab Project  