import urllib.request
from bs4 import BeautifulSoup
import os
import time

cwd = os.getcwd()

to_download = list()

with open(cwd + "/all_project_ground_truths.txt") as do_not_use_file:
    for line in do_not_use_file:
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

output = open(cwd + "/features_of_baseline.txt", "a")
output.write("Name of repo\tcommits\tpull_requests\n")
for i in range(len(to_download)):
    name = to_download[i]
    if name not in do_not_use_again:
        url = "https://github.com/" + name
        try:
            fp = urllib.request.urlopen(url)
            print(name)
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
            requ = soup.find_all("a", attrs = {"href" : "/" + name_new + "/pulls"})
            if len(requ) != 1:
                print(requ)
                print("ERROR ERROR2")
                continue
            count = int(requ[0].find("span", attrs={"class" : "Counter"}).string.replace(",", ""))
            output.write(name + "\t" + str(commits) + "\t" + str(count) + "\n")
        except urllib.error.HTTPError as e:
            print(e)
    #file_name = name + ".html"
    #output = open(cwd + "/all_github_pages_htmls/" + file_name.replace("/", "_"), "w+")
    #output.write(mystr)
    #output.close()
output.close()

