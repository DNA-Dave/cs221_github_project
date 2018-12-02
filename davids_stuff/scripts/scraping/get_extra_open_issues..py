import requests
from tqdm import tqdm

to_download = list()

with open("need_open_issues.txt") as input_file:
    for line in input_file:
        to_download.append(line.rstrip().replace("_", "/", 1))
output = open("project_to_num_open_issues_second_round.txt", "w+")
for i in tqdm(range(len(to_download))):
    element = to_download[i]
    url = "https://api.github.com/repos/" + element
    response = requests.get(url, auth=('username', '40dec8eb34d3b654c3204b750f0725c610dfb705'))
    if 200 <= response.status_code <= 299:
        data = response.json()
        output.write(element + "\t" + str(data['open_issues']) + "\n")
    else:
        print(url)
output.close()