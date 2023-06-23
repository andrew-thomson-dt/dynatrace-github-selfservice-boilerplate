import yaml
import os

branchName = os.environ["GITHUB_HEAD_REF"].split("/")[-1]
print(f"Branch name: {branchName}")
projectPath = ""

with open("manifest.yaml") as manifest:
    manifest = yaml.safe_load(manifest)
    projects = manifest.get("projects", [])
    for project in projects:
        print(f"Project: {project.get('name')}")
        if project.get("name") == branchName:
            print("Project found in manifest")
            projectPath = project.get("path")
            break
    if projectPath == "":
        print("Project not found in manifest")
        exit(1)

# check if project path exists
if os.path.exists(projectPath):
    print("Project path exists")
    if os.path.exists(projectPath + "/env.vars"):
        with open(projectPath + "/env.vars", 'r') as f:
            data = yaml.safe_load(f)    

        with open(os.environ['GITHUB_ENV'], 'a') as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")
                
        for key, value in data.items():
            os.environ[key] = str(value)
    exit(0)
else:
    print("Project path does not exist")
    exit(1)

