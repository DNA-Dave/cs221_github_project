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
parent_dir = Path(os.getcwd())

counter = 0
users = list()
with open(str(parent_dir) + "\\all_contributors.txt", 'r', encoding="utf-8") as input_file:
    for line in input_file:
        users.append(line.split("\t"))
####################################################################################################
# Scrapes API and saves the resulting json object in the directory named "repo_names_info"
# Each json object will be in its own file and the file name will be the name of the repo

async def getData(users):
    cwd = "D:\CS221-Data\\Users\\"
    count = 0
    start = 3650
    end = float("inf")
    pauseCount = 0;
    for userLine in users:
        count += 1
        if count < start:
            continue
        if count >= end:
            break
        updateCount = 0
        for user in userLine:
            if updateCount == 0:
                updateCount += 1
                continue
            pauseCount += 1
            # Guarantees 5000 requests per hour
            if pauseCount == 5000:
                await asyncio.sleep(3550)
                pauseCount = 0

            async def req(url, name, count):
                r = requests.get(url, headers={"Authorization": "token "+ const.API_2})
                data = r.json()
                print (str(count) + "." + name)
                with open(cwd + name + ".json", 'w+', encoding="utf-8") as outfile:
                    json.dump(data, outfile, ensure_ascii=False)
            task = asyncio.ensure_future(req("https://api.github.com/users/" + user + "/followers" , user.replace("\n",""), count))
            updateCount += 1



asyncio.new_event_loop()
asyncio.run(getData(users))