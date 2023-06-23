# Dynatrace Self-Service Portal

## Help guides 

- **You've just forked this repository for the first time** - [fork-quickstart.md](fork-quickstart.md)
- **You want to make changes to your organisation's Dynatrace environments** - [user-guide.md](user-guide.md)

## Repository structure

### **/.github**

Contains the functional components of the Github automation.

New Templates must be created in the `ISSUE_TEMPLATES` folder to be detected by Github. 

Workflows must be in the `workflows` folder to be detected by Github

### **/.temp**

Leave this alone! Used to store various transient assets between steps in the automation.

### **/.templates**

The templates used by the script when an issue is raised. When creating a new issue template place your monaco tempalates here.

### **/configuration**

The fun bit. This is the base folder for the monaco configuration projects. The issue automation will create it's projects here and users can also manually create projects if they want something more advanced than the issue templates. 

The first set of subfolders should match the names of your environments defined in the manifest.yaml. This enables users to easily define which environment their configuration is for.

## Contributors

[Andrew Thomson, Dynatrace](https://dynatrace.slack.com/team/U03C67GAY4T)