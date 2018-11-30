from pathlib import Path
import os
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=[8,6])
ax.set_title("Distribution of scores amoung our github repos")
ax.set_xlabel("Score bucket")
ax.set_ylabel("Num Projects with score")



parent_dir = Path(os.getcwd()).parent
parent_of_parent = Path(parent_dir).parent
parent_of_parent_of_parent = parent_of_parent.parent

all_scores = list()
data_1 = list()
map1 = dict()
hi = 0
with open(str(parent_of_parent_of_parent) + "/common_stuff/all_project_ground_truths.txt") as opened:
    for line in opened:
        if line == "Name of repo	stars	forks	watches\n":
            continue
        tokens = line.split("\t")
        stars = int(tokens[1])
        forks = int(tokens[2])
        watches = int(tokens[-1])
        score = 0.5 * float(stars) + 0.15 * float(watches) + 0.35 * float(forks)
        all_scores.append(score)
        if score > 5:
            hi += 1
        if score != 0.15:
            data_1.append(score)
        if score in map1:
            map1[score] += 1
        else:
            map1[score] = 1
print(len(data_1))
bin1 = list()
for j in range(30):
    for i in range(0, 10):
        bin1.append(i*0.1 + j)
N, bins, patches = ax.hist(data_1, bins=bin1)
plt.show()
