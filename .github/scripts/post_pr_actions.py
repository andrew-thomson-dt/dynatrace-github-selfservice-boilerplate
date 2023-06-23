import os
import yaml
import shutil


def get_project_path(project_name):
    with open("manifest.yaml") as manifest:
        manifest = yaml.safe_load(manifest)
        for project in manifest.get("projects"):
            if project["name"] == project_name:
                return project["path"]
            
        print(f"Project {project_name} not found in manifest.yaml")
        exit(1)

def get_all_configs(project_path):
    delete_configs = []
    for file in os.listdir(project_path):
        if file.endswith(".yaml"):
            with open(f"{project_path}/{file}") as configs:
                configs = yaml.safe_load(configs)
                for config in configs.get("configs"):
                    if config["type"].get("api"):
                        config_api = config["type"]["api"]
                        config_name = config["config"]["name"]
                    else:
                        config_api = config["type"]["settings"]["schema"]
                        config_name = config["id"]

                    delete_configs.append({"name": config_name, "api": config_api})
    return delete_configs

def create_delete_yaml(configs, pr_number):
    if not os.path.exists(f".temp/{pr_number}"):
        os.makedirs(f".temp/{pr_number}")

    with open(f".temp/{pr_number}/delete.yaml", "w") as out:
        out.writelines("delete:\n")
        for config in configs:
            out.writelines(f"  - {config['api']}/{config['name']}\n")

def save_project_name(project_name, pr_number,project_path):
    os.makedirs('.temp') if not os.path.exists('.temp') else None
    with open(".temp/project_details.txt", "w") as out:
        out.write(f"PROJECT_NAME={project_name}\n")
        out.write(f"PROJECT_PATH={project_path}\n")
        out.write(f"PROJECT_ENV={project_path.split('/')[1]}\n")
        out.write(f"PR_NUMBER={pr_number}\n")

def set_env_vars(project_path):
     if os.path.exists(project_path + "/env.vars"):
        with open(project_path + "/env.vars", 'r') as f:
            data = yaml.safe_load(f)    

        with open(os.environ['GITHUB_ENV'], 'a') as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")
                
        for key, value in data.items():
            os.environ[key] = str(value)


if __name__ == "__main__":
    project_name = os.environ["GITHUB_HEAD_REF"].split("/")[-1]
    pr_number = os.environ["GITHUB_REF"].split("/")[-2]

    project_path = get_project_path(project_name)

    configs = get_all_configs(project_path)
    set_env_vars(project_path)

    #create_delete_yaml(configs, pr_number)
    save_project_name(project_name, pr_number, project_path)

    print("Done")

