import requests
from pathlib import Path
import os
import json
####################################################################################################
# This part parses all of the repo names that we have in our ground truth file (IE all the repos we are interested in
# Repo names will be in a list called "all_repos_interested" at the end of this section of code
cwd = str(os.getcwd())
parent_dir = Path(os.getcwd()).parent
parent_of_parent = Path(parent_dir).parent
parent_of_parent_of_parent = parent_of_parent.parent

counter = 0
all_repos_interested = list()
with open(str(parent_of_parent_of_parent) + "/common_stuff/all_project_ground_truths.txt") as input_file:
    for line in input_file:
        if counter == 0:
            counter += 1
            continue
        name = line.split("\t")[0]
        all_repos_interested.append(name)
####################################################################################################
# Scrapes API and saves the resulting json object in the directory named "repo_names_info"
# Each json object will be in its own file and the file name will be the name of the repo

for name in all_repos_interested:
    url = "https://api.github.com/search/repositories?q=" + name + "+in%3Aname&type=Repositories"
    r = requests.get(url)
    data = r.json()
    with open(cwd + "/repo_names_info/" + name.replace("/", "_") + ".txt", 'w+') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    break
