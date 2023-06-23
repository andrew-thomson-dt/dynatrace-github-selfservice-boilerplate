import os

# Open the file
with open('.temp/project_details', 'r') as f:
    # Read the contents of the file
    contents = f.read().splitlines()

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.writelines(contents)
    myfile.write(contents[1].split("/")[1])
