all_repos_to_get = dict()
set1 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/input_data/featurized-repos-2.txt") as input_file:
    for line in input_file:
        if "owner.login_name	owner.type	open_issues_count	has_wiki	has_downloads	has_projects	archived	size	fork	owner_popularity	contributor_popularity	" in line:
            continue
        else:
            tokens = line.split("\t")
            name = tokens[0].replace("/", "_")
            all_repos_to_get[name] = line.rstrip().replace(tokens[0], "")
            set1.add(name)

name_to_num_contributors = dict()
set2 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/all_contributors.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name_to_num_contributors[tokens[0]] = len(tokens[1:])
        set2.add(tokens[0])

need_contributors = open("need_contributors.txt", "w+")
for difference in set1 - set2:
    need_contributors.write(difference + "\n")
need_contributors.close()


name_to_num_pull_requests = dict()
set4 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/repo_to_num_pull_requests.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name_to_num_pull_requests[tokens[0]] = tokens[1]
        set4.add(tokens[0])


need_pull_requests = open("need_pull_requests.txt", "w+")
for difference in set1 - set4:
    need_pull_requests.write(difference + "\n")
need_pull_requests.close()


name_to_num_releases = dict()
set5 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/repo_to_num_releases.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name_to_num_releases[tokens[0]] = tokens[1]
        set5.add(tokens[0])

need_num_releases = open("need_num_releases.txt", "w+")
for difference in set1 - set5:
    need_num_releases.write(difference + "\n")
need_num_releases.close()

name_to_num_times = dict()
set6 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/project_to_times.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name_to_num_times[tokens[0]] = line.replace(tokens[0] + "\t", "")
        set6.add(tokens[0])

need_num_times = open("need_times.txt", "w+")
for difference in set1 - set6:
    need_num_times.write(difference + "\n")
need_num_times.close()

name_to_num_commits = dict()
set7 = set()
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/project_to_commits.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name_to_num_commits[tokens[0].replace("/", "_")] = line.rstrip().replace(tokens[0] + "\t", "")
        set7.add(tokens[0].replace("/", "_"))

need_commits = open("need_commits.txt", "w+")
for difference in set1 - set7:
    need_commits.write(difference + "\n")
need_commits.close()


final_data_to_show = set1 & set2 & set4 & set5 & set6 & set7
print(len(final_data_to_show))

for element in set1 - final_data_to_show:
    print(element)

output = open("featurized-repos_v1DW.txt", "w+")
output.write("owner.login_name\towner.type\topen_issues_count\thas_wiki\thas_downloads\thas_projects\tarchived\tsize\tfork\towner_popularity\tcontributor_popularity\taverage_commit_char_count\tnum_contributors\tnum_pull_requests\tnum_releases\tcommits\tcreated_time\tupdated_time\n")
for element in sorted(list(final_data_to_show)):
    output.write(element)
    output.write(all_repos_to_get[element])
    output.write("\t" + str(name_to_num_contributors[element]))
    output.write("\t" + str(name_to_num_pull_requests[element]))
    output.write("\t" + str(name_to_num_releases[element]))
    output.write("\t" + str(name_to_num_commits[element]))
    output.write("\t" + name_to_num_times[element])
output.close()


output_all_ground_truths = open("all_ground_truths_DWv1.txt", "w+")
with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/input_data/all_project_ground_truths.txt") as opened:
    for line in opened:
        tokens = line.rstrip().split("\t")
        name = tokens[0]
        if name.replace("/", "_") in final_data_to_show:
            output_all_ground_truths.write(line)
output_all_ground_truths.close()