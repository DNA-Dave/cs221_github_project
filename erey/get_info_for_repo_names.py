import requests
from pathlib import Path
import os
import json
import time
####################################################################################################
# This part parses all of the repo names that we have in our ground truth file (IE all the repos we are interested in
# Repo names will be in a list called "all_repos_interested" at the end of this section of code
cwd = "D:\CS221-Data"
parent_dir = Path(os.getcwd()).parent

counter = 0
all_repos_interested = list()
with open(str(parent_dir) + "\common_stuff\\all_project_ground_truths.txt") as input_file:
    for line in input_file:
        if counter == 0:
            counter += 1
            continue
        name = line.split("\t")[0]
        all_repos_interested.append(name)
####################################################################################################
# Scrapes API and saves the resulting json object in the directory named "repo_names_info"
# Each json object will be in its own file and the file name will be the name of the repo

count = 0
start = 189
startTime = time.time()
for name in all_repos_interested:
    count += 1
    if count < start:
        continue
    if (count - start)% 30 == 0:
        elapsedtime = time.time() - startTime
        print("(" + str(elapsedtime) + " seconds)")
    url = "https://api.github.com/search/repositories?q=" + name + "+in%3Aname&type=Repositories"
    
    r = requests.get(url,headers={"Authorization": "token TOKEN"})
    data = r.json()
    print(str(count) + "." + name)
    with open(cwd + "\\repo_names_info\\" + name.replace("/", "_") + ".json", 'w+', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    time.sleep(2)
    