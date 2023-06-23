# Fork Quickstart

- [Fork Quickstart](#fork-quickstart)
- [Repository Setup](#repository-setup)
  - [Manifest File](#manifest-file)
  - [Environment folders](#environment-folders)
  - [Secrets](#secrets)
  - [Dev environment](#dev-environment)

# Repository Setup

## Manifest File

Create a manifest file in the configuration folder. Use the existing template or create your own based on [guidance at dynatrace](https://www.dynatrace.com/support/help/manage/configuration-as-code/manage-configuration)

## Environment folders

Create folders under .configuration that match the environment names set in the manifest above. 

For example:

```
└───configuration
    ├───dev
    ├───production
    └───sandbox
```

## Secrets

Add [secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) to the repository for the monaco access tokens needed for each environment. Using the naming structure `monaco_<env name>`


## Dev environment

The pull request workflow will try to deploy the configuration to an environment named `dev` in your 
manifest.yaml. This is to test the configuration and to give the approver somewhere to view the configuration in the UI. 

If you want to name the dev environment differently in your mainfest file you can change the reference in the workflow. The environment name is referenced in the monaco deploy scripts. Also be concious of your secret naming. 

.github/workflows/monaco-pr-dev.yml
```yaml
# Dry run the deployment to check for defects
- name: Monaco Dry Run
env:
    MONACO_DEV: ${{ secrets.MONACO_DEV }}
    MONACO_SANDBOX: ${{ secrets.MONACO_SANDBOX }}
    PROJECT: ${{ github.head_ref}}
run: | 
    echo $PROJECT
    monaco deploy --dry-run -g <dev env name> manifest.yaml -p $PROJECT

# Deploy to dev
- name: Monaco Deploy
env:
    MONACO_DEV: ${{ secrets.MONACO_DEV }}
    MONACO_SANDBOX: ${{ secrets.MONACO_SANDBOX }}
    PROJECT: ${{ github.head_ref }}
run: | 
    monaco deploy -g <dev env name> manifest.yaml -p $PROJECT
```

---


