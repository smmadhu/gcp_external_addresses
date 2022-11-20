import os, json, sys
import pygsheets
import pandas as pd
from google.oauth2 import service_account
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_svc_acc_secret.json"

credentials = GoogleCredentials.get_application_default()

service_compute = discovery.build('compute', 'v1', credentials=credentials)

def get_argument():
    project_list = []
    if len(sys.argv) > 1:
        project = sys.argv[1]
        project_list.append(project)
    else:   
        gcps_id = list_projects()
        for project in gcps_id:
            project_list.append(project)
    return project_list

#Declarations for resourcemanager API to get GCPs list
service_resourcemanager = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
request_resourcemanager = service_resourcemanager.projects().list()

#Function to list of GCP's in organization
def list_projects():
    global request_resourcemanager
    filtered_list = []
    while request_resourcemanager is not None:
        response = request_resourcemanager.execute()
        for project in response.get('projects', []):
            temp_lists = project['projectId'].split('\n')
            for project_id in temp_lists:
                if not project_id.startswith("sys-"):   #exclution of project Id's which starts with 'sys-*' created for Apps script
                    filtered_list.append(project_id)
        request_resourcemanager = service_resourcemanager.projects().list_next(previous_request=request_resourcemanager, previous_response=response)
    return filtered_list


projects = get_argument()
print(projects)



# Function to get addresses used in the project
def get_addresses():
    dump_list = []
    for lists in projects:
        # Error handling for the failed projects to get the data from, either due to project not found or no access
        try:
            request = service_compute.addresses().aggregatedList(project=lists.strip())
            response = request.execute()
            for data_dump in response['items'].items():
                for lists,keys in enumerate(data_dump):
                    if 'addresses' in keys:
                        for dicts in keys['addresses']:
                            if (dicts["status"] == "IN_USE") and (dicts["addressType"] == "EXTERNAL"):
                                users_list = dicts["users"]
                                data_list = (dicts["address"], ', '.join([item[item.rindex('/', 0, item.rindex('/'))+1:] for item in users_list]), response["id"].rsplit("/")[1])
                                dump_list.append(data_list)
        except Exception as e:
            print(e)
    return dump_list

print(*get_addresses(),sep='\n')


"""
#Below code block to update the data gathered above to the spreadsheet
gc = pygsheets.authorize(service_file='your_svc_acc_secret.json') #svc account which has permissions to the respective sheet

df = pd.DataFrame()
column1 = []
column2 = []
column3 = []

for i,j,l in get_addresses():
    column1.append(i)
    column2.append(j)
    column3.append(l)

df['External IP'] = column1
df["In_use_by"] = column2
df["project"] = column3

sh = gc.open_by_key('your_google_sheet_id_here') # set the sheet ID where the data to be uploaded on same 

try:
    wks = sh.worksheet_by_title("External_IPs")
    print("worksheet found")
except pygsheets.WorksheetNotFound as error:
    sh.add_worksheet("External_IPs")

wks = sh.worksheet_by_title("External_IPs")
wks.set_dataframe(df,(1,1))
"""
