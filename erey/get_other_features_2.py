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
with open(str(parent_dir) + "\common_stuff\\base_features.txt", 'r', encoding="utf-8") as input_file:
    for line in input_file:
        if counter == 0:
            counter += 1
            continue
        all_repos_interested.append(line.split("\t"))
####################################################################################################
# Scrapes API and saves the resulting json object in the directory named "repo_names_info"
# Each json object will be in its own file and the file name will be the name of the repo

async def getData(all_repos_interested):
    cwd = "D:\CS221-Data"
    toRequest = [5, 6, 20, 22, 23, 24, 25]
    folders =  ["stargazers", "subscribers", "issues", "commits", "pulls", "releases", "contributors"]
    count = 0
    start = 18150
    end = float("inf")
    startTime = time.time()
    for features in all_repos_interested:
        count += 1
        if count < start:
            continue
        if count >= end:
            break
        featureCount = 0
        updateCount = 0
        for feature in features:
            if featureCount != 22:
                featureCount += 1
                if toRequest.__contains__(featureCount):
                    updateCount += 1
                continue
            # If feature require stop
            if toRequest.__contains__(featureCount):
                async def req(updateCount, url, name, count):
                    r = requests.get(url, headers={"Authorization": "token "+ const.API_1})
                    data = r.json()
                    print (str(count) + "." + name + "_" + folders[updateCount])
                    with open(cwd + "\\" + folders[updateCount] + "\\" + name + ".json", 'w+', encoding="utf-8") as outfile:
                        json.dump(data, outfile, ensure_ascii=False)
                task = asyncio.ensure_future(req(updateCount -1, feature, features[3] + "_" + features[1], count))
                updateCount += 1
            featureCount += 1
        # if (count - start) % 400 == 0:
                #     await asyncio.sleep(3) # At most 5000 requests can be done an hour

        #     elapsedtime = time.time() - startTime
        #     print("(" + str(elapsedtime) + " seconds)")
        #     await asyncio.sleep(3) # At most 5000 requests can be done an hour


   # print("---------------------------- Completed up to item " + str(end) + "in " + str(elapsedtime) + " seconds ------------------------------")
asyncio.new_event_loop()
asyncio.run(getData(all_repos_interested))