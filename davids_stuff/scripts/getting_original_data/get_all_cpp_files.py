import pandas as pd
from bq_helper import BigQueryHelper

print("export GOOGLE_APPLICATION_CREDENTIALS=\"/Users/davidwu/Downloads/cs221-project-1b5850653193.json\"")

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")
#all_tables = bq_assistant.list_tables()
#for table in all_tables:
#    print(table)
#    print(str(bq_assistant.table_schema(table)))

QUERY = """
        SELECT *
        FROM `bigquery-public-data.github_repos.languages`
        """
#print(bq_assistant.estimate_query_size(QUERY))
print("HELLO")
df = bq_assistant.query_to_pandas_safe(QUERY)
print("HELLO")
df.to_csv("all_project_languages.txt", sep='\t')