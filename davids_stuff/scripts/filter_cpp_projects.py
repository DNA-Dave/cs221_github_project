import json
import urllib.request
from bs4 import BeautifulSoup
import os

projname_to_attrs = dict()

all_potential_lines = list()
with open("all_project_languages.csv") as all:
    for line in all:
        if "C++" in line:
            all_potential_lines.append(line.rstrip())


all_cpp_projs_output = open("all_cpp_projects.txt", "w+")
for line in all_potential_lines:
    tokens = line.split("\t")
    name = tokens[1]
    attrs = tokens[2]
    if "\"" in attrs:
        continue
    list_representation = json.loads(attrs.replace("\'", "\""))
    if len(list_representation) == 1 and "Objective-C++" not in attrs:
        all_cpp_projs_output.write(name + "\n")
        projname_to_attrs[name] = attrs
all_cpp_projs_output.close()

cwd = os.getcwd()

do_not_use_again = list()

try:
    with open(cwd + "/all_project_ground_truths.txt") as do_not_use_file:
        for line in do_not_use_file:
            token_of_interest = line.rstrip().split("\t")[0]
            do_not_use_again.append(token_of_interest)
except FileNotFoundError:
    donothing = 1

try:
    with open(cwd + "/errors.txt") as do_not_use_file:
        for line in do_not_use_file:
            token_of_interest = line.rstrip()
            do_not_use_again.append(token_of_interest)
except FileNotFoundError:
    donothing = 1

output = open(cwd + "/all_project_ground_truths.txt", "a")
output_1 = open(cwd + "/errors.txt", "a")
output.write("Name of repo\tstars\tforks\twatches\n")
list_keys = list(projname_to_attrs.keys())
for i in range(len(list_keys)):
    name = list_keys[i]
    if name not in do_not_use_again:
        url = "https://github.com/" + name
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr, "html5lib")
            stats = soup.find_all('a', attrs={"class": "social-count"})
            if len(stats) != 3:
                print("ERROR ERROR")
                quit()
            for stat in stats:
                label = stat['aria-label']
                if "watching" in label:
                    num_watchers = int((stat.string).replace(",", ""))
                elif "starred" in label:
                    num_stars = int((stat.string).replace(",", ""))
                elif "forked" in label:
                    num_forks = int((stat.string).replace(",", ""))
            output.write(name + "\t" + str(num_stars) + "\t" + str(num_forks) + "\t" + str(num_watchers) + "\n")
        except urllib.error.HTTPError as e:
            output_1.write(name + "\n")
            print(e)
    #file_name = name + ".html"
    #output = open(cwd + "/all_github_pages_htmls/" + file_name.replace("/", "_"), "w+")
    #output.write(mystr)
    #output.close()
output.close()
output_1.close()
