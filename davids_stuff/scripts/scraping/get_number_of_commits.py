import urllib.request
from bs4 import BeautifulSoup
import os

cwd = os.getcwd()

to_download = list()

with open("need_commits.txt") as input_file:
    for line in input_file:
        to_download.append(line.rstrip().replace("_", "/", 1))

output = open(cwd + "/project_to_commits_second_round.txt", "w+")

for i in range(len(to_download)):
    name = to_download[i]
    #if name not in do_not_use_again:
    url = "https://github.com/" + name
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        soup = BeautifulSoup(mystr, "html5lib")
        auth = soup.find_all("a", attrs={"class" : "url fn", "rel" : "author"})
        na = soup.find_all("strong", attrs={"itemprop" : "name"})
        if len(auth) != 1 and len(na) != 1:
            print("ERRO REREWRJWR")
            print(url)
            continue
        ha = na[0].find("a").string
        name_new = auth[0].string + "/" + ha
        com = soup.find_all('li', attrs={"class": "commits"})
        if len(com) != 1:
            print("ERROR ERROR")
            continue
        commits = int(com[0].find("span", attrs={"class" : "num text-emphasized"}).string.replace(",", ""))
        output.write(name + "\t" + str(commits) + "\n")
        #print(name + "NUM COMMITS:" + str(commits))
    except urllib.error.HTTPError as e:
        #print(e)
        print(url)
output.close()

'''
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/input_data/all_project_ground_truths.txt") as do_not_use_file:
    for line in do_not_use_file:
        if "owner.login_name	owner.type	open_issues_count	has_wiki	has_downloads" in line:
            continue
        token_of_interest = line.rstrip().split("\t")[0]
        to_download.append(token_of_interest)

do_not_use_again = list()

try:
    with open(cwd + "/features_of_baseline.txt") as do_not_use_file:
        for line in do_not_use_file:
            token_of_interest = line.rstrip().split("\t")[0]
            do_not_use_again.append(token_of_interest)
except FileNotFoundError:
        donothing = 1

output = open(cwd + "/project_to_commits.txt", "a")
for i in range(len(to_download)):
    name = to_download[i]
    if name not in do_not_use_again:
        url = "https://github.com/" + name
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr, "html5lib")
            auth = soup.find_all("a", attrs={"class" : "url fn", "rel" : "author"})
            na = soup.find_all("strong", attrs={"itemprop" : "name"})
            if len(auth) != 1 and len(na) != 1:
                print("ERRO REREWRJWR")
                quit()
            ha = na[0].find("a").string
            name_new = auth[0].string + "/" + ha
            com = soup.find_all('li', attrs={"class": "commits"})
            if len(com) != 1:
                print("ERROR ERROR")
                continue
            commits = int(com[0].find("span", attrs={"class" : "num text-emphasized"}).string.replace(",", ""))
            output.write(name + "\t" + str(commits) + "\n")
            print(name)
        except urllib.error.HTTPError as e:
            print(e)
            print(url)
output.close()
'''