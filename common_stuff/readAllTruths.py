truths = open("all_project_ground_truths.txt", "r")
truths.readline()

#list of (star, project) tuples
projList = []
for line in truths.readlines():
    name, stars, forks, watches = line.split("\t")
    if int(stars) > 100: print name, stars
    projList.append((int(stars), name)) 
projList.sort(reverse = True)
#print projList
#mapping of PROJECT - rank of project
projToRanking = {projList[i][1]: i for i in range(len(projList))}

#ASK user for which projects
while (True):
    query = raw_input()
    print query, projToRanking.get(query, "not in set")
    if query == "EXIT":
	break

