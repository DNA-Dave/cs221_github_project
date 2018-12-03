import os

all_files_to_read = [file for file in os.listdir("/Users/davidwu/Desktop/cs221/project/CS221-Data/repo_names_info/") if file.endswith(".json")]
name_to_create_time = dict()
name_to_update_time = dict()
for file_to_read in all_files_to_read:
    with open("/Users/davidwu/Desktop/cs221/project/CS221-Data/repo_names_info/" + file_to_read) as f:
        hello = f.read()
        tokens = hello.split(",")
        created_time = None
        updated_time = None
        for token in tokens:
            if "created_at" in token:
                created_time = token.replace("\"created_at\": \"", "").replace("\"", "").replace("-", "").split("T")[0]
            elif "updated_at" in token:
                updated_time = token.replace("\"updated_at\": \"", "").replace("\"", "").replace("-", "").split("T")[0]
        if created_time is not None and updated_time is not None:
            name_to_create_time[file_to_read] = created_time
            name_to_update_time[file_to_read] = updated_time

output = open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/features/project_to_times.txt", "w+")
output.write("project_name\tcreated_time\tupdated_time\n")
for key in name_to_create_time:
    output.write(key.replace(".json", "") + "\t" + name_to_create_time[key] + "\t" + name_to_update_time[key] + '\n')
output.close()

