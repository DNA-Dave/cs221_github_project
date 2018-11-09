# cs221_github_project
# RULES OF THE GITHUB PROJECT:
1. Please do not work in any of the public folders, (IE only work in your designated folder which I (David) have made for you). We can try to work on master as a team, but in order for this to work, you MUST only edit files in your own folder! When we are all ready to have something in the common folder, we will agree on it and make sure no conflicts exist.
2. Pretty much it. Don't put things that are too larger for github (IE data dumps, html scrapes, etc). 

Starting files:
In the common files folder, there is a file named "all_project_ground_truths.txt" and it has ALL of the ground truth values for ALL of the projects that we are interested in! 
In the common files folder, there is a file named "cs221-project-d676736fc863.json" This is the key for your bigquery access. Here's how you use it. 

from bq_helper import BigQueryHelper (must have this installed first, I think pip is fine)
run "export GOOGLE_APPLICATION_CREDENTIALS=\"*PATH_TO_THIS_FILE*/cs221-project-1b5850653193.json\"
Then query away!

Queries are basically SQL:
QUERY = "
        SELECT *
        FROM `bigquery-public-data.github_repos.languages`
        "

df = bq_assistant.query_to_pandas_safe(QUERY)
