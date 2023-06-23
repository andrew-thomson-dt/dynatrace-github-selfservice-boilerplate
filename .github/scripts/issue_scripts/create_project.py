import os
import pathlib
import yaml
import subprocess


def import_issue_data():
    with open('issue_body.txt', 'r') as f:
        data = f.readlines()

    result = {}
    key = None

    for line in data:
        line = line.strip()
        if line.startswith('###'):
            key = line[3:].strip()
            result[key] = ''
        elif key is not None:
            if line != '':
                result[key] += line + ' '

    for key, value in result.items():
        result[key] = value.strip()

    result['project_number'] = os.environ['GITHUB_ISSUE_NUMBER']
    result['project_type'] = os.environ['GITHUB_ISSUE_LABEL']

    return result

def create_project_folders(data):
    environment = data.get('environment')
    department = data.get('department')
    application = data.get('application')
    project_type = data.get('project_type')
    project_number = data.get('project_number')
    project_path = os.path.join('configuration', environment, department.lower() , application, f'{project_type}_{project_number}')

    if not os.path.exists(project_path):
        os.makedirs(project_path)

    return project_path

def add_project_to_manifest(project_name, project_path):
    # Load the manifest file
    with open('manifest.yaml', 'r') as f:
        manifest = yaml.safe_load(f)

    if 'projects' not in manifest or manifest['projects'] is None:
        manifest['projects'] = []

    # Create a new project dictionary
    new_project = {'name': project_name, 'path': project_path}

    # Add the new project to the projects list
    manifest['projects'].append(new_project)

    # Write the updated manifest file
    with open('manifest.yaml', 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False)

def move_template_files(project_path):
    # copy the template from .templates/http-health/template.json to the new project folder
    template_path = os.path.join(project_path, 'template.json')
    config_path = os.path.join(project_path, 'config.yaml')

    project_type = "_".join(project_path.split('/')[-1].split('_')[:-1])

    os.system(f"cp .templates/{project_type}.json {template_path}")
    os.system(f"cp .templates/{project_type}.yaml {config_path}")


def write_environment_vars(project_dict):
    with open(os.environ['GITHUB_ENV'], 'a') as f:
        for key, value in project_dict.items():
            f.write(f"{key}={value}\n")
    
    #write project_dict to environment variables
    for key, value in project_dict.items():
        os.environ[key] = value

def write_vars_to_file(project_dict, project_path):
    with open(os.path.join(project_path, 'env.vars'), 'w') as f:
        yaml.dump(project_dict, f, default_flow_style=False)

if __name__ == '__main__':

    project_dict = import_issue_data()

    project_path = create_project_folders(project_dict)

    project_name = f'{project_dict["project_type"]}_{project_dict["project_number"]}'

    add_project_to_manifest(project_name, project_path)

    move_template_files(project_path)

    write_environment_vars(project_dict)

    write_vars_to_file(project_dict, project_path)

    if project_dict.get('script') != None:
        subprocess.run(project_dict.get('script'), shell=True, check=True)