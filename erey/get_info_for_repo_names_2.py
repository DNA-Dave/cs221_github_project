import requests
from pathlib import Path
import os
import json
import time
import asyncio
import const
####################################################################################################
# This part parses all of the repo names that we have in our ground truth file (IE all the repos we are interested in
# Repo names will be in a list called "all_repos_interested" at the end of this section of code
cwd = "D:\CS221-Data"
parent_dir = Path(os.getcwd())

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

async def getData(all_repos_interested):
    cwd = "D:\CS221-Data"
    count = 0
    start = 9690
    end = 10742
    startTime = time.time()
    for name in all_repos_interested:
        count += 1
        if count < start:
            continue
        if (count - start)% 30 == 0:
            elapsedtime = time.time() - startTime
            print("(" + str(elapsedtime) + " seconds)")
        if count >= end:
            print("---------------------------- Completed up to item " + str(end) + "in " + str(elapsedtime) + " seconds ------------------------------")
            break
        
        url = "https://api.github.com/search/repositories?q=" + name + "+in%3Aname&type=Repositories"
        async def req():
            r = requests.get(url,headers={"Authorization": "token "+const.API_2})
            data = r.json()
            print(str(count) + "." + name)
            with open(cwd + "\\repo_names_info\\" + name.replace("/", "_") + ".json", 'w+', encoding="utf-8") as outfile:
                json.dump(data, outfile, ensure_ascii=False)
        
        task = asyncio.ensure_future(req())
        
        await asyncio.sleep(2)

    print("---------------------------- Completed up to item " + str(end) + "in " + str(elapsedtime) + " seconds ------------------------------")
asyncio.new_event_loop()
asyncio.run(getData(all_repos_interested))