from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os
import json
from google.cloud import bigquery

####################################################################################################
# This part parses all of the repo names that we have in our ground truth file (IE all the repos we are interested in
# Repo names will be in a list called "all_repos_interested" at the end of this section of code
cwd = str(os.getcwd())
parent_dir = Path(os.getcwd()).parent
parent_of_parent = Path(parent_dir).parent
parent_of_parent_of_parent = parent_of_parent.parent

counter = 0
all_repos_interested = list()
with open(cwd + "/common_stuff/all_project_ground_truths.txt") as input_file:
    for line in input_file:
        if counter == 0:
            counter += 1
            continue
        name = line.split("\t")[0]
        all_repos_interested.append(name)
print all_repos_interested
#print all_repos_interested

####################################################################################################
##run "export 
#export "GOOGLE_APPLICATION_CREDENTIALS = cwd +\"common_stuff/cs221-project-d676736fc863.json\""
#run "export GOOGLE_APPLICATION_CREDENTIALS=\"*PATH_TO_THIS_FILE*/cs221-project-1b5850653193.json\""
#Then query away!

#Queries are basically SQL:
#QUERY = "
#        SELECT *
#        FROM `bigquery-public-data.github_repos.languages`
#        "
#
#df = bq_assistant.query_to_pandas_safe(QUERY)
#client = bigquery.Client.from_service_account_json(cwd+'/common_stuff/cs221-project-d676736fc863.json')
#print client
#QUERY = '''
#        SELECT content
#        FROM `bigquery-public-data.github_repos.contents`
#        WHERE size=5
#        LIMIT 1
##        '''

#df = bq_assistant.query_to_pandas_safe(QUERY)
#result =  client.query(QUERY).result()
#for row in result:
#    print row.content
#    break