import os
import yaml

project_path = os.environ["PROJECT_PATH"]

if os.path.exists(project_path):
    print("Project path exists")
    if os.path.exists(project_path + "/env.vars"):
        with open(project_path + "/env.vars", 'r') as f:
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